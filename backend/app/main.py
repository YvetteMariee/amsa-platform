from fastapi import FastAPI, UploadFile, File
import shutil
from pypdf import PdfReader
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

from .core.config import UPLOAD_DIR

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API AMSA active"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "saved": str(file_path)
    }


@app.get("/extract")
def extract_file(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {"error": "file not found", "path": str(file_path)}

    reader = PdfReader(str(file_path))

    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return {
        "filename": filename,
        "chars": len(text),
        "preview": text[:500]
    }


@app.get("/search")
def search_keyword(filename: str, keyword: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {"error": "file not found"}

    reader = PdfReader(str(file_path))

    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    pattern = r"(Article\s+\d+.*?)(?=Article\s+\d+|$)"
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    results = []
    for i, article in enumerate(matches):
        if keyword.lower() in article.lower():
            results.append(article[:800])

    return {
        "count": len(results),
        "results": results[:10]
    }


@app.get("/ask")
def ask(filename: str, question: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {"error": "file not found"}

    if client is None:
        return {"error": "OPENAI_API_KEY missing"}

    reader = PdfReader(str(file_path))

    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"{text}\n\nQuestion: {question}"
            }
        ]
    )

    return {"answer": response.choices[0].message.content}