# resources/eks/nodegroup_costs.py

from core import duration_meta, logger, pricing_utils
from resources.eks import ec2_filters

HOURS_PER_MONTH = duration_meta.HOURS_PER_MONTH


def process_node_group(pricing_client, ec2_client, instance_type, desired_size, market_option, region):
    if not instance_type or desired_size <= 0:
        return [], 0.0

    filters = ec2_filters.build(instance_type, region, market_option)

    if market_option == "OnDemand":
        price = pricing_utils.get_price_for_service(pricing_client, "AmazonEC2", filters)
    else:
        price = pricing_utils.get_spot_price(ec2_client, instance_type)

    total_cost = round(price * desired_size * HOURS_PER_MONTH, 5)

    logger.info(f"NodeGroup: {desired_size} x {instance_type} ({market_option}) = {total_cost} USD/Monat")
    return [["EKS Node Group", desired_size, instance_type, f"${total_cost:.5f}"]], total_cost
