# app/models/project.py
from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey, JSON, func
from app.models.db import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "hygen_re"}
    id = Column(BigInteger, primary_key=True, index=True)
    builder_id = Column(BigInteger, ForeignKey("builders.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    project_type = Column(Text, nullable=False)  # 'plot','flat','villa', etc.
    location = Column(Text)
    price_range = Column(Text)
    bhk_options = Column(Text)  # comma-separated for MVP1
    possession_date = Column(Text)
    amenities = Column(JSON)
    wa_entry_number = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
