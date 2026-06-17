import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")
CHROMA_DIR = os.getenv("CHROMA_DIR", "data/chroma")
