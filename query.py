from qdrant_client import QdrantClient
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_openai = OpenAI(api_key=OPENAI_API_KEY)
client = QdrantClient(
    host=QDRANT_URL,
    port=443,
    https=True,
    timeout=60
)

def get_embedding(text):
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def get_context(query):
    query_vector = get_embedding(query)

    results = client.query_points(
        collection_name="clinqo",
        query=query_vector,
        limit=3
    )
    
    all_texts = []
    
    for r in results.points:
        point = r[0] if isinstance(r, tuple) else r
        all_texts.append(point.payload.get("text", "")[:300])
    
    combined_context = "\n".join(all_texts)
    return combined_context