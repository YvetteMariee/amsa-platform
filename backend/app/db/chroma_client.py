import chromadb
from app.core.config import CHROMA_DIR
import os

os.makedirs(CHROMA_DIR, exist_ok=True)

client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = client.get_or_create_collection(
    name="documents"
)