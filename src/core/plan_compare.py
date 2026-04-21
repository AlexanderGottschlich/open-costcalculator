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

    def format_row(row):
        if not row or not row[0]:
            return ""
        name = row[0]
        count = row[1] if len(row) > 1 and row[1] else ""
        typ = row[2] if len(row) > 2 and row[2] else ""
        cost = row[3].replace("$", "") if len(row) > 3 and row[3] else ""
        return f"{name:<20} {count}x {typ:<14} ${cost:>10}"

    rows = []
    rows.append([plan1_name, plan2_name])
    rows.append(["", ""])
    rows.append(["Komponente:", "Komponente:"])

    max_rows = max(len(plan1_table), len(plan2_table))
    for i in range(max_rows):
        p1 = plan1_table[i] if i < len(plan1_table) else None
        p2 = plan2_table[i] if i < len(plan2_table) else None
        rows.append([format_row(p1), format_row(p2)])

    rows.append([f"Gesamtkosten ${plan1_cost:.5f}", f"Gesamtkosten ${plan2_cost:.5f}"])

    print("")
    print("=" * 92)
    print("Cost Comparison")
    print("=" * 92)
    print(tabulate(rows, tablefmt="grid"))

    print("=" * 92)
    print(f"Delta (Cost Change): {delta_symbol} ${abs(delta):.5f}")
    print("=" * 92)
