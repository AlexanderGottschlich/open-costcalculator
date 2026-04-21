# resources/cognito_user_pool/cognito_user_pool_meta.py


def extract_cognito_user_pool(plan):
    pools = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_cognito_user_pool":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    pool_name = after.get("name", "unknown")
                    user_pool_id = after.get("id", "")
                    pools.append({"name": pool_name, "id": user_pool_id})
    return pools


def detect_cognito_user_pool_usage(plan):
    pools = extract_cognito_user_pool(plan)
    return len(pools) > 0


def count(plan):
    return len(extract_cognito_user_pool(plan))
