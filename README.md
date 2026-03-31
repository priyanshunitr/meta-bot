# Meta Bot 🤖

Meta Bot is a FastAPI-based backend service designed to act as a webhook for Instagram (Meta) messaging. When a user sends a message to your Instagram account, this bot receives the message, processes it through OpenAI's powerful GPT-4o-mini model, and automatically sends back a helpful, AI-generated reply.

## 🚀 Features

- **FastAPI Backend:** Fast, asynchronous, and easy-to-read Python web framework.
- **Instagram Webhook Authentication:** Implements Meta's challenge-response verification.
- **AI-Powered Replies:** Uses OpenAI's `gpt-4o-mini` to formulate conversational and intelligent responses.
- **Dockerized:** Includes a `Dockerfile` and `docker-compose.yml` for seamless local setup and deployment.

## 🛠️ Prerequisites

- Python 3.11+
- [Docker](https://www.docker.com/) (optional, for containerized running)
- An active [Meta Developer App](https://developers.facebook.com/) configured for Instagram Messaging
- An [OpenAI API Key](https://platform.openai.com/api-keys)

## ⚙️ Environment Variables

Create a `.env` file in the root directory and add the following keys:

```env
VERIFY_TOKEN=your_custom_verify_token_here
OPENAI_API_KEY=your_openai_api_key_here
PAGE_ACCESS_TOKEN=your_meta_page_access_token_here
```

## 💻 How to Run Locally

### Option 1: Using Python & Virtual Environment (Recommended)

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows Git Bash/Linux/Mac
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   The app will run on `http://127.0.0.1:8000`.

### Option 2: Using Docker Compose

1. Ensure Docker Desktop is running.
2. Build and start the container:
   ```bash
   docker compose up --build
   ```
   The app will run on `http://localhost:8000`.

## ☁️ Deployment (e.g., Render, Railway, Heroku)

When deploying to cloud providers like Render, use the following commands:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔗 Endpoints

- `GET /` - Health check. Returns `{"Server": "Running"}`.
- `GET /webhook` - Used by Meta to verify your webhook subscription.
- `POST /webhook` - Receives incoming Instagram messages and handles the AI reply logic.

## 📘 Meta Instagram + Messenger Bot Setup

### 🎯 Objective

Build a backend service that:

- Receives messages from Instagram/Messenger.
- Processes them with AI or custom logic.
- Sends automated replies.

### 1. 🧩 Initial Setup (Meta Developer App)

You should create a Meta app in the Meta Developers portal:

- App type: Business (or equivalent).
- Use cases added:
  - Messenger
  - Instagram Messaging

Key insight:

- Adding a use case is not enough by itself.
- You still need to configure permissions, access tokens, and webhook subscriptions.

### 2. 🔐 Permissions Setup

Messenger permissions:

- `pages_messaging` (required)
- `pages_show_list`
- `pages_manage_metadata`
- `pages_read_engagement` (optional)

Instagram permissions:

- `instagram_business_basic`
- `instagram_manage_comments`
- `instagram_business_manage_messages`

App review clarification:

- You may see: "Complete App Review required".
- App review is not required for your own testing in Development mode.
- App review is required for public users in Production mode.

| Mode                                  | App Review Needed |
| ------------------------------------- | ----------------- |
| Development (only app admins/testers) | No                |
| Production (public users)             | Yes               |

### 3. 🔗 Account Linking

Required setup:

- Instagram account must be Business or Creator.
- Instagram account must be linked to a Facebook Page.

Common issue if not linked:

- Access token appears valid but fails for messaging.
- Messages do not trigger webhook flows as expected.

### 4. 🔑 Access Token Generation

Steps:

1. Open Instagram setup in Meta app dashboard.
2. Select the Instagram account.
3. Click Generate Token.

### 5. 🌐 Webhook Setup

Configuration:

- Callback URL: your deployed backend URL (for example, Render).
- Verify token: your custom `VERIFY_TOKEN`.
- Subscribed fields:
  - `messages`
  - `messaging_postbacks`

Verification signal:

- Logs show `POST /webhook 200 OK`.

Meaning:

- Meta can reach your backend.
- Webhook configuration is valid.

### 6. 🖥️ Backend Setup (FastAPI)

Webhook endpoint example:

```python
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Incoming:", data)
```

Debugging tip:

```python
print(json.dumps(data, indent=2))
```

This is similar to `console.log` formatting in JavaScript.

### 7. 📩 Incoming Message Formats (Critical)

Meta can send multiple payload formats. Support both patterns.

Format 1 (`entry[].messaging[]`):

```json
{
  "entry": [
    {
      "messaging": [
        {
          "sender": { "id": "USER_ID" },
          "message": { "text": "hi" }
        }
      ]
    }
  ]
}
```

Format 2 (`entry[].changes[].value.messages[]`):

```json
{
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "USER_ID",
                "text": { "body": "hi" }
              }
            ]
          }
        }
      ]
    }
  ]
}
```
