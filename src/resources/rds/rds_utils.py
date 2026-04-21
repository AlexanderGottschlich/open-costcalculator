# filter/rds_utils.py

import json

from core import logger


def get_rds_storage_price(pricing_client, storage_type, region):
    """
    Fragt dynamisch den Preis für RDS-Storage anhand des volumeType ab.
    Beispiel: gp3, io1, standard
    """
    try:
        filters = [
            {"Type": "TERM_MATCH", "Field": "volumeType", "Value": storage_type},
            {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        ]
        response = pricing_client.get_products(ServiceCode="AmazonRDS", Filters=filters, MaxResults=1)
        for item in response.get("PriceList", []):
            offer = json.loads(item)
            terms = offer.get("terms", {}).get("OnDemand", {})
            for term in terms.values():
                for dim in term.get("priceDimensions", {}).values():
                    return float(dim.get("pricePerUnit", {}).get("USD", 0.115))
    except Exception as e:
        logger.warn(f"Fehler bei RDS Storage-Preisabfrage: {e}")
    return 0.115
