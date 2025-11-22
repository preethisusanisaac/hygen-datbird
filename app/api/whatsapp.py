# app/api/whatsapp.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
import httpx
import logging

from app.config import settings
from app.models.db import get_db
from app.services.lead_service import get_or_create_lead
from app.services.conversation import handle_message

router = APIRouter()


@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: str,
    hub_challenge: str,
    hub_verify_token: str,
):
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def receive_whatsapp(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    logging.info("Incoming WA payload: %s", payload)

    try:
        entry = payload["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages", [])
        if not messages:
            return {"status": "no_messages"}

        message = messages[0]
        wa_phone = message["from"]  # sender phone (string)
        msg_type = message["type"]

        if msg_type != "text":
            # For MVP: ignore non-text, or send generic reply
            text = "[non-text message]"
        else:
            text = message["text"]["body"]

    except Exception as e:
        logging.exception("Failed to parse WA payload: %s", e)
        raise HTTPException(status_code=400, detail="Invalid WA payload")

    # Find or create lead
    lead = get_or_create_lead(db, wa_phone=wa_phone)

    # Get reply from conversation engine
    reply_text = handle_message(db, lead, text)

    # Send reply via WA Cloud API
    await send_whatsapp_text(wa_phone, reply_text)

    return {"status": "ok"}


async def send_whatsapp_text(to_phone: str, message: str):
    url = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message},
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, json=data, headers=headers)
        if resp.status_code >= 400:
            logging.error("Error sending WA message: %s %s", resp.status_code, resp.text)
