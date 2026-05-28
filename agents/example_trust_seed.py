from agents.product_identity import ProductTrustProfile, ProductIdentity, TrustSignal

profile = ProductTrustProfile(
    product=ProductIdentity(
        id="urn:evt:product:acme-thermometer-plus",
        manufacturer="ACME",
        model="thermometer",
        variant="plus"
    ),
    trust_signals=[
        TrustSignal(
            type="verified_manufacturer",
            score=1.0,
            source="did:web:acme.org"
        ),
        TrustSignal(
            type="user_rating",
            score=0.87,
            source="agent:bob",
            payload={"votes": 42, "avg": 4.4}
        )
    ]
)

# Canonical serialization for signing/verifying (sorted, compact separators)
import json
print(profile.model_dump_json(exclude_none=True, by_alias=True, sort_keys=True, separators=(",", ":")))
