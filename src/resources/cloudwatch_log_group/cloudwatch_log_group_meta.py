# resources/cloudwatch_log_group/cloudwatch_log_group_meta.py


def extract_cloudwatch_log_group(plan):
    log_groups = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_cloudwatch_log_group":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    name = after.get("name", "unknown")
                    retention_in_days = after.get("retention_in_days")
                    log_groups.append(
                        {
                            "name": name,
                            "retention_in_days": retention_in_days,
                        }
                    )
    return log_groups


def detect_cloudwatch_log_group_usage(plan):
    log_groups = extract_cloudwatch_log_group(plan)
    return len(log_groups) > 0


def count(plan):
    return len(extract_cloudwatch_log_group(plan))
