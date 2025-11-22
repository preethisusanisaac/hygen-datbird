# app/models/builder.py
from sqlalchemy import Column, BigInteger, Text, DateTime, func
from app.models.db import Base


class Builder(Base):
    __tablename__ = "builders"
    __table_args__ = {"schema": "hygen_re"}
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    contact_name = Column(Text)
    contact_phone = Column(Text)
    contact_email = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
