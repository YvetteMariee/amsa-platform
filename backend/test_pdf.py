import os
import camelot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    BASE_DIR,
    "app/data/uploads/BVMAC-instruction-n2-relative-aux-regles-de-marche-de-bvmac.pdf"
)

print("Fichier utilisé :", file_path)

tables = camelot.read_pdf(file_path, pages="all")

print("Tables détectées :", tables.n)

if tables.n > 0:
    print(tables[0].df.head())