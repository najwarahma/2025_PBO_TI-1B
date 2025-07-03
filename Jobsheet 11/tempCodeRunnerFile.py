# setup_db_petcare.py
import sqlite3
from konfigurasi import DB_PATH

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabel Perawatan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perawatan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            kategori TEXT NOT NULL,
            hewan TEXT NOT NULL,
            tanggal DATE NOT NULL
        );
    """)

    # Tabel Lokasi Dokter
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lokasi_dokter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("✔️ Database dan tabel berhasil dibuat!")

if __name__ == "__main__":
    setup_database()
