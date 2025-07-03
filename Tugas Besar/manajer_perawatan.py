# manajer_perawatan.py
from model import Perawatan
import database
import datetime
import pandas as pd

class ManajerPerawatan:
    def tambah_perawatan(self, perawatan: Perawatan) -> bool:
        if not isinstance(perawatan, Perawatan): return False
        sql = """
            INSERT INTO perawatan (deskripsi, kategori, hewan, tanggal)
            VALUES (?, ?, ?, ?)
        """
        params = (
            perawatan.deskripsi,
            perawatan.kategori,
            perawatan.hewan,
            perawatan.tanggal.strftime("%Y-%m-%d")
        )
        result = database.execute_query(sql, params)
        return result is not None

    def get_semua_perawatan(self) -> list[Perawatan]:
        sql = """
            SELECT id, deskripsi, kategori, hewan, tanggal
            FROM perawatan
            ORDER BY tanggal DESC, id DESC
        """
        rows = database.fetch_all(sql)
        return [
            Perawatan(
                id_perawatan=row["id"],
                deskripsi=row["deskripsi"],
                kategori=row["kategori"],
                hewan=row["hewan"],
                tanggal=row["tanggal"]
            )
            for row in rows
        ]

    def get_dataframe_perawatan(self, tanggal_filter: datetime.date = None) -> pd.DataFrame:
        sql = """
            SELECT tanggal, hewan, kategori, deskripsi
            FROM perawatan
        """
        params = ()
        if tanggal_filter:
            sql += " WHERE tanggal = ?"
            params = (tanggal_filter.strftime("%Y-%m-%d"),)
        sql += " ORDER BY tanggal DESC, id DESC"
        return database.get_dataframe(sql, params)

    def hitung_aktivitas_per_kategori(self, tanggal_filter: datetime.date = None) -> dict:
        sql = "SELECT kategori, COUNT(*) FROM perawatan"
        params = []
        if tanggal_filter:
            sql += " WHERE tanggal = ?"
            params.append(tanggal_filter.strftime("%Y-%m-%d"))
        sql += " GROUP BY kategori"
        rows = database.fetch_all(sql, tuple(params))
        return {row["kategori"]: row[1] for row in rows}

    def hitung_aktivitas_per_hewan(self, tanggal_filter: datetime.date = None) -> dict:
        sql = "SELECT hewan, COUNT(*) FROM perawatan"
        params = []
        if tanggal_filter:
            sql += " WHERE tanggal = ?"
            params.append(tanggal_filter.strftime("%Y-%m-%d"))
        sql += " GROUP BY hewan"
        rows = database.fetch_all(sql, tuple(params))
        return {row["hewan"]: row[1] for row in rows}
    
    def update_perawatan(self, perawatan: Perawatan) -> bool:
        sql = """
        UPDATE perawatan
        SET deskripsi = ?, kategori = ?, hewan = ?, tanggal = ?
        WHERE id = ?
    """
        params = (
            perawatan.deskripsi,
            perawatan.kategori,
            perawatan.hewan,
            perawatan.tanggal.strftime("%Y-%m-%d"),
            perawatan.id
    )
        return database.execute_query(sql, params) is not None


    def hapus_perawatan(self, id_perawatan: int) -> bool:
        sql = "DELETE FROM perawatan WHERE id = ?"
        return database.execute_query(sql, (id_perawatan,)) is not None
