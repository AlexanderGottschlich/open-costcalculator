# resources/route53_zone/route53_zone_meta.py


def extract_route53_zone(plan):
    zones = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_route53_zone":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    name = after.get("name", "unknown")
                    zone_id = after.get("zone_id", "")
                    zones.append({"name": name, "zone_id": zone_id})
    return zones


def detect_route53_zone_usage(plan):
    zones = extract_route53_zone(plan)
    return len(zones) > 0


def count(plan):
    return len(extract_route53_zone(plan))
