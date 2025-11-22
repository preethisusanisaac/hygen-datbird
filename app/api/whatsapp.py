# app/api/whatsapp.py
from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
import httpx
import logging

from app.config import settings
from app.models.db import get_db
from app.services.lead_service import get_or_create_lead
from app.services.conversation import handle_message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def receive_whatsapp(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    logger.info("=" * 80)
    logger.info("📨 INCOMING WHATSAPP MESSAGE")
    logger.info("=" * 80)
    logger.info("Full payload: %s", payload)

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
            logger.info("⚠️  Non-text message from %s (type: %s)", wa_phone, msg_type)
        else:
            text = message["text"]["body"]
            logger.info("📱 From: %s", wa_phone)
            logger.info("💬 Message: %s", text)

    except Exception as e:
        logger.exception("❌ Failed to parse WA payload: %s", e)
        raise HTTPException(status_code=400, detail="Invalid WA payload")

    # Find or create lead
    logger.info("🔍 Finding or creating lead for phone: %s", wa_phone)
    lead = get_or_create_lead(db, wa_phone=wa_phone)
    logger.info("✅ Lead ID: %s (Status: %s)", lead.id, lead.status)

    # Get reply from conversation engine
    logger.info("🤖 Processing message through conversation engine...")
    reply_text = handle_message(db, lead, text)
    logger.info("💭 Reply: %s", reply_text)

    # Send reply via WA Cloud API
    logger.info("📤 Sending reply to %s...", wa_phone)
    await send_whatsapp_text(wa_phone, reply_text)
    logger.info("✅ Reply sent successfully")
    logger.info("=" * 80)

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
            logger.error("❌ Error sending WA message: %s %s", resp.status_code, resp.text)
        else:
            logger.info("✅ WhatsApp API response: %s", resp.status_code)
