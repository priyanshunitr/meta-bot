from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
from ai_model import generate_reply

load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = FastAPI()


class SendMessageRequest(BaseModel):
    recipient_id: str
    message_text: str

@app.get("/")
def read_root():
    return {"Server": "Running"}

#------------------Verify Webhook----------------------
@app.get("/webhook")
async def verify(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    if hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return "error"

#--------------Receive Instagram Messages-------------------

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Incoming:", data)

    try:
        # Step 1: Check entry exists
        entry_list = data.get("entry")
        if not entry_list:
            return {"status": "no entry"}

        entry = entry_list[0]

        # Step 2: Check messaging exists
        messaging_list = entry.get("messaging")
        if not messaging_list:
            return {"status": "no messaging"}

        msg_event = messaging_list[0]

        # Step 3: Extract message safely
        sender_id = msg_event.get("sender", {}).get("id")
        message = msg_event.get("message", {})
        text = message.get("text")

        if not sender_id:
            return {"status": "no sender"}

        if text:
            print(f"User: {text}")

            reply = await generate_reply(text)
            send_instagram_message(sender_id, reply)
            print("Sender ID:", sender_id)

            print(f"Bot: {reply}")

        else:
            print("Non-text message received")

    except Exception as e:
        print("Error:", str(e))

    return {"status": "ok"}

#------------------Send Reply to Instagram----------------------

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def send_instagram_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/17841448023461323/messages"

    params = {
        "access_token": ACCESS_TOKEN
    }

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, params=params, json=payload)
    print("Send response:", response.text)

@app.post("/send_message")
async def send_message_endpoint(payload: SendMessageRequest):
    send_instagram_message(payload.recipient_id, payload.message_text)
    return {"status": "message sent"}


