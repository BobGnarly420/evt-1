from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Assertion(Base):
    __tablename__ = "assertions"
    id: Mapped[int] = mapped_column(primary_key=True)
    assertion_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    issuer: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(255), index=True)
    claim: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[str] = mapped_column(String(64))
    signature: Mapped[str] = mapped_column(String(255))
    public_key: Mapped[str] = mapped_column(String(255))
    provenance: Mapped[dict] = mapped_column(JSON, default=dict)
