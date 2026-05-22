import os
import camelot
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    BASE_DIR,
    "app/data/uploads/BVMAC-instruction-n2-relative-aux-regles-de-marche-de-bvmac.pdf"
)

tables = camelot.read_pdf(file_path, pages="all")

all_tables = []

for t in tables:
    df = t.df
    all_tables.append(df)

final_df = pd.concat(all_tables, ignore_index=True)

print(final_df.head())