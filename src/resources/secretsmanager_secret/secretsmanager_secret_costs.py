# resources/secretsmanager_secret/secretsmanager_secret_costs.py

from core import pricing_utils
from resources.secretsmanager_secret import secretsmanager_secret_meta

SEGRETSMANAGER_SECRET_RATE = 0.40  # $0.40 per secret per month (Standard Tier)


def build_secretsmanager_filter(region):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Secrets Manager"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": "SecretStorage"},
    ]


def get_secretsmanager_price(pricing, region):
    return pricing_utils.get_price_for_service(
        pricing,
        "AWSSecretsManager",
        build_secretsmanager_filter(region),
        unit="GB/Mo",
        fallback_price=SEGRETSMANAGER_SECRET_RATE,
    )


def process_secretsmanager_secret(plan, pricing, region):
    secrets = secretsmanager_secret_meta.extract_secretsmanager_secret(plan)
    if not secrets:
        return [], 0.0

    secret_count = len(secrets)
    price_per_secret = get_secretsmanager_price(pricing, region)

    total_cost = round(price_per_secret * secret_count, 5)

    return [
        [
            "Secrets Manager",
            secret_count,
            "Secret",
            f"${total_cost:.5f}",
        ]
    ], total_cost
