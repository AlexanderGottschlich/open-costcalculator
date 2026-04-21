# filter/rds_meta.py


def extract(plan):
    instances = extract_all(plan)
    return instances[0] if instances else None


def extract_all(plan):
    instances = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_db_instance":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    instances.append(
                        {
                            "instance_class": after.get("instance_class"),
                            "engine": after.get("engine"),
                            "storage_gb": after.get("allocated_storage", 20),
                            "multi_az": after.get("multi_az", False),
                            "storage_type": after.get("storage_type", "gp2"),
                        }
                    )
    return instances


def count(plan):
    return len(extract_all(plan))
