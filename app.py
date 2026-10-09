import streamlit as st
import pandas as pd
import joblib

st.title("Aplikasi Prediksi Kelayakan Kredit Usaha Rakyat (KUR)")
st.write("Sistem ini memprediksi gagal bayar calon debitur KUR berdasarkan input data yang diberikan.")

#Load Model Pipeline yang udah diekspor dari Colab
@st.cache_resource
def load_model():
    return joblib.load("model/model_kredit_usaha_rakyat.pkl")

model = load_model()

st.header("Masukan Data Calon Debitur")
col1, col2 = st.columns(2)

with col1:
    usia = st.number_input("Usia Nasabah", min_value=18, max_value=100, value=None, placeholder="Masukkan usia")
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    status = st.selectbox("status Pekerjaan", ["Wirausaha", "Karyawan"])
    jumlah_anak = st.number_input("Jumlah Anak/Tanggungan", min_value=0, max_value=20, value=None, placeholder="Jika tidak ada, isi 0")
    
with col2:
    omset = st.number_input("Pendapatan / Omset per Bulan (Rp)", min_value=0, step=1000000, value=None, placeholder="Masukkan omset per bulan")
    jumlah_pinjaman = st.number_input("Nominal Pinjaman yang Diajukan (Rp)", min_value=1, value=None, step=1000000, placeholder="Masukkan nominal pinjaman")
    tenor_pinjaman = st.number_input("Tenor Pinjaman (Bulan)", min_value=1, max_value=240, value=None, placeholder="Masukkan tenor pinjaman")
    riwayat_telat_bayar = st.selectbox("Riwayat Telat Bayar Sebelumnya", ["Tidak Pernah", "Pernah"])


if st.button("Mulai Prediksi Kelayakan"):
    
    #Cek kalau ada kotak angka yang belum diisi
    if None in [usia, jumlah_anak, omset, jumlah_pinjaman, tenor_pinjaman]:
        st.warning("⚠️ Mohon ketik dan lengkapi semua data angka di atas sebelum memprediksi.")
    else:
        st.markdown("----")
        st.subheader("Hasil Evaluasi Sistem:")
        
        
        cicilan_per_bulan = jumlah_pinjaman / tenor_pinjaman
        batas_aman_cicilan = 0.40 * omset # Asumsi bank: cicilan maksimal 40% dari omset bulanan
        
        if cicilan_per_bulan > batas_aman_cicilan:
            st.error("❌ **TIDAK LAYAK (REJECTED BY SYSTEM RULE)**")
            st.write(f"Sistem menolak otomatis. Perkiraan cicilan (Rp {cicilan_per_bulan:,.0f}/bulan) terlalu besar dan melebihi batas rasio aman 40% dari omset (Rp {batas_aman_cicilan:,.0f}/bulan).")
        else:
            # Mapping inputan UI ke format yang dimengerti model
            input_data = pd.DataFrame({
                'usia': [usia],
                'jenis_kelamin': [jenis_kelamin.lower()], # Huruf keciln sesuai training
                'status': [status.lower()], # Huruf kecil sesuai training
                'omset': [omset],
                'jumlah_pinjaman': [jumlah_pinjaman],
                'tenor_pinjaman_(bulan)': [tenor_pinjaman],
                'jumlah_anak': [jumlah_anak],
                'riwayat_telat_bayar': [0 if riwayat_telat_bayar == "Tidak Pernah" else 1] # = Tidak Pernah, 1 = Pernah
            })
            
            
            #Eksekusi Prediksimodel bakal otomatis nge-scale dan nge-encode input_data ini
            prediksi = model.predict(input_data)[0]
            
            
            if prediksi == 0:
                st.success("✅ **LAYAK DIBERIKAN (APPROVED)**")
                st.write("Nasabah ini lolos kriteria finansial dan diprediksi oleh AImemiliki risiko gagal bayar yang rendah.")
            else:
                st.error("❌ **RISIKO GAGAL BAYAR TINGGI (REJECTED BY AI)**")
                st.write("Nasabah lolos secara rasio finansial, namun AI mendeteksi pola historis yang berpotensi tinggi mengakibatkan kredit macet.")
            