from pydantic import BaseModel, Field

class TrustScores(BaseModel):
    identity_confidence: float = Field(ge=0, le=1)
    counterfeit_risk: float = Field(ge=0, le=1)
    vendor_reliability: float = Field(ge=0, le=1)
    repairability: float | None = Field(default=None, ge=0, le=1)
    claim_verifiability: float | None = Field(default=None, ge=0, le=1)
    return_friction: float | None = Field(default=None, ge=0, le=1)

class ProductIn(BaseModel):
    schema_version: str = "evt1.v1"
    canonical_name: str
    manufacturer: str
    category: str
    model: str
    variant: str
    identity_metadata: dict = Field(default_factory=dict)
    trust_scores: TrustScores
    provenance: dict = Field(default_factory=dict)
    signatures: dict = Field(default_factory=dict)

class ProductOut(BaseModel):
    schema_version: str
    product_id: str
    canonical_name: str
    manufacturer: str
    category: str
    identity_metadata: dict
    trust_scores: TrustScores
    provenance: dict
    signatures: dict
