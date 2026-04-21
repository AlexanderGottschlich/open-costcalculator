from pathlib import Path
from typing import Any

import yaml


def load_config(path: str = "config.yaml") -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.is_file():
        return {}
    try:
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return {}


def get_default_values(config: dict, resource_type: str) -> dict[str, Any]:
    defaults = config.get("defaults", {})
    return defaults.get(resource_type, {})


def get_override_values(config: dict, resource_id: str) -> dict[str, Any]:
    overrides = config.get("overrides", {})
    return overrides.get(resource_id, {})


def get_resource_config(config: dict, resource_type: str, resource_id: str) -> dict[str, Any]:
    override = get_override_values(config, resource_id)
    if override:
        return override
    return get_default_values(config, resource_type)
