import os
from typing import Optional

import camelot
import pandas as pd


def _map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and map common synonyms to standard names."""
    col_map = {}
    for c in df.columns:
        c0 = str(c).strip().lower()
        if c0 in ("instrument", "titre", "title", "security"):
            col_map[c] = "instrument"
        elif c0 in ("prix", "price", "px"):
            col_map[c] = "prix"
        elif c0 in ("volume", "vol"):
            col_map[c] = "volume"
        elif c0 in ("date", "jour", "day"):
            col_map[c] = "date"
        elif c0 in ("compartiment", "comp", "segment"):
            col_map[c] = "compartiment"
        else:
            # keep original name trimmed
            col_map[c] = c0
    return df.rename(columns=col_map)


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Drop fully empty rows and columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def parse_pdf(file_path: str, pages: Optional[str] = "all") -> pd.DataFrame:
    """Parse a PDF using Camelot and return a normalized DataFrame.

    Steps:
    - Try Camelot with 'lattice' then fallback to 'stream'
    - Concatenate all detected tables
    - Clean and normalize columns to: instrument, prix, volume, date, compartiment, source_file

    Returns a DataFrame with standardized columns.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    flavors = ["lattice", "stream"]
    tables = None
    for flavor in flavors:
        try:
            tables = camelot.read_pdf(file_path, pages=pages, flavor=flavor)
        except Exception:
            tables = None
        if tables and len(tables) > 0:
            break

    if not tables or len(tables) == 0:
        raise ValueError(f"No tables detected in PDF: {file_path}")

    dfs = []
    for t in tables:
        try:
            df = t.df.copy()
            dfs.append(df)
        except Exception:
            continue

    if len(dfs) == 0:
        raise ValueError(f"Failed to extract any table DataFrames from PDF: {file_path}")

    combined = pd.concat(dfs, ignore_index=True, sort=False)

    combined = _clean_dataframe(combined)
    combined = _map_columns(combined)

    # Try to coerce numeric columns
    if "prix" in combined.columns:
        combined["prix"] = pd.to_numeric(combined["prix"].str.replace(" ", "").str.replace(",", "."), errors="coerce")
    if "volume" in combined.columns:
        combined["volume"] = pd.to_numeric(combined["volume"].str.replace(" ", "").str.replace(",", "."), errors="coerce")

    if "date" in combined.columns:
        combined["date"] = pd.to_datetime(combined["date"], errors="coerce", dayfirst=True)

    # Ensure required columns exist
    for col in ("instrument", "prix", "volume", "date", "compartiment"):
        if col not in combined.columns:
            combined[col] = pd.NA

    combined["source_file"] = os.path.basename(file_path)
    combined["anomaly_score"] = pd.NA

    # Keep only standardized columns in a consistent order
    cols = ["instrument", "prix", "volume", "date", "compartiment", "source_file", "anomaly_score"]
    result = combined.loc[:, [c for c in cols if c in combined.columns]]

    return result


if __name__ == "__main__":
    # Quick local test when running the module directly
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(BASE_DIR, "../../data/uploads/BVMAC-instruction-n2-relative-aux-regles-de-marche-de-bvmac.pdf")
    try:
        df = parse_pdf(test_file)
        print(df.head())
    except Exception as e:
        print("Error parsing PDF:", e)
