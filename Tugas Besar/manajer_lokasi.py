# manajer_lokasi.py
from model import LokasiDokter
import database

class ManajerLokasi:
    def get_semua_lokasi(self) -> list[LokasiDokter]:
        sql = """
            SELECT id, nama, alamat, latitude, longitude
            FROM lokasi_dokter
            ORDER BY nama ASC
        """
        rows = database.fetch_all(sql)
        return [
            LokasiDokter(
                id_dokter=row["id"],
                nama=row["nama"],
                alamat=row["alamat"],
                latitude=row["latitude"],
                longitude=row["longitude"]
            )
            for row in rows
        ]

    def get_dataframe_lokasi(self):
        sql = """
            SELECT nama, alamat, latitude, longitude
            FROM lokasi_dokter
            ORDER BY nama ASC
        """
        return database.get_dataframe(sql)

    def tambah_lokasi(self, lokasi: LokasiDokter) -> bool:
        sql = """
            INSERT INTO lokasi_dokter (nama, alamat, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """
        params = (lokasi.nama, lokasi.alamat, lokasi.latitude, lokasi.longitude)
        return database.execute_query(sql, params) is not None
