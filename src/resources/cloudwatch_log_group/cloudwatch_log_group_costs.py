# resources/cloudwatch_log_group/cloudwatch_log_group_costs.py

from core import pricing_utils
from resources.cloudwatch_log_group import cloudwatch_log_group_meta

CLOUDWATCH_LOG_GB_RATE = 0.50  # $0.50 per GB stored per month


def build_cloudwatch_log_filter(region):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Amazon CloudWatch Logs"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": "DataProcessing-Bytes"},
    ]


def get_cloudwatch_log_price(pricing, region):
    return pricing_utils.get_price_for_service(
        pricing,
        "AmazonCloudWatch",
        build_cloudwatch_log_filter(region),
        unit="GB",
        fallback_price=CLOUDWATCH_LOG_GB_RATE,
    )


def process_cloudwatch_log_group(plan, pricing, region):
    log_groups = cloudwatch_log_group_meta.extract_cloudwatch_log_group(plan)
    if not log_groups:
        return [], 0.0

    log_group_count = len(log_groups)
    price_per_gb = get_cloudwatch_log_price(pricing, region)

    total_cost = round(price_per_gb * log_group_count, 5)

    return [
        [
            "CloudWatch Log Group",
            log_group_count,
            "LogGroup",
            f"${total_cost:.5f}",
        ]
    ], total_cost
