from core.config import get_region_display_name


def build(instance_type, region, marketoption="OnDemand"):
    region_display = get_region_display_name(region)
    return [
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region_display},
        {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
        {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
        {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
        {"Type": "TERM_MATCH", "Field": "marketoption", "Value": marketoption},
        {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
    ]
