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
        entry_list = data.get("entry")
        if not entry_list:
            return {"status": "no entry"}

        for entry in entry_list:

            # ===== DMs =====
            messaging_list = entry.get("messaging")
            if messaging_list:
                for msg_event in messaging_list:

                    if msg_event.get("message", {}).get("is_echo"):
                        continue

                    sender_id = msg_event.get("sender", {}).get("id")
                    text = msg_event.get("message", {}).get("text")

                    if not sender_id or not text:
                        continue

                    print(f"User (DM): {text}")

                    reply = await generate_reply(text)
                    send_instagram_message(sender_id, reply)

                    print(f"Bot: {reply}")

            # ===== Comments =====
            elif entry.get("changes"):
                for change in entry.get("changes"):

                    if change.get("field") != "comments":
                        continue

                    value = change.get("value", {})

                    comment_id = value.get("id")
                    text = value.get("text")
                    username = value.get("from", {}).get("username")
                    commenter_id = value.get("from", {}).get("id")
                    if commenter_id == "17841452076255595":
                        continue

                    if not text:
                        continue

                    print(f"{username} (comment): {text}")

                    reply = await generate_reply(text)
                    send_instagram_comment_reply(comment_id, reply)
                    print("Comment ID:", comment_id)

                    print(f"Bot (comment reply): {reply}")

    except Exception as e:
        print("Error:", str(e))

    return {"status": "ok"}

#------------------Send Reply to Instagram----------------------

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

import requests

def send_instagram_message(recipient_id, text):
    url = "https://graph.facebook.com/v19.0/1107771282409772/messages"

    payload = {
        "recipient": {
            "id": recipient_id   # ✅ MUST use this
        },
        "message": {
            "text": text
        }
    }

    params = {
        "access_token": ACCESS_TOKEN  # ✅ Page token only
    }

    print("Sending to:", recipient_id)   # 🔍 debug
    print("Payload:", payload)

    response = requests.post(url, json=payload, params=params)

    print("Send response:", response.text)


#------------------Send comment reply to Instagram----------------------

def send_instagram_comment_reply(comment_id: str, message: str):
    """
    Sends a reply to an Instagram comment using Meta Graph API.

    Args:
        comment_id (str): ID of the Instagram comment
        message (str): Reply text
        
    Returns:
        dict: API response (success or error)
    """

    url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"

    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.post(url, params=params)
        data = response.json()

        if response.status_code == 200:
            print("✅ Reply sent successfully")
        else:
            print("❌ Error:", data)

        return data

    except Exception as e:
        print("⚠️ Exception occurred:", str(e))
        return {"error": str(e)}


