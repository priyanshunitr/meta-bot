from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import requests
from ai_model import generate_reply

load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = FastAPI()

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
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        if "messages" in value:
            message = value["messages"][0]
            sender_id = message.get("from")

            # safer text extraction
            text = message.get("text", {}).get("body")

            if text:
                reply = generate_reply(text)
                send_instagram_message(sender_id, reply)
            else:
                print("Non-text message received")

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}


#------------------Send Reply to Instagram----------------------

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def send_instagram_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"

    params = {
        "access_token": ACCESS_TOKEN
    }

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, params=params, json=payload)
    print("Send response:", response.text)



