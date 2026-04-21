# tests/test_cognito_user_pool.py

from resources.cognito_user_pool import cognito_user_pool_meta


def test_extract_cognito_user_pool():
    plan = {
        "resource_changes": [
            {
                "type": "aws_cognito_user_pool",
                "change": {
                    "actions": ["create"],
                    "after": {"name": "my-pool", "id": "us-east-1_xxxxx"},
                },
            }
        ]
    }
    result = cognito_user_pool_meta.extract_cognito_user_pool(plan)
    assert len(result) == 1
    assert result[0]["name"] == "my-pool"


def test_extract_cognito_user_pool_no_pools():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    result = cognito_user_pool_meta.extract_cognito_user_pool(plan)
    assert result == []


def test_extract_multiple_pools():
    plan = {
        "resource_changes": [
            {"type": "aws_cognito_user_pool", "change": {"actions": ["create"], "after": {"name": "pool1"}}},
            {"type": "aws_cognito_user_pool", "change": {"actions": ["create"], "after": {"name": "pool2"}}},
        ]
    }
    result = cognito_user_pool_meta.extract_cognito_user_pool(plan)
    assert len(result) == 2


def test_detect_cognito_user_pool_usage():
    plan = {"resource_changes": [{"type": "aws_cognito_user_pool", "change": {"actions": ["create"], "after": {}}}]}
    assert cognito_user_pool_meta.detect_cognito_user_pool_usage(plan) is True


def test_detect_cognito_user_pool_usage_no_pools():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert cognito_user_pool_meta.detect_cognito_user_pool_usage(plan) is False


def test_count_pools():
    plan = {
        "resource_changes": [
            {"type": "aws_cognito_user_pool", "change": {"actions": ["create"], "after": {}}},
            {"type": "aws_cognito_user_pool", "change": {"actions": ["create"], "after": {}}},
        ]
    }
    assert cognito_user_pool_meta.count(plan) == 2


def test_count_pools_none():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert cognito_user_pool_meta.count(plan) == 0
