# core/group_by/tags.py


TAG_KEYS = ["project", "team", "environment", "cost_center", "owner"]


def extract_tags(resource):
    tags = {}
    change = resource.get("change", {})
    after = change.get("after", {})
    if after:
        tags_data = after.get("tags", {})
        if tags_data:
            for key in TAG_KEYS:
                if key in tags_data:
                    tags[key] = tags_data[key]
    return tags


def extract_all_resource_tags(plan):
    tagged_resources = []
    for res in plan.get("resource_changes", []):
        res_type = res.get("type", "")
        if res_type.startswith("aws_"):
            tags = extract_tags(res)
            if tags:
                tagged_resources.append(
                    {
                        "type": res_type,
                        "address": res.get("address", ""),
                        "tags": tags,
                    }
                )
    return tagged_resources


def group_by_key(all_tags, key):
    groups = {}
    for res in all_tags:
        tag_value = res["tags"].get(key, "untagged")
        if tag_value not in groups:
            groups[tag_value] = []
        groups[tag_value].append(res)
    return groups


def get_available_tags(all_tags):
    available = set()
    for res in all_tags:
        available.update(res["tags"].keys())
    return list(available)
