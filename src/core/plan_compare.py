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

    rows = []
    max_rows = max(len(plan1_table), len(plan2_table))
    for i in range(max_rows):
        p1 = plan1_table[i] if i < len(plan1_table) else ["", "", "", ""]
        p2 = plan2_table[i] if i < len(plan2_table) else ["", "", "", ""]
        rows.append([f"{p1[0]:<18} {p1[1]}x {p1[2]:<14} ${p1[3].replace('$', ''):<10}", f"{p2[0]:<18} {p2[1]}x {p2[2]:<14} ${p2[3].replace('$', ''):<10}"])

    print("")
    print("=" * 70)
    print("Cost Comparison".center(70))
    print("=" * 70)
    print(f"{'Plan 1':^35}{'Plan 2':^35}")
    print("-" * 70)
    print(tabulate(rows, tablefmt="plain"))
    print("-" * 70)
    print(f"{'Gesamtkosten':<25} ${plan1_cost:<15}{'Gesamtkosten':<25} ${plan2_cost:<15}")
    print("=" * 70)
    print(f"Delta (Cost Change): {delta_symbol} ${abs(delta):.5f}")
    print("=" * 70)
