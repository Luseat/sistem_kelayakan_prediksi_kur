import streamlit as st
import pandas as pd
import joblib

st.title("Aplikasi Prediksi Kelayakan Kredit Usaha Rakyat (KUR)")
st.write("Sistem ini memprediksi gagal bayar calon debitur KUR berdasarkan input data yang diberikan.")

@st.cache_resource
def load_model():
    return joblib.load("model_kredit_usaha_rakyat.pkl")

model = load_model()

st.header("Masukan Data Calon Debitur")
col1, col2 = st.columns(2)

with col1:
    usia = st.number_input("Usia Nasabah", min_value=18, max_value=100, value=30)
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    status = st.selectbox("status Pekerjaan", ["Wirausaha", "Karyawan"])
    jumlah_anak = st.number_input("Jumlah Anak/Tanggungan", min_value=0, max_value=20, value=0)
    
with col2:
    omset = st.number_input("Pendapatan / Omset per Bulan (Rp)", min_value=0, value=10000000, step=1000000)
    jumlah_pinjaman = st.number_input("Nominal Pinjaman yang Diajukan (Rp)", min_value=1, value=500000000, step=1000000)
    tenor_pinjaman = st.number_input("Tenor Pinjaman (Bulan)", min_value=1, max_value=240, value=12)
    riwayat_telat_bayar = st.selectbox("Riwayat Telat Bayar Sebelumnya", ["Tidak Pernah", "Pernah"])


if st.button("Mulai Prediksi Kelayakan"):
    
    input_data = pd.DataFrame({
        'usia': [usia],
        'jenis_kelamin': [jenis_kelamin.lower()],
        'status': [status.lower()],
        'omset': [omset],
    })