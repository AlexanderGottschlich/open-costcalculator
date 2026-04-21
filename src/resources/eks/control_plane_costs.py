from datetime import datetime

from core import logger, pricing_defaults, pricing_utils
from resources.eks import cluster_meta, eks_pricing_meta


def calculate_control_plane_cost(release_date, hours):
    if not release_date:
        logger.warn("Keine Release-Info gefunden – Standardrate wird verwendet.")
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours

    current_date = datetime.now()
    months_since_release = (current_date.year - release_date.year) * 12 + current_date.month - release_date.month

    if months_since_release <= 12:
        logger.info(f"EKS Control Plane: Standard Rate ({months_since_release} Monate)")
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours
    elif months_since_release <= 14:
        logger.info(f"EKS Control Plane: Extended Rate ({months_since_release} Monate)")
        return pricing_defaults.CONTROL_PLANE_EXTENDED_RATE * hours
    else:
        logger.warn("Kubernetes-Version wird möglicherweise nicht mehr unterstützt.")
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours


def process_control_plane(plan, hours):
    k8s_version = cluster_meta.extract_version(plan)
    if not k8s_version:
        logger.warn("Keine Kubernetes-Version im Plan gefunden – Kontrollplane-Kosten nicht berechnet.")
        return [], 0.0

    release_date = eks_pricing_meta.get_release_date(k8s_version)
    cp_cost = round(calculate_control_plane_cost(release_date, hours), 5)
    return [["Control Plane", 1, f"v{k8s_version}", f"${cp_cost:.5f}"]], cp_cost
