import os
import pandas as pd
from app.services.pdf_parser import parse_pdf

UPLOAD_DIR = "app/data/uploads"


def process_all_pdfs():

    all_data = []

    for file in os.listdir(UPLOAD_DIR):

        if file.endswith(".pdf"):

            path = os.path.join(UPLOAD_DIR, file)

            df = parse_pdf(path)

            if not df.empty:
                df["source_file"] = file
                all_data.append(df)

    if all_data:
        return pd.concat(all_data, ignore_index=True)

    return pd.DataFrame()