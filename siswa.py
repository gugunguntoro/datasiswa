import streamlit as st
import pandas as pd
import sqlite3

# Cache DataFrame dari database
@st.cache_data
def load_data():
    conn = sqlite3.connect('siswa.db')
    df = pd.read_sql_query("SELECT * FROM siswa", conn)
    conn.close()
    return df

# Cache koneksi ke database
@st.cache_resource
def get_connection():
    return sqlite3.connect('siswa.db', check_same_thread=False)

# Load koneksi
conn = get_connection()

# Judul & Input
st.subheader("Cek Kelengkapan Data E-Ijazah", divider=True)
st.title("Cari Data Siswa Berdasarkan NISN dan Tanggal Lahir")
akun = st.text_input("Masukkan NISN dan Tanggal Lahir:", placeholder="Contoh: 00454323-04122008")
cek = st.button("🔍 Cek Data")

# Aksi saat tombol ditekan
if cek:
    if akun.strip() == "":
        st.warning("⚠️ Silakan masukkan NISN dan Tanggal Lahir terlebih dahulu.")
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM siswa WHERE Akun = ?", (akun,))
        hasil = cursor.fetchone()

        if hasil:
            kolom = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(kolom, hasil))

            st.markdown(
                f"""
                <div style="border: 2px solid #4CAF50; padding: 16px; border-radius: 10px; background-color: #f0fff0;">
                    <h4 style="color:#2e7d32;">✅ Data Siswa Ditemukan</h4>
                    <ul style="list-style-type: none; padding: 0;">
                        <li><strong>Nama:</strong> {data_dict.get('Nama', '-')}</li>
                        <li><strong>NISN:</strong> {data_dict.get('NISN', '-')}</li>
                        <li><strong>Kelas:</strong> {data_dict.get('Kelas', '-')}</li>
                        <li><strong>Alamat:</strong> {data_dict.get('Alamat', '-')}</li>
                    </ul>
                </div>
                <br>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                "[![Pengajuan Perbaikan](https://img.shields.io/badge/Pengajuan%20Perbaikan-blue)](https://example.com)"
            )

        else:
            st.error("❌ Akun tidak ditemukan dalam database.")
