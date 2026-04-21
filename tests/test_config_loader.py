import os
import tempfile

from core.config_loader import (get_default_values, get_override_values,
                                get_resource_config, load_config)


def test_load_config_file_not_found():
    result = load_config("nonexistent.yaml")
    assert result == {}


def test_load_config_valid_yaml():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("defaults:\n  s3:\n    estimated_storage_gb: 100\n")
        f.flush()
        try:
            result = load_config(f.name)
            assert result == {"defaults": {"s3": {"estimated_storage_gb": 100}}}
        finally:
            os.unlink(f.name)


def test_load_config_invalid_yaml():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("invalid: yaml: content:")
        f.flush()
        try:
            result = load_config(f.name)
            assert result == {}
        finally:
            os.unlink(f.name)


def test_get_default_values():
    config = {
        "defaults": {
            "s3": {"estimated_storage_gb": 100},
            "sqs": {"estimated_requests": 50000},
        }
    }
    result = get_default_values(config, "s3")
    assert result == {"estimated_storage_gb": 100}

    result = get_default_values(config, "unknown")
    assert result == {}


def test_get_override_values():
    config = {
        "overrides": {
            "aws_s3_bucket.data_bucket": {"estimated_storage_gb": 500},
        }
    }
    result = get_override_values(config, "aws_s3_bucket.data_bucket")
    assert result == {"estimated_storage_gb": 500}

    result = get_override_values(config, "unknown")
    assert result == {}


def test_get_resource_config_prefers_override():
    config = {
        "defaults": {"s3": {"estimated_storage_gb": 100}},
        "overrides": {"aws_s3_bucket.data_bucket": {"estimated_storage_gb": 500}},
    }
    result = get_resource_config(config, "s3", "aws_s3_bucket.data_bucket")
    assert result == {"estimated_storage_gb": 500}


def test_get_resource_config_falls_back_to_default():
    config = {
        "defaults": {"s3": {"estimated_storage_gb": 100}},
    }
    result = get_resource_config(config, "s3", "aws_s3_bucket.unknown")
    assert result == {"estimated_storage_gb": 100}


def test_get_resource_config_empty_config():
    config = {}
    result = get_resource_config(config, "s3", "aws_s3_bucket.data_bucket")
    assert result == {}
