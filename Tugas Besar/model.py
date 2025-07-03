# model.py
import datetime

class Perawatan:
    def __init__(self, deskripsi, kategori, hewan, tanggal, id_perawatan=None):
        self.id = id_perawatan
        self.deskripsi = deskripsi or "Tanpa Deskripsi"
        self.kategori = kategori or "Lainnya"
        self.hewan = hewan or "Tidak Diketahui"
        if isinstance(tanggal, str):
            self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
        else:
            self.tanggal = tanggal or datetime.date.today()

    def to_dict(self):
        return {
            "deskripsi": self.deskripsi,
            "kategori": self.kategori,
            "hewan": self.hewan,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }

class LokasiDokter:
    def __init__(self, nama, alamat, latitude, longitude, id_dokter=None):
        self.id = id_dokter
        self.nama = nama
        self.alamat = alamat
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "nama": self.nama,
            "alamat": self.alamat,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
