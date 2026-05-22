import pandas as pd
from app.db.session import engine

STANDARD_COLUMNS = {
    "instrument": ["instrument", "titre", "title", "security"],
    "prix": ["prix", "price", "px"],
    "volume": ["volume", "vol"],
    "date": ["date", "jour", "day"],
    "compartiment": ["compartiment", "comp", "segment"],
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {}
    for col in df.columns:
        key = str(col).strip().lower()
        found = None
        for standard, variants in STANDARD_COLUMNS.items():
            if key in variants:
                found = standard
                break
        mapping[col] = found or key.replace(" ", "_")
    df = df.rename(columns=mapping)
    return df


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    if "prix" in df.columns:
        df["prix"] = pd.to_numeric(df["prix"].astype(str).str.replace(" ", "").str.replace(",", "."), errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"].astype(str).str.replace(" ", "").str.replace(",", "."), errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    return df


def ingest_dataframe(file_path: str, table_name: str):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    df = _normalize_columns(df)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = _coerce_types(df)
    df["source_file"] = file_path.split("/")[-1]
    df["anomaly_score"] = None

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    return {
        "table": table_name,
        "rows_inserted": len(df),
        "columns": list(df.columns)
    }