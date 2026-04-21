# tests/test_cloudwatch_log_group.py

from resources.cloudwatch_log_group import cloudwatch_log_group_meta


def test_extract_cloudwatch_log_group():
    plan = {
        "resource_changes": [
            {
                "type": "aws_cloudwatch_log_group",
                "change": {
                    "actions": ["create"],
                    "after": {"name": "/aws/lambda/my-function", "retention_in_days": 30},
                },
            }
        ]
    }
    result = cloudwatch_log_group_meta.extract_cloudwatch_log_group(plan)
    assert len(result) == 1
    assert result[0]["name"] == "/aws/lambda/my-function"
    assert result[0]["retention_in_days"] == 30


def test_extract_cloudwatch_log_group_no_groups():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    result = cloudwatch_log_group_meta.extract_cloudwatch_log_group(plan)
    assert result == []


def test_extract_multiple_groups():
    plan = {
        "resource_changes": [
            {"type": "aws_cloudwatch_log_group", "change": {"actions": ["create"], "after": {"name": "/group1"}}},
            {"type": "aws_cloudwatch_log_group", "change": {"actions": ["create"], "after": {"name": "/group2"}}},
        ]
    }
    result = cloudwatch_log_group_meta.extract_cloudwatch_log_group(plan)
    assert len(result) == 2


def test_detect_cloudwatch_log_group_usage():
    plan = {"resource_changes": [{"type": "aws_cloudwatch_log_group", "change": {"actions": ["create"], "after": {}}}]}
    assert cloudwatch_log_group_meta.detect_cloudwatch_log_group_usage(plan) is True


def test_detect_cloudwatch_log_group_usage_no_groups():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert cloudwatch_log_group_meta.detect_cloudwatch_log_group_usage(plan) is False


def test_count_groups():
    plan = {
        "resource_changes": [
            {"type": "aws_cloudwatch_log_group", "change": {"actions": ["create"], "after": {}}},
            {"type": "aws_cloudwatch_log_group", "change": {"actions": ["create"], "after": {}}},
        ]
    }
    assert cloudwatch_log_group_meta.count(plan) == 2


def test_count_groups_none():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert cloudwatch_log_group_meta.count(plan) == 0
