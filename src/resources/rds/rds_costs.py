# resources/rds/rds_costs.py

from core import duration_meta, pricing_utils
from resources.rds import rds_filters, rds_meta, rds_utils

HOURS_PER_MONTH = duration_meta.HOURS_PER_MONTH


def process_rds(plan: dict, pricing_client, region: str) -> tuple:
    instances = rds_meta.extract_all(plan)
    if not instances:
        return [], 0.0

    rows = []
    total_cost = 0.0

    for rds_info in instances:
        instance_filters = rds_filters.build(
            instance_class=rds_info["instance_class"],
            engine=rds_info["engine"],
            location=region,
            multi_az=rds_info["multi_az"],
        )
        instance_price = pricing_utils.get_price_for_service(pricing_client, "AmazonRDS", instance_filters)

        storage_price = rds_utils.get_rds_storage_price(pricing_client, rds_info["storage_type"], region)
        storage_cost = storage_price * rds_info["storage_gb"]

        total_instance_cost = round(instance_price * HOURS_PER_MONTH, 5)
        total_storage_cost = round(storage_cost, 5)
        instance_total = round(total_instance_cost + total_storage_cost, 5)

        rows.append(["RDS Instance", 1, rds_info["instance_class"], f"${total_instance_cost:.5f}"])
        rows.append(["RDS Storage", rds_info["storage_gb"], rds_info["storage_type"], f"${total_storage_cost:.5f}"])
        total_cost += instance_total

    return rows, round(total_cost, 5)
