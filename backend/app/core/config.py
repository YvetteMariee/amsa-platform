from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # ajuste selon ton arborescence
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)