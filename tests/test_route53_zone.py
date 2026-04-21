# tests/test_route53_zone.py

from resources.route53_zone import route53_zone_meta


def test_extract_route53_zone():
    plan = {
        "resource_changes": [
            {
                "type": "aws_route53_zone",
                "change": {
                    "actions": ["create"],
                    "after": {"name": "example.com", "zone_id": "Z1234567890"},
                },
            }
        ]
    }
    result = route53_zone_meta.extract_route53_zone(plan)
    assert len(result) == 1
    assert result[0]["name"] == "example.com"


def test_extract_route53_zone_no_zones():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    result = route53_zone_meta.extract_route53_zone(plan)
    assert result == []


def test_extract_multiple_zones():
    plan = {
        "resource_changes": [
            {"type": "aws_route53_zone", "change": {"actions": ["create"], "after": {"name": "zone1.com"}}},
            {"type": "aws_route53_zone", "change": {"actions": ["create"], "after": {"name": "zone2.com"}}},
        ]
    }
    result = route53_zone_meta.extract_route53_zone(plan)
    assert len(result) == 2


def test_detect_route53_zone_usage():
    plan = {"resource_changes": [{"type": "aws_route53_zone", "change": {"actions": ["create"], "after": {}}}]}
    assert route53_zone_meta.detect_route53_zone_usage(plan) is True


def test_detect_route53_zone_usage_no_zones():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert route53_zone_meta.detect_route53_zone_usage(plan) is False


def test_count_zones():
    plan = {
        "resource_changes": [
            {"type": "aws_route53_zone", "change": {"actions": ["create"], "after": {}}},
            {"type": "aws_route53_zone", "change": {"actions": ["create"], "after": {}}},
        ]
    }
    assert route53_zone_meta.count(plan) == 2


def test_count_zones_none():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert route53_zone_meta.count(plan) == 0
