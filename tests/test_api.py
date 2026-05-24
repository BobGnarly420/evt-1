from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200

def test_product_create_and_fetch():
    payload = {
      "schema_version": "evt1.v1", "canonical_name": "Sony WH-1000XM6", "manufacturer": "Sony", "category": "headphones", "model": "WH1000XM6", "variant": "Black",
      "identity_metadata": {}, "trust_scores": {"identity_confidence": 0.95, "counterfeit_risk": 0.1, "vendor_reliability": 0.9}, "provenance": {}, "signatures": {}
    }
    c = client.post('/product', json=payload)
    assert c.status_code == 200
    pid = c.json()["product_id"]
    g = client.get(f'/product/{pid}')
    assert g.status_code == 200
