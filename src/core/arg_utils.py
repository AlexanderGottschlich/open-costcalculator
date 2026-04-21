# filter/arg_utils.py

import argparse

from core.config import DEFAULT_REGION

DEFAULT_PLAN_PATH = "../plan/terraform-loadbalancer.plan.json"
LOG_DEBUG = False  # Werd per parse_args() aktualisiert


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=DEFAULT_PLAN_PATH, help="Pfad zur terraform-eks.plan.json Datei")
    parser.add_argument("--debug", action="store_true", help="Aktiviere detaillierte Debug-Ausgaben für Preisabfragen")
    parser.add_argument("--region", default=DEFAULT_REGION, help="AWS Region (default: eu-central-1)")
    args = parser.parse_args()

    global LOG_DEBUG
    LOG_DEBUG = args.debug

    return args
