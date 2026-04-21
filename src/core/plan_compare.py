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
    delta_str = f"+${delta:.5f}" if delta >= 0 else f"-${abs(delta):.5f}"
    delta_symbol = "↑" if delta > 0 else "↓" if delta < 0 else "="

    combined_table = []
    max_rows = max(len(plan1_table), len(plan2_table))

    for i in range(max_rows):
        p1 = plan1_table[i] if i < len(plan1_table) else ["", "", "", ""]
        p2 = plan2_table[i] if i < len(plan2_table) else ["", "", "", ""]
        combined_table.append([p1[0], p1[1], p1[2], p1[3], p2[0], p2[1], p2[2], p2[3]])

    print("")
    print("=" * 70)
    print("Cost Comparison")
    print("=" * 70)
    print(
        tabulate(
            combined_table,
            headers=["Komponente", "Anzahl", "Typ", "Kosten", "Komponente", "Anzahl", "Typ", "Kosten"],
            tablefmt="github",
        )
    )
    print("-" * 70)
    print(f"{plan1_name:30} | ${plan1_cost:.5f}")
    print(f"{plan2_name:30} | ${plan2_cost:.5f}")
    print("-" * 70)
    print(f"Delta (Cost Change)       | {delta_symbol} ${abs(delta):.5f}")
    print("=" * 70)
