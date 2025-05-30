import streamlit as st
import pandas as pd
import sqlite3

# Langkah 1: Load dan simpan data ke SQLite
@st.cache_resource
def load_data():
    df = pd.read_excel('siswa.xlsx')
    conn = sqlite3.connect('siswa.db')
    df = pd.read_sql_query("SELECT * FROM siswa", conn)
    conn.close()
    return df

# Langkah 2: Koneksi database
conn = load_data()

# Langkah 3: Judul & Input
st.title("📋 Cari Data Siswa Berdasarkan NISN")
akun = st.text_input("Masukkan NISN:", placeholder="00454323-04122008")
cek = st.button("🔍 Cek Data")

# Langkah 4: Aksi saat tombol diklik
if cek:
    if akun.strip() == "":
        st.warning("⚠️ Silakan masukkan NISN terlebih dahulu.")
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM siswa WHERE Akun = ?", (akun,))
        hasil = cursor.fetchone()

        if hasil:
            kolom = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(kolom, hasil))

            # Langkah 5: Tampilan elegan
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
                """,
                unsafe_allow_html=True
                
            )
            st.markdown("[Pengjuan Perbaikan](https://example.com)")
        else:
            st.error("❌ NISN tidak ditemukan dalam database.")

