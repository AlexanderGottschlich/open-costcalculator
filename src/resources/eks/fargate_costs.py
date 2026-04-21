# resources/eks/fargate_costs.py

from core import pricing_defaults


def calculate_fargate_cost(hours):
    cpu_cost = pricing_defaults.FARGATE_VCPU_RATE * pricing_defaults.FARGATE_DEFAULT_VCPU
    ram_cost = pricing_defaults.FARGATE_RAM_RATE * pricing_defaults.FARGATE_DEFAULT_RAM_GB
    total_per_pod = (cpu_cost + ram_cost) * hours
    return round(total_per_pod * pricing_defaults.FARGATE_DEFAULT_PODS, 5)


def detect_fargate_usage(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_eks_fargate_profile":
            return True
    return False


def process_fargate(hours):
    cost = calculate_fargate_cost(hours)
    return [
        [
            "EKS Fargate",
            pricing_defaults.FARGATE_DEFAULT_PODS,
            f"{pricing_defaults.FARGATE_DEFAULT_VCPU}vCPU/{pricing_defaults.FARGATE_DEFAULT_RAM_GB}GB",
            f"${cost:.5f}",
        ]
    ], cost
