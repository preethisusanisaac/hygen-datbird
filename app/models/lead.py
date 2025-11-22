# app/models/lead.py
from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    DateTime,
    Date,
    Boolean,
    Numeric,
    ForeignKey,
    func,
)
from app.models.db import Base


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = {"schema": "hygen_re"}
    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("hygen_re.projects.id", ondelete="CASCADE"), nullable=False)
    wa_phone = Column(Text, nullable=False)
    name = Column(Text)
    budget_min = Column(Numeric)
    budget_max = Column(Numeric)
    bhk_preference = Column(Text)
    location_pref = Column(Text)
    timeline = Column(Text)
    current_state = Column(Text, nullable=False)
    visit_interested = Column(Boolean, nullable=False, server_default="false")
    visit_date = Column(Date)
    visit_slot = Column(Text)
    last_message_time = Column(DateTime(timezone=True))
    last_direction = Column(Text)
    status = Column(Text, nullable=False, server_default="NEW")
    conversation_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
