from sqlalchemy import JSON, Float, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    schema_version: Mapped[str] = mapped_column(String(32))
    product_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    canonical_name: Mapped[str] = mapped_column(String(255), index=True)
    manufacturer: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(255))
    identity_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    identity_confidence: Mapped[float] = mapped_column(Float)
    counterfeit_risk: Mapped[float] = mapped_column(Float)
    vendor_reliability: Mapped[float] = mapped_column(Float)
    repairability: Mapped[float | None] = mapped_column(Float, nullable=True)
    claim_verifiability: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_friction: Mapped[float | None] = mapped_column(Float, nullable=True)
    provenance: Mapped[dict] = mapped_column(JSON, default=dict)
    signatures: Mapped[dict] = mapped_column(JSON, default=dict)

Index("ix_products_product_id", Product.product_id)
