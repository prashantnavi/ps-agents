"""
FastAPI server exposing SendGrid Inbound Parse webhook to capture replies
and auto-respond using the SDR agent.
"""

import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import (
    init_db,
    find_conversation_by_message_ref,
    upsert_conversation,
    insert_message,
    set_conversation_last_message,
)
from email_service import send_html_email
from agents import AgentFactory, Runner


INBOUND_TOKEN = os.environ.get("PARSE_TOKEN", "")

app = FastAPI()


class InboundPayload(BaseModel):
    from_field: str | None = None
    to: str | None = None
    subject: str | None = None
    text: str | None = None
    html: str | None = None
    headers: str | None = None
    InReplyTo: str | None = None
    References: str | None = None
    MessageID: str | None = None


@app.on_event("startup")
def on_startup():
    init_db()


def _parse_address(email_header: str | None) -> str | None:
    if not email_header:
        return None
    # naive parse for address in form "Name <email@domain>"
    if "<" in email_header and ">" in email_header:
        try:
            return email_header.split("<", 1)[1].split(">", 1)[0].strip()
        except Exception:
            return email_header.strip()
    return email_header.strip()


@app.post("/webhooks/sendgrid/inbound")
async def inbound_parse(request: Request):
    token = request.query_params.get("token", "")
    if INBOUND_TOKEN and token != INBOUND_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # SendGrid posts form encoded by default
    form = await request.form()

    payload = InboundPayload(
        from_field=form.get("from"),
        to=form.get("to"),
        subject=form.get("subject"),
        text=form.get("text"),
        html=form.get("html"),
        headers=form.get("headers"),
        InReplyTo=form.get("In-Reply-To") or form.get("in-reply-to") or form.get("InReplyTo"),
        References=form.get("References"),
        MessageID=form.get("Message-ID") or form.get("message-id") or form.get("MessageID"),
    )

    # Idempotency: skip if we've seen this MessageID
    try:
        conv_id = find_conversation_by_message_ref(payload.InReplyTo, _parse_address(payload.from_field))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    if not conv_id:
        conv_id = upsert_conversation(payload.subject or "", _parse_address(payload.from_field) or "")

    # Store inbound message
    headers_json = json.dumps({"raw": payload.headers or ""})
    insert_message(
        conversation_id=conv_id,
        direction="inbound",
        message_id=payload.MessageID,
        in_reply_to=payload.InReplyTo,
        headers=headers_json,
        body_text=payload.text,
        body_html=payload.html,
    )
    set_conversation_last_message(conv_id, payload.MessageID)

    # Guardrails: do not auto-reply to auto-generated emails
    headers_lower = (payload.headers or "").lower()
    if "auto-submitted:" in headers_lower or "x-auto-response-suppress:" in headers_lower:
        return JSONResponse({"status": "ignored", "reason": "auto response detected"})

    # Generate SDR reply using existing agents
    factory = AgentFactory()
    sdr = factory.create_sales_manager(tools=[])  # reasoning agent for reply

    history_text = payload.text or payload.html or ""
    prompt = (
        "You are continuing an email thread with a prospect. Read their last message and craft a short, helpful reply.\n\n"
        f"Prospect message:\n{history_text}\n\n"
        "Respond politely with one clear CTA."
    )
    sdr_reply = await Runner.run(sdr, prompt)
    reply_text = sdr_reply.final_output

    # Simple subject reuse and threading headers
    subject = payload.subject or "Re:"
    in_reply_to = payload.MessageID
    references = payload.References

    # For now send HTML with wrapped <p>
    html_body = f"<p>{reply_text}</p>"
    send_result = send_html_email(html_body, subject, in_reply_to=in_reply_to, references=references)

    # Save outbound
    insert_message(
        conversation_id=conv_id,
        direction="outbound",
        message_id=None,
        in_reply_to=in_reply_to,
        headers=json.dumps({"sent_via": "sendgrid"}),
        body_text=reply_text,
        body_html=html_body,
    )

    return JSONResponse({"status": "ok", "send": send_result})


def run_dev():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


