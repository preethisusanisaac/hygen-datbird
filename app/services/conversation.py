# app/services/conversation.py
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.lead import Lead
from app.services.lead_service import update_lead_state
from app.utils.parsing import parse_budget


def handle_message(db: Session, lead: Lead, text: str) -> str:
    text_lower = text.strip().lower()
    now = datetime.now(timezone.utc)
    lead.last_message_time = now
    lead.last_direction = "INBOUND"

    state = lead.current_state

    # NEW LEAD → ask budget
    if state == "NEW_LEAD":
        reply = (
            "Hi 👋, thanks for your interest in our project. "
            "To help you better, may I know your budget range?"
        )
        update_lead_state(db, lead, state="ASKED_BUDGET")
        return reply

    # ASKED_BUDGET → parse and ask BHK
    if state == "ASKED_BUDGET":
        bmin, bmax = parse_budget(text)
        update_lead_state(
            db,
            lead,
            state="ASKED_BHK",
            budget_min=bmin,
            budget_max=bmax,
        )
        return "Got it 👍\nAre you looking for 2 BHK or 3 BHK?"

    # ASKED_BHK → store and ask location
    if state == "ASKED_BHK":
        update_lead_state(
            db,
            lead,
            state="ASKED_LOCATION",
            bhk_preference=text.strip(),
        )
        return "Nice. Which area are you currently staying in, or where do you prefer?"

    # ASKED_LOCATION → store, qualify, propose visit
    if state == "ASKED_LOCATION":
        update_lead_state(
            db,
            lead,
            state="PROPOSED_VISIT",
            location_pref=text.strip(),
            status="QUALIFIED",
            visit_interested=True,
        )
        return (
            "Based on what you shared, this project looks like a strong match for you. "
            "Would you like to visit the property in person?"
        )

    # PROPOSED_VISIT → if yes, ask slot
    if state == "PROPOSED_VISIT":
        if any(word in text_lower for word in ["yes", "ok", "sure", "ya", "yeah"]):
            update_lead_state(db, lead, state="ASKED_VISIT_SLOT")
            return "Great! We have visit slots at 11 AM and 4 PM tomorrow. Which works for you?"

        # If they say no / later
        if any(word in text_lower for word in ["no", "not now", "later"]):
            update_lead_state(db, lead, status="QUALIFIED")
            return "No worries. I’ll keep you updated with offers and availability. You can message anytime if you’d like to schedule a visit."

        # Neutral / unclear → gently reprompt
        return "If you’d like, I can help you schedule a quick site visit. Shall I share available time slots?"

    # ASKED_VISIT_SLOT → confirm slot
    if state == "ASKED_VISIT_SLOT":
        slot = "11 AM" if "11" in text_lower else "4 PM" if "4" in text_lower else text.strip()
        # For MVP, assume visit tomorrow; you can improve later
        from datetime import date, timedelta

        visit_date = date.today() + timedelta(days=1)
        update_lead_state(
            db,
            lead,
            state="VISIT_CONFIRMED",
            status="VISIT_BOOKED",
            visit_slot=slot,
            visit_date=visit_date,
        )
        # TODO: trigger notification to sales here
        return (
            f"Done ✅ Your site visit is confirmed for {visit_date.strftime('%d %b')} at {slot}. "
            "Our team will connect with you before the visit with directions."
        )

    # Default fallback
    return "Thank you for your message. Our team will review this and get back to you shortly."
