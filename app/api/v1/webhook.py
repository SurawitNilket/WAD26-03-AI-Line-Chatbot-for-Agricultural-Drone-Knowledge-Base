"""
LINE Webhook Endpoint.
Receives webhook events from LINE Messaging API, validates signatures,
and delegates processing to the Dispatcher.
"""
from fastapi import APIRouter, Request, Header, HTTPException, BackgroundTasks
from linebot.v3.webhook import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from app.config import settings
from app.core.dispatcher import dispatcher

router = APIRouter()

@router.post("/webhook")
async def line_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(None, alias="X-Line-Signature")
):
    body = (await request.body()).decode("utf-8")
    secret = settings.LINE_CHANNEL_SECRET.strip()

    # In development with dummy keys, allow testing if signature is dummy or omitted
    if secret == "dummy_line_channel_secret" and not x_line_signature:
        return {"status": "debug_mode_ok"}

    if not x_line_signature:
        print("[Webhook Error] Missing X-Line-Signature header in request!")
        raise HTTPException(status_code=400, detail="Missing X-Line-Signature header")

    parser = WebhookParser(secret)
    try:
        events = parser.parse(body, x_line_signature)
    except InvalidSignatureError:
        masked_secret = f"{secret[:4]}...{secret[-4:]}" if len(secret) > 8 else "***"
        print(f"[Webhook Error] Invalid Signature Verification!")
        print(f"  -> Secret length: {len(secret)} (Masked: {masked_secret})")
        print(f"  -> Signature received: {x_line_signature[:15]}...")
        print(f"  -> Hint: Ensure LINE_CHANNEL_SECRET in .env matches Channel Secret in Basic Settings.")
        raise HTTPException(status_code=400, detail="Invalid signature verification")

    for event in events:
        user_id = getattr(event.source, "user_id", "unknown_user")
        reply_token = getattr(event, "reply_token", None)

        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            user_text = event.message.text
            background_tasks.add_task(
                dispatcher.handle_text_message,
                user_id=user_id,
                reply_token=reply_token,
                text=user_text
            )
        elif isinstance(event, PostbackEvent):
            postback_data = event.postback.data
            background_tasks.add_task(
                dispatcher.handle_postback,
                user_id=user_id,
                reply_token=reply_token,
                postback_data=postback_data
            )

    return {"status": "ok", "events_processed": len(events)}
