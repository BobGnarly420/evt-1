from pydantic import BaseModel, Field


class AssertionIn(BaseModel):
    assertion_id: str
    issuer: str
    subject: str
    claim: dict
    timestamp: str
    signature: str
    public_key: str
    provenance: dict = Field(default_factory=dict)

class VerifyRequest(BaseModel):
    payload: dict
    signature: str
    public_key: str

class VerifyResponse(BaseModel):
    valid: bool
