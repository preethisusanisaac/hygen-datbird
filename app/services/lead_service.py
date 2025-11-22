# app/services/lead_service.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.lead import Lead
from app.config import settings
from datetime import datetime, timezone


def get_or_create_lead(db: Session, wa_phone: str, project_id: Optional[int] = None) -> Lead:
    if project_id is None:
        project_id = settings.DEFAULT_PROJECT_ID

    stmt = select(Lead).where(Lead.project_id == project_id, Lead.wa_phone == wa_phone)
    lead = db.execute(stmt).scalar_one_or_none()

    if lead:
        return lead

    lead = Lead(
        project_id=project_id,
        wa_phone=wa_phone,
        current_state="NEW_LEAD",
        status="NEW",
        last_message_time=datetime.now(timezone.utc),
        last_direction="INBOUND",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def update_lead_state(
    db: Session,
    lead: Lead,
    *,
    state: Optional[str] = None,
    status: Optional[str] = None,
    **fields,
) -> Lead:
    if state:
        lead.current_state = state
    if status:
        lead.status = status

    for k, v in fields.items():
        setattr(lead, k, v)

    from datetime import datetime, timezone

    lead.updated_at = datetime.now(timezone.utc)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
