# filter/arg_utils.py

import argparse

DEFAULT_PLAN_PATH = "../plan/terraform-loadbalancer.plan.json"
LOG_DEBUG = False  # Wird per parse_args() aktualisiert


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=DEFAULT_PLAN_PATH, help="Pfad zur terraform-eks.plan.json Datei")
    parser.add_argument("--debug", action="store_true", help="Aktiviere detaillierte Debug-Ausgaben für Preisabfragen")
    args = parser.parse_args()

    global LOG_DEBUG
    LOG_DEBUG = args.debug  # Setze globales Flag

    return args
