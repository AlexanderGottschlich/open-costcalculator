# tests/test_ses_domain_identity.py

from resources.ses_domain_identity import ses_domain_identity_meta


def test_extract_ses_domain_identity():
    plan = {
        "resource_changes": [
            {
                "type": "aws_ses_domain_identity",
                "change": {
                    "actions": ["create"],
                    "after": {"domain": "example.com"},
                },
            }
        ]
    }
    result = ses_domain_identity_meta.extract_ses_domain_identity(plan)
    assert len(result) == 1
    assert result[0]["domain"] == "example.com"


def test_extract_ses_domain_identity_no_identities():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    result = ses_domain_identity_meta.extract_ses_domain_identity(plan)
    assert result == []


def test_extract_multiple_identities():
    plan = {
        "resource_changes": [
            {"type": "aws_ses_domain_identity", "change": {"actions": ["create"], "after": {"domain": "domain1.com"}}},
            {"type": "aws_ses_domain_identity", "change": {"actions": ["create"], "after": {"domain": "domain2.com"}}},
        ]
    }
    result = ses_domain_identity_meta.extract_ses_domain_identity(plan)
    assert len(result) == 2


def test_detect_ses_domain_identity_usage():
    plan = {"resource_changes": [{"type": "aws_ses_domain_identity", "change": {"actions": ["create"], "after": {}}}]}
    assert ses_domain_identity_meta.detect_ses_domain_identity_usage(plan) is True


def test_detect_ses_domain_identity_usage_no_identities():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert ses_domain_identity_meta.detect_ses_domain_identity_usage(plan) is False


def test_count_identities():
    plan = {
        "resource_changes": [
            {"type": "aws_ses_domain_identity", "change": {"actions": ["create"], "after": {}}},
            {"type": "aws_ses_domain_identity", "change": {"actions": ["create"], "after": {}}},
        ]
    }
    assert ses_domain_identity_meta.count(plan) == 2


def test_count_identities_none():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert ses_domain_identity_meta.count(plan) == 0
