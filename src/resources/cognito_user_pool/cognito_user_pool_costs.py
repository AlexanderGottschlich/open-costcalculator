# resources/cognito_user_pool/cognito_user_pool_costs.py

from resources.cognito_user_pool import cognito_user_pool_meta


def process_cognito_user_pool(plan):
    pools = cognito_user_pool_meta.extract_cognito_user_pool(plan)
    if not pools:
        return [], 0.0

    pool_count = len(pools)

    return [
        [
            "Cognito User Pool",
            pool_count,
            "Pool",
            "$0.00",
        ]
    ], 0.0
