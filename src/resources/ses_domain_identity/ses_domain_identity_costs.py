# resources/ses_domain_identity/ses_domain_identity_costs.py

from resources.ses_domain_identity import ses_domain_identity_meta


def process_ses_domain_identity(plan):
    identities = ses_domain_identity_meta.extract_ses_domain_identity(plan)
    if not identities:
        return [], 0.0

    identity_count = len(identities)

    return [
        [
            "SES Domain Identity",
            identity_count,
            "Domain",
            "$0.00",
        ]
    ], 0.0
