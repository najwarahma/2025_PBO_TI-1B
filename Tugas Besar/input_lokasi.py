from model import LokasiDokter
from manajer_lokasi import ManajerLokasi

lokasi_mgr = ManajerLokasi()

lokasi_baru = [
    LokasiDokter("Aruna Pet Care", "Villa P4A Blok A1 No.6, Pudakpayung", -7.096526880387632, 110.41710981472804),
    LokasiDokter("Blossom Pet Care", "Jl. Cemara Raya No.8, Padangsari", -7.072935142159645, 110.42267522592775),
    LokasiDokter("Klinik Dokter Hewan | Emerald Pet Clinic", "Jl. MT. Haryono No.747, Wonodri", -7.002389768955787, 110.43182001472798),
    LokasiDokter("Pet Zone", "Jl. Ngesrep Tim. V No.105, Sumurboto", -7.050873634532909, 110.42937001941394),
    LokasiDokter("GSL Pet Point Banyumanik", "Jl. Tirto Agung No.56a, Pedalangan", -7.058456588603215, 110.42800176583863 ),
    LokasiDokter("Kochibon Pet Store and Veterinary", "Jl. Tusam Timur Raya No.36, Pedalangan", -7.066717140358719, 110.426280114728),
    LokasiDokter("Klinik Hewan Dan Pets drh. Bambang Himawan", "Jl. Meranti Raya No.141, Padangsari", -7.0727647870610975, 110.42233190318488),
    LokasiDokter("TEN-TEN PETCARE", "Jl. Alam Asri Raya No.18, Tembalang", -7.037003058225755, 110.47500767609945),
    LokasiDokter("Klinik Hewan My Cat Veterinary Service Ungaran", "Jl. Ahmad Yani No.12, Dliwang, Ungaran", -7.128722576374877, 110.40891492952804)
]

for lokasi in lokasi_baru:
    lokasi_mgr.tambah_lokasi(lokasi)

print("✔️ Semua lokasi berhasil ditambahkan ke database.")
