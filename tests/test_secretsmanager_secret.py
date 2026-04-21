# tests/test_secretsmanager_secret.py

from resources.secretsmanager_secret import secretsmanager_secret_meta


def test_extract_secretsmanager_secret():
    plan = {
        "resource_changes": [
            {
                "type": "aws_secretsmanager_secret",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "name": "my-secret",
                        "arn": "arn:aws:secretsmanager:us-east-1:123456789012:secret:my-secret",
                    },
                },
            }
        ]
    }
    result = secretsmanager_secret_meta.extract_secretsmanager_secret(plan)
    assert len(result) == 1
    assert result[0]["name"] == "my-secret"


def test_extract_secretsmanager_secret_no_secrets():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    result = secretsmanager_secret_meta.extract_secretsmanager_secret(plan)
    assert result == []


def test_extract_multiple_secrets():
    plan = {
        "resource_changes": [
            {
                "type": "aws_secretsmanager_secret",
                "change": {"actions": ["create"], "after": {"name": "secret1"}},
            },
            {
                "type": "aws_secretsmanager_secret",
                "change": {"actions": ["create"], "after": {"name": "secret2"}},
            },
        ]
    }
    result = secretsmanager_secret_meta.extract_secretsmanager_secret(plan)
    assert len(result) == 2


def test_detect_secretsmanager_usage():
    plan = {"resource_changes": [{"type": "aws_secretsmanager_secret", "change": {"actions": ["create"], "after": {}}}]}
    assert secretsmanager_secret_meta.detect_secretsmanager_usage(plan) is True


def test_detect_secretsmanager_usage_no_secrets():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert secretsmanager_secret_meta.detect_secretsmanager_usage(plan) is False


def test_count_secrets():
    plan = {
        "resource_changes": [
            {"type": "aws_secretsmanager_secret", "change": {"actions": ["create"], "after": {}}},
            {"type": "aws_secretsmanager_secret", "change": {"actions": ["create"], "after": {}}},
        ]
    }
    assert secretsmanager_secret_meta.count(plan) == 2


def test_count_secrets_none():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert secretsmanager_secret_meta.count(plan) == 0
