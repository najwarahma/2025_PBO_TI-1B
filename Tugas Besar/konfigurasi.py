# konfigurasi.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = "petcare.db"
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

KATEGORI_PERAWATAN = ["Makan", "Obat", "Grooming", "Vaksin", "Lainnya"]
KATEGORI_DEFAULT = "Lainnya"