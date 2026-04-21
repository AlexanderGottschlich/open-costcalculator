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

    return added, removed


def print_cost_comparison(plan1_name, plan1_table, plan1_cost, plan2_name, plan2_table, plan2_cost):
    from tabulate import tabulate

    delta = plan2_cost - plan1_cost
    delta_symbol = "↑" if delta > 0 else "↓" if delta < 0 else "="

    def format_plan_table(name, table):
        lines = []
        lines.append(f"{name}")
        lines.append("")
        lines.append("Komponente:")
        for row in table:
            lines.append(f"{row[0]:20} {row[1]}x {row[2]:15} ${row[3].replace('$', ''):>12}")
        return lines

    print("")
    print("=" * 80)
    print("Cost Comparison")
    print("=" * 80)

    plan1_lines = format_plan_table(plan1_name, plan1_table)
    plan2_lines = format_plan_table(plan2_name, plan2_table)
    max_lines = max(len(plan1_lines), len(plan2_lines))

    combined = []
    for i in range(max_lines):
        p1 = plan1_lines[i] if i < len(plan1_lines) else ""
        p2 = plan2_lines[i] if i < len(plan2_lines) else ""
        combined.append([p1, p2])

    print(tabulate(combined, tablefmt="plain"))

    print("-" * 80)
    header_len = max(len(plan1_name), len(plan2_name), 6)
    print(
        tabulate(
            [[f"{plan1_name:<{header_len}}", f"${plan1_cost:.5f}", f"{plan2_name:<{header_len}}", f"${plan2_cost:.5f}"]],
            tablefmt="grid",
        )
    )
    print("-" * 80)
    print(f"Delta (Cost Change)       | {delta_symbol} ${abs(delta):.5f}")
    print("=" * 80)
