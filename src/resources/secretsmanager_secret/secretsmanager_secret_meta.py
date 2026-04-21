# resources/secretsmanager_secret/secretsmanager_secret_meta.py


def extract_secretsmanager_secret(plan):
    secrets = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_secretsmanager_secret":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    name = after.get("name", "unknown")
                    secret_arn = after.get("arn", "")
                    recovery_window = after.get("recovery_window_in_days", 30)
                    secrets.append(
                        {
                            "name": name,
                            "arn": secret_arn,
                            "recovery_window_in_days": recovery_window,
                        }
                    )
    return secrets


def detect_secretsmanager_usage(plan):
    secrets = extract_secretsmanager_secret(plan)
    return len(secrets) > 0


def count(plan):
    return len(extract_secretsmanager_secret(plan))
