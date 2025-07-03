# manajer_anggaran.py
import datetime
import pandas as pd
from model import Transaksi
import database  # Impor modul database kita

class AnggaranHarian:
    """Mengelola logika bisnis pengeluaran harian (Repository Pattern)."""
    
    _db_setup_done = False  # Flag: Setup DB hanya sekali per sesi

    def __init__(self):
        if not AnggaranHarian._db_setup_done:
            print("[AnggaranHarian] Melakukan pengecekan/setup database awal...")
            if database.setup_database_initial():
                AnggaranHarian._db_setup_done = True
                print("[AnggaranHarian] Database siap.")
            else:
                print("[AnggaranHarian] KRITIKAL: Setup database awal GAGAL!")

    def tambah_transaksi(self, transaksi: Transaksi) -> bool:
        """Menambahkan transaksi baru ke database."""
        if not isinstance(transaksi, Transaksi) or transaksi.jumlah <= 0:
            return False

        sql = """
            INSERT INTO transaksi (deskripsi, jumlah, kategori, tanggal)
            VALUES (?, ?, ?, ?)
        """
        params = (
            transaksi.deskripsi,
            transaksi.jumlah,
            transaksi.kategori,
            transaksi.tanggal.strftime("%Y-%m-%d")
        )
        last_id = database.execute_query(sql, params)

        if last_id is not None:
            transaksi.id = last_id
            return True
        return False

    def get_semua_transaksi_obj(self) -> list[Transaksi]:
        """Mengambil semua transaksi sebagai list objek Transaksi."""
        sql = """
            SELECT id, deskripsi, jumlah, kategori, tanggal
            FROM transaksi
            ORDER BY tanggal DESC, id DESC
        """
        rows = database.fetch_query(sql, fetch_all=True)
        transaksi_list = []

        if rows:
            for row in rows:
                transaksi_list.append(
                    Transaksi(
                        id_transaksi=row['id'],
                        deskripsi=row['deskripsi'],
                        jumlah=row['jumlah'],
                        kategori=row['kategori'],
                        tanggal=row['tanggal']
                    )
                )
        return transaksi_list

    def get_dataframe_transaksi(self, filter_tanggal: datetime.date | None = None) -> pd.DataFrame:
        """Mengambil data transaksi dalam bentuk DataFrame, opsional difilter berdasarkan tanggal."""
        query = "SELECT id, tanggal, kategori, deskripsi, jumlah FROM transaksi"
        params = None

        if filter_tanggal:
            query += " WHERE tanggal = ?"
            params = (filter_tanggal.strftime("%Y-%m-%d"),)

        query += " ORDER BY tanggal DESC, id DESC"
        df = database.get_dataframe(query, params=params)

        if not df.empty:
            try:
                import locale
                locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
                df['Jumlah (Rp)'] = df['jumlah'].map(
                    lambda x: locale.currency(x or 0, grouping=True, symbol='Rp ')[:-3]
                )
            except:
                df['Jumlah (Rp)'] = df['jumlah'].map(
                    lambda x: f"Rp {x or 0:,.0f}".replace(",", ".")
                )
            if 'id' not in df.columns and 'id_transaksi' in df.columns:
                df = df.rename(columns={'id_transaksi': 'id'})
                
            required_cols = ['id', 'tanggal', 'kategori', 'deskripsi', 'Jumlah (Rp)']
            available_cols = [col for col in required_cols if col in df.columns]
            df = df[available_cols]

        return df

    def hitung_total_pengeluaran(self, tanggal: datetime.date | None = None) -> float:
        """Menghitung total pengeluaran, bisa difilter berdasarkan tanggal."""
        sql = "SELECT SUM(jumlah) FROM transaksi"
        params = None

        if tanggal:
            sql += " WHERE tanggal = ?"
            params = (tanggal.strftime("%Y-%m-%d"),)

        result = database.fetch_query(sql, params=params, fetch_all=False)
        if result and result[0] is not None:
            return float(result[0])
        return 0.0

    def get_pengeluaran_per_kategori(self, tanggal: datetime.date | None = None) -> dict:
        """Mengelompokkan pengeluaran berdasarkan kategori (opsional per tanggal)."""
        hasil = {}
        sql = "SELECT kategori, SUM(jumlah) FROM transaksi"
        params = []

        if tanggal:
            sql += " WHERE tanggal = ?"
            params.append(tanggal.strftime("%Y-%m-%d"))

        sql += " GROUP BY kategori HAVING SUM(jumlah) > 0 ORDER BY SUM(jumlah) DESC"
        rows = database.fetch_query(sql, params=tuple(params) if params else None, fetch_all=True)

        if rows:
            for row in rows:
                kategori = row['kategori'] if row['kategori'] else "Lainnya"
                jumlah = float(row[1]) if row[1] is not None else 0.0
                hasil[kategori] = jumlah

        return hasil
    
    # Tambahkan dalam class AnggaranHarian
    def hapus_transaksi(self, id_transaksi: int) -> bool:
        """Menghapus transaksi berdasarkan ID."""
        sql = "DELETE FROM transaksi WHERE id = ?"
        params = (id_transaksi,)
        try:
            # Run the delete query
            rows_affected = database.execute_query(sql, params)
            if rows_affected > 0:  # Check if any row was deleted
                return True
            else:
                print(f"Error: No rows affected for ID {id_transaksi}")
                return False
        except Exception as e:
            print(f"Error saat menghapus transaksi: {e}")
            return False


