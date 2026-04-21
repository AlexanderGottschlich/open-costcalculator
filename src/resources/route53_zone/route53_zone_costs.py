# resources/route53_zone/route53_zone_costs.py

from core import pricing_utils
from resources.route53_zone import route53_zone_meta

ROUTE53_ZONE_RATE = 0.50  # $0.50 per hosted zone per month


def build_route53_zone_filter(region):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Amazon Route 53"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": "HostedZone"},
    ]


def get_route53_zone_price(pricing, region):
    return pricing_utils.get_price_for_service(
        pricing,
        "AmazonRoute53",
        build_route53_zone_filter(region),
        unit="Hrs",
        fallback_price=ROUTE53_ZONE_RATE,
    )


def process_route53_zone(plan, pricing, region):
    zones = route53_zone_meta.extract_route53_zone(plan)
    if not zones:
        return [], 0.0

    zone_count = len(zones)
    price_per_zone = get_route53_zone_price(pricing, region)

    total_cost = round(price_per_zone * zone_count, 5)

    return [
        [
            "Route53 Zone",
            zone_count,
            "HostedZone",
            f"${total_cost:.5f}",
        ]
    ], total_cost
