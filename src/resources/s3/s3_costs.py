# resources/s3/s3_costs.py

from core import pricing_utils
from resources.s3 import s3_meta

S3_STORAGE_GB_RATE = {
    "STANDARD": 0.023,
    "STANDARD_IA": 0.0125,
    "GLACIER": 0.004,
    "INTELLIGENT_TIERING": 0.0125,
    "DEEP_ARCHIVE": 0.00099,
}

S3_API_REQUEST_RATE = {
    "PUT": 0.005,
    "GET": 0.0004,
    "DELETE": 0.0,
}


def build_s3_storage_filter(region, storage_class="Standard"):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Amazon S3"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": f"TimedStorage-ByteHrs"},
    ]


def get_s3_storage_price(pricing, region, storage_class):
    rate = S3_STORAGE_GB_RATE.get(storage_class, S3_STORAGE_GB_RATE["STANDARD"])
    return pricing_utils.get_price_for_service(
        pricing,
        "AmazonS3",
        build_s3_storage_filter(region, storage_class),
        unit="GB/Mo",
        fallback_price=rate,
    )


def calculate_s3_cost(storage_gb, storage_class, storage_price, get_requests, put_requests):
    storage_cost = storage_price * storage_gb
    api_cost = (get_requests * S3_API_REQUEST_RATE["GET"]) + (put_requests * S3_API_REQUEST_RATE["PUT"])
    return round(storage_cost + api_cost, 5)


def process_s3(plan, pricing, region, app_config):
    buckets = s3_meta.extract_s3_bucket(plan)
    if not buckets:
        return [], 0.0

    rows = []
    total_cost = 0.0

    for bucket in buckets:
        bucket_name = bucket["name"]
        s3_config = s3_meta.get_s3_config(app_config, bucket_name)

        storage_gb = s3_config.get("estimated_storage_gb", 1)
        storage_class = s3_config.get("storage_class", "STANDARD")
        get_requests = s3_config.get("estimated_get_requests", 0)
        put_requests = s3_config.get("estimated_put_requests", 0)

        storage_price = get_s3_storage_price(pricing, region, storage_class)
        bucket_cost = calculate_s3_cost(storage_gb, storage_class, storage_price, get_requests, put_requests)

        rows.append(["S3 Bucket", bucket_name, f"{storage_gb}GB/{storage_class}", f"${bucket_cost:.5f}"])
        total_cost += bucket_cost

    if total_cost == 0:
        return [["?", len(buckets), "Buckets", "$0.00 (requires config)"]], 0.0

    return rows, round(total_cost, 5)
