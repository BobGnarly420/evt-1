import json
from pathlib import Path
from app.db.session import SessionLocal
from app.schemas.product import ProductIn
from app.models.product import Product
from app.services.canonicalization import canonicalize

if __name__ == "__main__":
    db = SessionLocal()
    data = json.loads(Path("app/data/sample_products.json").read_text())
    for row in data:
        body = ProductIn(**row)
        pid, conf, explain = canonicalize(body.manufacturer, body.model, body.variant)
        exists = db.query(Product).filter_by(product_id=pid).first()
        if exists:
            continue
        db.add(Product(schema_version=body.schema_version, product_id=pid, canonical_name=body.canonical_name, manufacturer=body.manufacturer, category=body.category, identity_metadata={**body.identity_metadata, "canonicalization": explain}, identity_confidence=max(body.trust_scores.identity_confidence, conf), counterfeit_risk=body.trust_scores.counterfeit_risk, vendor_reliability=body.trust_scores.vendor_reliability, repairability=body.trust_scores.repairability, claim_verifiability=body.trust_scores.claim_verifiability, return_friction=body.trust_scores.return_friction, provenance=body.provenance, signatures=body.signatures))
    db.commit(); db.close()
    print("seed complete")
