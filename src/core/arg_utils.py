# filter/arg_utils.py

import argparse

from core.config import DEFAULT_REGION

DEFAULT_PLAN_PATH = "../plan/terraform-loadbalancer.plan.json"
DEFAULT_CONFIG_PATH = "config.yaml"
LOG_DEBUG = False
LOG_LEVEL = "INFO"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=DEFAULT_PLAN_PATH, help="Pfad zur terraform-eks.plan.json Datei")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="Pfad zur config.yaml Datei")
    parser.add_argument("--debug", action="store_true", help="Aktiviere detaillierte Debug-Ausgaben für Preisabfragen")
    parser.add_argument("--region", default=DEFAULT_REGION, help="AWS Region (default: eu-central-1)")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)",
    )
    parser.add_argument(
        "--group-by",
        default=None,
        choices=["project", "team", "environment", "cost_center"],
        help="Group costs by tag (default: None)",
    )
    args = parser.parse_args()

    global LOG_DEBUG, LOG_LEVEL
    LOG_DEBUG = args.debug
    LOG_LEVEL = args.log_level

    return args
