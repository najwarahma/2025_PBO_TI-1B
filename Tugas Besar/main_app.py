# main_app.py
import streamlit as st
import datetime
from model import Perawatan, LokasiDokter
from manajer_perawatan import ManajerPerawatan
from manajer_lokasi import ManajerLokasi
from konfigurasi import KATEGORI_PERAWATAN
from streamlit_folium import st_folium
import folium
import locale

# Atur locale untuk format tanggal/Rupiah
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Indonesian_Indonesia.1252')
    except:
        pass

# Instance manager
perawatan_mgr = ManajerPerawatan()
lokasi_mgr = ManajerLokasi()

# Helper
def format_rupiah(jumlah):
    try:
        return locale.currency(jumlah or 0, grouping=True, symbol='Rp ')
    except:
        return f"Rp {jumlah or 0:,.0f}".replace(",", ".")

# Sidebar
st.sidebar.title("🐾 PetCare Manager")
halaman = st.sidebar.radio("Pilih Halaman:", [
    "➕ Tambah Perawatan", 
    "📋 Riwayat Perawatan", 
    "📊 Ringkasan", 
    "📍 Peta Dokter Hewan"
])
st.sidebar.markdown("---")
st.sidebar.caption("PetCare Manager v1")

# ➕ Tambah Perawatan
if halaman == "➕ Tambah Perawatan":
    st.header("Tambah Aktivitas Perawatan 🐶")
    with st.form("form_tambah", clear_on_submit=True):
        deskripsi = st.text_input("Deskripsi Perawatan")
        kategori = st.selectbox("Kategori:", KATEGORI_PERAWATAN)
        hewan = st.text_input("Nama/Jenis Hewan")
        tanggal = st.date_input("Tanggal:", value=datetime.date.today())
        simpan = st.form_submit_button("Simpan Data")
        if simpan:
            if deskripsi and hewan:
                p = Perawatan(deskripsi, kategori, hewan, tanggal)
                if perawatan_mgr.tambah_perawatan(p):
                    st.success("✅ Data berhasil disimpan!")
                else:
                    st.error("❌ Gagal menyimpan data.")
            else:
                st.warning("Deskripsi & Hewan wajib diisi!")

# 📋 Riwayat Perawatan
elif halaman == "📋 Riwayat Perawatan":
    st.header("📋 Riwayat Aktivitas Perawatan")

    # 🔹 Tampilkan sebagai tabel biasa dulu
    df = perawatan_mgr.get_dataframe_perawatan()
    if df.empty:
        st.info("Belum ada data perawatan.")
    else:
        st.subheader("📊 Tabel Ringkasan")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("✏️ Edit / 🗑️ Hapus Data")

        semua_data = perawatan_mgr.get_semua_perawatan()
        for item in semua_data:
            with st.expander(f"📌 {item.tanggal} | {item.hewan} - {item.kategori}"):
                col1, col2 = st.columns([1, 5])
                with col2:
                    st.markdown(f"**Deskripsi:** {item.deskripsi}")
                    st.markdown(f"**Kategori:** {item.kategori}")
                    st.markdown(f"**Hewan:** {item.hewan}")
                    st.markdown(f"**Tanggal:** {item.tanggal}")
                with col1:
                    hapus = st.button("🗑️ Hapus", key=f"hapus_{item.id}")
                    edit = st.button("✏️ Edit", key=f"edit_{item.id}")

                if hapus:
                    perawatan_mgr.hapus_perawatan(item.id)
                    st.warning(f"Data dengan ID {item.id} telah dihapus.")
                    st.experimental_rerun()

                if edit:
                    st.markdown("### Ubah Data Perawatan")
                    with st.form(f"form_edit_{item.id}"):
                        new_desc = st.text_input("Deskripsi", value=item.deskripsi)
                        new_kat = st.selectbox("Kategori", KATEGORI_PERAWATAN, index=KATEGORI_PERAWATAN.index(item.kategori))
                        new_hew = st.text_input("Hewan", value=item.hewan)
                        new_tgl = st.date_input("Tanggal", value=item.tanggal)
                        simpan_edit = st.form_submit_button("Simpan Perubahan")
                        if simpan_edit:
                            item.deskripsi = new_desc
                            item.kategori = new_kat
                            item.hewan = new_hew
                            item.tanggal = new_tgl
                            if perawatan_mgr.update_perawatan(item):
                                st.success("✅ Data berhasil diupdate.")
                                st.experimental_rerun()
                            else:
                                st.error("❌ Gagal update data.")

# 📊 Ringkasan
elif halaman == "📊 Ringkasan":
    st.header("Statistik Aktivitas Perawatan 📊")
    tanggal_filter = st.date_input("Filter tanggal (opsional)", value=None)
    kategori_stat = perawatan_mgr.hitung_aktivitas_per_kategori(tanggal_filter)
    hewan_stat = perawatan_mgr.hitung_aktivitas_per_hewan(tanggal_filter)

    st.subheader("➤ Grafik Jumlah Aktivitas per Kategori")
    if kategori_stat:
        st.bar_chart(data=kategori_stat)
    else:
        st.info("Tidak ada data kategori untuk tanggal tersebut.")

    st.subheader("➤ Grafik Jumlah Aktivitas per Hewan")
    if hewan_stat:
        st.bar_chart(data=hewan_stat)
    else:
        st.info("Tidak ada data hewan untuk tanggal tersebut.")

# 📍 Peta Dokter Hewan
elif halaman == "📍 Peta Dokter Hewan":
    st.header("📍 Peta Lokasi Dokter Hewan di Semarang")

    df_lokasi = lokasi_mgr.get_dataframe_lokasi()
    if df_lokasi.empty:
        st.warning("Belum ada data lokasi dokter hewan.")
    else:
        # 🗺️ Buat peta terpusat di Semarang
        peta = folium.Map(location=[-6.9904, 110.4229], zoom_start=13)

        # Tambahkan marker untuk semua lokasi
        for _, row in df_lokasi.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"<b>{row['nama']}</b><br>{row['alamat']}",
                tooltip=row['nama'],
                icon=folium.Icon(color="blue", icon="plus-sign", prefix="fa")
            ).add_to(peta)

        # Tampilkan peta di Streamlit
        st_folium(peta, width=700, height=500)

