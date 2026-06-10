from fastapi.testclient import TestClient

from app.main import app
from app.services.crypto import generate_keypair, sign_payload

client = TestClient(app)


def product_payload(variant: str = "Black") -> dict:
    return {
        "schema_version": "evt1.v1",
        "canonical_name": "Sony WH-1000XM6",
        "manufacturer": "Sony",
        "category": "headphones",
        "model": "WH1000XM6",
        "variant": variant,
        "identity_metadata": {},
        "trust_scores": {
            "identity_confidence": 0.95,
            "counterfeit_risk": 0.1,
            "vendor_reliability": 0.9,
        },
        "provenance": {},
        "signatures": {},
    }


def test_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_product_create_and_fetch():
    c = client.post("/product", json=product_payload())
    assert c.status_code == 200
    pid = c.json()["product_id"]
    assert pid == "urn:evt:product:sony-wh1000xm6-black"
    g = client.get(f"/product/{pid}")
    assert g.status_code == 200


def test_duplicate_product_returns_conflict():
    client.post("/product", json=product_payload(variant="Silver"))
    dup = client.post("/product", json=product_payload(variant="Silver"))
    assert dup.status_code == 409


def test_product_not_found():
    r = client.get("/product/urn:evt:product:does-not-exist")
    assert r.status_code == 404


def test_resolve():
    client.post("/product", json=product_payload(variant="Midnight"))
    r = client.get("/resolve", params={"q": "Sony"})
    assert r.status_code == 200
    assert any(row["product_id"].startswith("urn:evt:product:sony-") for row in r.json())


def test_assert_and_verify_roundtrip():
    sk, pk = generate_keypair()
    payload = {
        "assertion_id": "a-test-1",
        "issuer": "validator:test",
        "subject": "urn:evt:product:sony-wh1000xm6-black",
        "claim": {"repairability": 0.81},
        "timestamp": "2026-01-01T00:00:00Z",
    }
    sig = sign_payload(sk, payload)
    body = {**payload, "signature": sig, "public_key": pk, "provenance": {}}
    r = client.post("/assert", json=body)
    assert r.status_code == 200
    assert r.json() == {"stored": True, "assertion_id": "a-test-1"}

    dup = client.post("/assert", json=body)
    assert dup.status_code == 409

    v = client.post("/verify", json={"payload": payload, "signature": sig, "public_key": pk})
    assert v.status_code == 200
    assert v.json() == {"valid": True}


def test_assert_rejects_bad_signature():
    _, pk = generate_keypair()
    payload = {
        "assertion_id": "a-test-2",
        "issuer": "validator:test",
        "subject": "urn:evt:product:sony-wh1000xm6-black",
        "claim": {"repairability": 0.5},
        "timestamp": "2026-01-01T00:00:00Z",
    }
    body = {**payload, "signature": "aW52YWxpZA==", "public_key": pk, "provenance": {}}
    r = client.post("/assert", json=body)
    assert r.status_code == 400
