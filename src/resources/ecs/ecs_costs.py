# resources/ecs/ecs_costs.py

from core import logger, pricing_defaults, pricing_utils
from resources.ecs import ecs_meta


def build_fargate_cpu_filter(region):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "EC2 Fargate"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": "Fargate-vCPU-Hours"},
    ]


def build_fargate_memory_filter(region):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "EC2 Fargate"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": "Fargate-GB-Hours"},
    ]


def get_fargate_pricing(pricing, region):
    cpu_price = pricing_utils.get_price_for_service(
        pricing,
        "AmazonECS",
        build_fargate_cpu_filter(region),
        unit="Hrs",
        fallback_price=pricing_defaults.FARGATE_VCPU_RATE,
    )
    memory_price = pricing_utils.get_price_for_service(
        pricing,
        "AmazonECS",
        build_fargate_memory_filter(region),
        unit="GB-Hrs",
        fallback_price=pricing_defaults.FARGATE_RAM_RATE,
    )
    return cpu_price, memory_price


def calculate_fargate_cost(cpu, memory, cpu_price, memory_price, desired_count, hours):
    try:
        cpu_value = int(cpu) if cpu else pricing_defaults.FARGATE_DEFAULT_VCPU
    except (ValueError, TypeError):
        cpu_value = pricing_defaults.FARGATE_DEFAULT_VCPU

    try:
        memory_value = int(memory) if memory else pricing_defaults.FARGATE_DEFAULT_RAM_GB
    except (ValueError, TypeError):
        memory_value = pricing_defaults.FARGATE_DEFAULT_RAM_GB

    cpu_units_to_vcpu = cpu_value / 1024.0

    cpu_cost = cpu_price * cpu_units_to_vcpu * hours * desired_count
    memory_cost = memory_price * memory_value * hours * desired_count

    return round(cpu_cost + memory_cost, 5)


def process_ecs(plan, pricing, region, hours):
    ecs_data = ecs_meta.extract(plan)

    if not ecs_data:
        return [], 0.0

    launch_type = ecs_data.get("launch_type", "FARGATE")

    if launch_type and launch_type.upper() != "FARGATE":
        logger.info(f"ECS launch_type '{launch_type}' wird derzeit nicht unterstützt")
        return [], 0.0

    cpu = ecs_data.get("cpu")
    memory = ecs_data.get("memory")
    desired_count = ecs_data.get("desired_count", 1)

    cpu_price, memory_price = get_fargate_pricing(pricing, region)

    cost = calculate_fargate_cost(cpu, memory, cpu_price, memory_price, desired_count, hours)

    cpu_str = f"{cpu}vCPU" if cpu else f"{pricing_defaults.FARGATE_DEFAULT_VCPU}vCPU"
    memory_str = f"{memory}GB" if memory else f"{pricing_defaults.FARGATE_DEFAULT_RAM_GB}GB"

    return [
        [
            "ECS Fargate",
            desired_count,
            f"{cpu_str}/{memory_str}",
            f"${cost:.5f}",
        ]
    ], cost
