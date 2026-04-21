# core/plan_compare.py

import json


def load_plan(path):
    with open(path) as f:
        return json.load(f)


def get_resource_types(plan):
    return set(res.get("type") for res in plan.get("resource_changes", []))


def compare_plans(before_path, after_path):
    before_plan = load_plan(before_path)
    after_plan = load_plan(after_path)

    before_types = get_resource_types(before_plan)
    after_types = get_resource_types(after_plan)

    added = after_types - before_types
    removed = before_types - after_types
    unchanged = before_types & after_types

    return {
        "added": sorted(added),
        "removed": sorted(removed),
        "unchanged": sorted(unchanged),
    }


def format_comparison(comparison):
    lines = []
    lines.append("=== Terraform Plan Comparison ===")
    lines.append("")

    if comparison["added"]:
        lines.append(f"Added ({len(comparison['added'])}):")
        for res in comparison["added"]:
            lines.append(f"  + {res}")

    if comparison["removed"]:
        lines.append("")
        lines.append(f"Removed ({len(comparison['removed'])}):")
        for res in comparison["removed"]:
            lines.append(f"  - {res}")

    if comparison["unchanged"]:
        lines.append("")
        lines.append(f"Unchanged ({len(comparison['unchanged'])}):")
        for res in comparison["unchanged"]:
            lines.append(f"  = {res}")

    return "\n".join(lines)
