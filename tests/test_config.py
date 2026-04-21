from core.config import DEFAULT_REGION


def test_default_region_is_set():
    assert DEFAULT_REGION == "eu-central-1"


def test_default_region_is_valid_aws_region():
    valid_regions = [
        "eu-central-1",
        "us-east-1",
        "us-west-2",
        "eu-west-1",
    ]
    assert DEFAULT_REGION in valid_regions
