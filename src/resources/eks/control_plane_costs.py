from datetime import datetime

from core import pricing_defaults
from resources.eks import cluster_meta, eks_pricing_meta


def calculate_control_plane_cost(release_date, hours):
    if not release_date:
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours

    current_date = datetime.now()
    months_since_release = (current_date.year - release_date.year) * 12 + current_date.month - release_date.month

    if months_since_release <= 12:
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours
    elif months_since_release <= 14:
        return pricing_defaults.CONTROL_PLANE_EXTENDED_RATE * hours
    else:
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours


def process_control_plane(plan, hours):
    k8s_version = cluster_meta.extract_version(plan)
    if not k8s_version:
        return [], 0.0

    release_date = eks_pricing_meta.get_release_date(k8s_version)
    cp_cost = round(calculate_control_plane_cost(release_date, hours), 5)
    return [["Control Plane", 1, f"v{k8s_version}", f"${cp_cost:.5f}"]], cp_cost
