import pandas as pd
from app.db.session import engine

def ingest_dataframe(file_path: str, table_name: str):

    # lecture fichier
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # nettoyage colonnes
    df.columns = [
        c.lower().replace(" ", "_")
        for c in df.columns
    ]

    # insertion PostgreSQL
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    return {
        "table": table_name,
        "rows_inserted": len(df),
        "columns": list(df.columns)
    }