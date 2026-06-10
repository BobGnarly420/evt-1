import json

from agents.product_identity import ProductIdentity, ProductTrustProfile, TrustSignal

profile = ProductTrustProfile(
    product=ProductIdentity(
        id="urn:evt:product:acme-thermometer-plus",
        manufacturer="ACME",
        model="thermometer",
        variant="plus",
    ),
    trust_signals=[
        TrustSignal(type="verified_manufacturer", score=1.0, source="did:web:acme.org"),
        TrustSignal(
            type="user_rating",
            score=0.87,
            source="agent:bob",
            payload={"votes": 42, "avg": 4.4},
        ),
    ],
)

# Canonical serialization for signing/verifying (sorted keys, compact separators)
print(
    json.dumps(
        profile.model_dump(mode="json", exclude_none=True),
        sort_keys=True,
        separators=(",", ":"),
    )
)
