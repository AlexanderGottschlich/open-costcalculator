# main.py

import json
import sys
from pathlib import Path

import boto3
from tabulate import tabulate

from core import (arg_utils, config, config_loader, duration_meta, logger,
                  plan_compare)
from core.group_by import tags as group_tags
from resources.alb import alb_costs
from resources.cloudwatch_log_group import cloudwatch_log_group_costs
from resources.cognito_user_pool import cognito_user_pool_costs
from resources.ecs import ecs_costs
from resources.eks import (control_plane_costs, fargate_costs, nodegroup_costs,
                           nodegroup_meta)
from resources.nat_gateway import nat_gateway_meta
from resources.rds import rds_costs
from resources.route53_zone import route53_zone_costs
from resources.s3 import s3_costs
from resources.secretsmanager_secret import secretsmanager_secret_costs
from resources.ses_domain_identity import ses_domain_identity_costs

TF_PLAN_FILE = "../plan/terraform-sf2l.plan.json"
IGNORED_PREFIXES = [
    "aws_iam_",
    "aws_network_acl",
    "aws_vpc",
    "aws_subnet",
    "aws_route",
    "aws_default_",
    "aws_internet_gateway",
]
IGNORED_RESOURCE_TYPES = ["null_resource", "local_file", "random_", "external"]

HOURS_PER_MONTH = duration_meta.HOURS_PER_MONTH


def parse_args():
    return arg_utils.parse_args()


def is_relevant_resource(resource_type):
    return not any(resource_type.startswith(prefix) for prefix in IGNORED_PREFIXES + IGNORED_RESOURCE_TYPES)


def extract_relevant_resources(plan_path):
    with open(plan_path) as f:
        plan = json.load(f)
    return sorted(
        {change.get("type") for change in plan.get("resource_changes", []) if is_relevant_resource(change.get("type"))}
    )


def extract_region_from_plan(plan):
    try:
        root = plan["configuration"]["provider_config"]["aws"]["expressions"]
        if "region" in root:
            return root["region"]["constant"]
    except Exception:
        pass
    return "eu-central-1"


def print_summary_table(table, total_cost):
    logger.info("Ressourcen Kostenubersicht (pro Monat)")
    print(tabulate(table, headers=["Komponente", "Anzahl", "Typ", "Kosten"], tablefmt="github"))
    logger.info(f"Gesamtkosten/Monat: ${round(total_cost, 5)}")


def analyze_plan(plan, pricing, region, app_config):
    table = []
    total_cost = 0.0

    has_eks_resources = any(
        res.get("type") in ["aws_eks_cluster", "aws_eks_node_group", "aws_eks_fargate_profile"]
        for res in plan.get("resource_changes", [])
    )

    if has_eks_resources:
        use_fargate = fargate_costs.detect_fargate_usage(plan)
        instance_type, capacity_type, desired_size = nodegroup_meta.extract(plan)

        marketoption = "OnDemand" if not capacity_type or capacity_type.upper() == "ON_DEMAND" else "Spot"
        if not capacity_type:
            logger.warn("Keine capacity_type gefunden - fallback zu 'OnDemand'")

        rows, cost = control_plane_costs.process_control_plane(plan, HOURS_PER_MONTH)
        table.extend(rows)
        total_cost += cost

        if instance_type and desired_size > 0 and not use_fargate:
            ec2_client = boto3.client("ec2", region_name=region)
            rows, cost = nodegroup_costs.process_node_group(
                pricing, ec2_client, instance_type, desired_size, marketoption, region
            )
            table.extend(rows)
            total_cost += cost

        if use_fargate:
            rows, cost = fargate_costs.process_fargate(HOURS_PER_MONTH)
            table.extend(rows)
            total_cost += cost

    has_ecs_resources = any(
        res.get("type") in ["aws_ecs_cluster", "aws_ecs_task_definition", "aws_ecs_service"]
        for res in plan.get("resource_changes", [])
    )

    if has_ecs_resources:
        rows, cost = ecs_costs.process_ecs(plan, pricing, region, HOURS_PER_MONTH)
        table.extend(rows)
        total_cost += cost

    rows, cost = alb_costs.calculate_alb_cost(plan, HOURS_PER_MONTH)
    table.extend(rows)
    total_cost += cost

    rows, cost = nat_gateway_meta.process_nat_gateway(plan, pricing, region, HOURS_PER_MONTH)
    table.extend(rows)
    total_cost += cost

    rds_rows, rds_total = rds_costs.process_rds(plan, pricing, region)
    table.extend(rds_rows)
    total_cost += rds_total

    has_secretsmanager_resources = any(
        res.get("type") == "aws_secretsmanager_secret" for res in plan.get("resource_changes", [])
    )

    if has_secretsmanager_resources:
        rows, cost = secretsmanager_secret_costs.process_secretsmanager_secret(plan, pricing, region)
        table.extend(rows)
        total_cost += cost

    has_route53_zone_resources = any(res.get("type") == "aws_route53_zone" for res in plan.get("resource_changes", []))

    if has_route53_zone_resources:
        rows, cost = route53_zone_costs.process_route53_zone(plan, pricing, region)
        table.extend(rows)
        total_cost += cost

    has_cloudwatch_log_group_resources = any(
        res.get("type") == "aws_cloudwatch_log_group" for res in plan.get("resource_changes", [])
    )

    if has_cloudwatch_log_group_resources:
        rows, cost = cloudwatch_log_group_costs.process_cloudwatch_log_group(plan, pricing, region)
        table.extend(rows)
        total_cost += cost

    has_ses_domain_identity_resources = any(
        res.get("type") == "aws_ses_domain_identity" for res in plan.get("resource_changes", [])
    )

    if has_ses_domain_identity_resources:
        rows, cost = ses_domain_identity_costs.process_ses_domain_identity(plan)
        table.extend(rows)
        total_cost += cost

    has_cognito_user_pool_resources = any(
        res.get("type") == "aws_cognito_user_pool" for res in plan.get("resource_changes", [])
    )

    if has_cognito_user_pool_resources:
        rows, cost = cognito_user_pool_costs.process_cognito_user_pool(plan)
        table.extend(rows)
        total_cost += cost

    has_s3_resources = any(res.get("type") == "aws_s3_bucket" for res in plan.get("resource_changes", []))

    if has_s3_resources:
        rows, cost = s3_costs.process_s3(plan, pricing, region, app_config)
        table.extend(rows)
        total_cost += cost

    return table, round(total_cost, 5)


def main():
    args = parse_args()
    logger.setup_logging(args.log_level)

    plan_path = Path(args.plan)
    if not plan_path.is_file():
        logger.error(f"Die angegebene Datei '{args.plan}' wurde nicht gefunden.")
        sys.exit(1)

    with open(args.plan) as f:
        plan = json.load(f)

    app_config = config_loader.load_config(args.config)
    if app_config:
        logger.info(f"Konfiguration geladen aus: {args.config}")

    region = args.region if args.region != config.DEFAULT_REGION else extract_region_from_plan(plan)
    logger.info(f"Verwende Region: {region}")

    pricing = boto3.client("pricing", region_name="us-east-1")

    if args.compare:
        compare_path = Path(args.compare)
        if not compare_path.is_file():
            logger.error(f"Die Vergleichsdatei '{args.compare}' wurde nicht gefunden.")
        else:
            with open(args.compare) as f:
                compare_plan = json.load(f)

            comparison = plan_compare.compare_plans(args.compare, args.plan)
            logger.info("")
            logger.info(plan_compare.format_comparison(comparison))

            before_region = (
                args.region if args.region != config.DEFAULT_REGION else extract_region_from_plan(compare_plan)
            )
            before_pricing = boto3.client("pricing", region_name="us-east-1")

            before_table, before_cost = analyze_plan(compare_plan, before_pricing, before_region, app_config)
            after_table, after_cost = analyze_plan(plan, pricing, region, app_config)

            plan_compare.print_cost_comparison(Path(args.compare).name, before_cost, Path(args.plan).name, after_cost)

            print_summary_table(after_table, after_cost)
            return

    table, total_cost = analyze_plan(plan, pricing, region, app_config)

    if args.group_by:
        tagged_resources = group_tags.extract_all_resource_tags(plan)
        if tagged_resources:
            groups = group_tags.group_by_key(tagged_resources, args.group_by)
            logger.info(f"Grouped by tag: {args.group_by}")
            for group_name, resources in groups.items():
                logger.info(f"  {args.group_by}={group_name}: {len(resources)} resources")
        else:
            logger.info(f"No resources found with tag '{args.group_by}'")

    print_summary_table(table, total_cost)


if __name__ == "__main__":
    main()
