from fastapi import FastAPI, Request
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests

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
                reply = generate_ai_reply(text)
                send_instagram_message(sender_id, reply)
            else:
                print("Non-text message received")

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}

#------------------AI Reply Function----------------------

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_reply(user_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Instagram assistant."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content or ""


#------------------Send Reply to Instagram----------------------

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")

def send_instagram_message(user_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "recipient": {"id": user_id},
        "message": {"text": message_text}
    }

    requests.post(url, headers=headers, json=data)



