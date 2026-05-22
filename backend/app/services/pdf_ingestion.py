import os
import pandas as pd
from app.services.pdf_parser import parse_pdf
from app.db.session import engine

UPLOAD_DIR = "app/data/uploads"


def process_all_pdfs():
    all_data = []

    for file in os.listdir(UPLOAD_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(UPLOAD_DIR, file)
        df = parse_pdf(path)

        if not df.empty:
            df["source_file"] = file
            all_data.append(df)

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        result.to_sql("market_data", engine, if_exists="append", index=False)
        return result

    return pd.DataFrame()