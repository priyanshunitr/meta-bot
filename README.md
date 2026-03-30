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
