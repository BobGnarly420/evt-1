from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Assertion, Product
from app.schemas.assertion import AssertionIn, VerifyRequest, VerifyResponse
from app.schemas.product import ProductIn, ProductOut, TrustScores
from app.services.canonicalization import canonicalize
from app.services.crypto import verify_signature

Base.metadata.create_all(bind=engine)
app = FastAPI(title="EVT-1 API", version="0.1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"name": "evt-1", "status": "ok"}


@app.get("/health")
def health():
    return {"healthy": True}


@app.post("/product", response_model=ProductOut)
def create_product(body: ProductIn, db: Session = Depends(get_db)):
    pid, conf, explain = canonicalize(body.manufacturer, body.model, body.variant)
    p = Product(
        schema_version=body.schema_version,
        product_id=pid,
        canonical_name=body.canonical_name,
        manufacturer=body.manufacturer,
        category=body.category,
        identity_metadata={**body.identity_metadata, "canonicalization": explain},
        identity_confidence=max(body.trust_scores.identity_confidence, conf),
        counterfeit_risk=body.trust_scores.counterfeit_risk,
        vendor_reliability=body.trust_scores.vendor_reliability,
        repairability=body.trust_scores.repairability,
        claim_verifiability=body.trust_scores.claim_verifiability,
        return_friction=body.trust_scores.return_friction,
        provenance=body.provenance,
        signatures=body.signatures,
    )
    db.add(p); db.commit(); db.refresh(p)
    return ProductOut(
        schema_version=p.schema_version, product_id=p.product_id, canonical_name=p.canonical_name,
        manufacturer=p.manufacturer, category=p.category, identity_metadata=p.identity_metadata,
        trust_scores=TrustScores(identity_confidence=p.identity_confidence, counterfeit_risk=p.counterfeit_risk, vendor_reliability=p.vendor_reliability, repairability=p.repairability, claim_verifiability=p.claim_verifiability, return_friction=p.return_friction),
        provenance=p.provenance, signatures=p.signatures
    )

@app.get("/product/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.product_id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut(schema_version=p.schema_version, product_id=p.product_id, canonical_name=p.canonical_name, manufacturer=p.manufacturer, category=p.category, identity_metadata=p.identity_metadata, trust_scores=TrustScores(identity_confidence=p.identity_confidence, counterfeit_risk=p.counterfeit_risk, vendor_reliability=p.vendor_reliability, repairability=p.repairability, claim_verifiability=p.claim_verifiability, return_friction=p.return_friction), provenance=p.provenance, signatures=p.signatures)

@app.get("/resolve")
def resolve(q: str = Query(...), db: Session = Depends(get_db)):
    rows = db.query(Product).filter(Product.canonical_name.ilike(f"%{q}%")).all()
    return [{"product_id": r.product_id, "canonical_name": r.canonical_name} for r in rows]

@app.post("/assert")
def create_assertion(body: AssertionIn, db: Session = Depends(get_db)):
    payload = {"assertion_id": body.assertion_id, "issuer": body.issuer, "subject": body.subject, "claim": body.claim, "timestamp": body.timestamp}
    if not verify_signature(body.public_key, payload, body.signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    a = Assertion(**body.model_dump())
    db.add(a); db.commit(); db.refresh(a)
    return {"stored": True, "assertion_id": a.assertion_id}

@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest):
    return VerifyResponse(valid=verify_signature(req.public_key, req.payload, req.signature))
