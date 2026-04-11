from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 

# 🔗 Config
QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_openai = OpenAI(api_key=OPENAI_API_KEY)

# 1. Load PDF
loader = PyPDFLoader("data/clinqodata.pdf")
docs = loader.load()

# 2. Chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)

texts = [chunk.page_content for chunk in chunks]

# 3. Create embeddings using OpenAI
def get_embedding(text):
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

vectors = [get_embedding(t) for t in texts]

# 4. Connect Qdrant
client = QdrantClient(
    host=QDRANT_URL,
    port=443,
    https=True,
    timeout=60
)

# 5. Create collection (IMPORTANT: size = 1536)
client.recreate_collection(
    collection_name="clinqo",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# 6. Upload
points = [
    PointStruct(
        id=i,
        vector=vectors[i],
        payload={"text": texts[i]}
    )
    for i in range(len(texts))
]

client.upsert(collection_name="clinqo", points=points)

print("✅ Uploaded with OpenAI embeddings")