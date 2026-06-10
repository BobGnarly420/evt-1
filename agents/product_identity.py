from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator


class ProductIdentity(BaseModel, extra="forbid"):
    """Schema for product identity URN and canonical attributes."""
    id: str = Field(
        ..., description="Product URN: urn:evt:product:{manufacturer}-{model}-{variant}"
    )
    manufacturer: str
    model: str
    variant: str | None = None

    @model_validator(mode="after")
    def validate_urn(self):
        assert self.id.startswith("urn:evt:product:"), "ID must be a product URN"
        return self

class TrustSignal(BaseModel, extra="forbid"):
    """A single trust claim about a product, with provenance and typed value."""
    type: Literal["verified_manufacturer", "test_report", "certificate", "user_rating", "custom"]
    score: float | None = Field(None, ge=0.0, le=1.0, description="Normalized trust score [0,1]")
    source: str | None = Field(None, description="Agent or signer issuing this trust claim")
    url: HttpUrl | None = Field(None, description="Evidence or report URL")
    payload: dict | None = Field(None, description="Custom assertion data or claim blob")

class ProductTrustProfile(BaseModel, extra="forbid"):
    """Agent-first canonical structure for product identity + all trust signals."""
    product: ProductIdentity
    trust_signals: list[TrustSignal] = Field(default_factory=list)
    profile_version: Literal["2024-05"] = "2024-05"
