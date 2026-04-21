# resources/ses_domain_identity/ses_domain_identity_meta.py


def extract_ses_domain_identity(plan):
    identities = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_ses_domain_identity":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    domain = after.get("domain", "unknown")
                    identities.append({"domain": domain})
    return identities


def detect_ses_domain_identity_usage(plan):
    identities = extract_ses_domain_identity(plan)
    return len(identities) > 0


def count(plan):
    return len(extract_ses_domain_identity(plan))
