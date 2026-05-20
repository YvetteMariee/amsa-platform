import requests

BASE_URL = "http://127.0.0.1:8000"


def upload_file(file):
    files = {"file": file}
    return requests.post(f"{BASE_URL}/upload", files=files)


def search(filename, keyword):
    return requests.get(
        f"{BASE_URL}/search",
        params={"filename": filename, "keyword": keyword}
    )


def ask(filename, question):
    return requests.get(
        f"{BASE_URL}/ask",
        params={"filename": filename, "question": question}
    )