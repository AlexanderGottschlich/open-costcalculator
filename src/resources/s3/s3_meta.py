# resources/s3/s3_meta.py

from core import config_loader


def extract_s3_bucket(plan):
    buckets = []
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_s3_bucket":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after")
                if after is not None:
                    bucket_name = after.get("bucket", "unknown")
                    versioning = after.get("versioning", False)
                    server_side_encryption = after.get("server_side_encryption_configuration", False)
                    buckets.append(
                        {
                            "name": bucket_name,
                            "versioning": versioning,
                            "server_side_encryption": server_side_encryption,
                        }
                    )
    return buckets


def detect_s3_usage(plan):
    buckets = extract_s3_bucket(plan)
    return len(buckets) > 0


def count(plan):
    return len(extract_s3_bucket(plan))


def get_s3_config(app_config, bucket_name):
    return config_loader.get_resource_config(app_config, "s3", bucket_name)
