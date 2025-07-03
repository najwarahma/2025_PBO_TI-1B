# database.py
import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"[DB ERROR] Gagal koneksi: {e}")
        return None

def execute_query(query: str, params: tuple = ()):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"[DB ERROR] Query gagal: {e}")
        return None
    finally:
        conn.close()

def fetch_all(query: str, params: tuple = ()):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Fetch gagal: {e}")
        return []
    finally:
        conn.close()

def get_dataframe(query: str, params: tuple = ()) -> pd.DataFrame:
    conn = get_connection()
    if not conn: return pd.DataFrame()
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"[DB ERROR] Gagal baca DataFrame: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
