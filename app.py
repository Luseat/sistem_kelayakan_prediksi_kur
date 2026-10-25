import streamlit as st
import pandas as pd
import joblib
import time

st.title("Aplikasi Prediksi Kelayakan Kredit Usaha Rakyat (KUR)")
st.write("Sistem ini memprediksi gagal bayar calon debitur KUR berdasarkan input data yang diberikan.")

#Load Model Pipeline yang udah diekspor dari Colab
@st.cache_resource
def load_model():
    return joblib.load("model/model_kredit_usaha_rakyat.pkl")

model = load_model()

tab1, tab2 = st.tabs(["Evaluasi Individu", "Evaluasi Massal (Upload CSV)"])

with tab1:
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
            with st.spinner(" Sedang memproses data & mengevaluasi kelayakan risiko kredit..."):
                time.sleep(3.5)
            
            
            st.markdown("----")
            cicilan_per_bulan = jumlah_pinjaman / tenor_pinjaman
            rasio_cicilan = (cicilan_per_bulan / omset) * 100
            batas_aman_cicilan = 0.40 * omset # Maksimal 40% dari omset
            sisa_omset = omset - cicilan_per_bulan
            
            
            st.subheader("📊 Ringkasan Kapasitas Finansial")
            m1, m2, m3 = st.columns(3)
            
            
            m1.metric(
                label="Estimasi Cicilan per Bulan",
                value=f"Rp {int(cicilan_per_bulan):,}".replace(",", ".")
            )
            
            
            m2.metric(
                label="Rasio Cicilan (DSR)", #Rasio Cicilan (DSR) terhadap batas 40%
                value=f"{rasio_cicilan:.1f}%",
                delta=f"{rasio_cicilan - 40:.1f}% dari batas aman 40%",
                delta_color="inverse"
            )
            
            
            m3.metric(
                label="Sisa Omset Bersih",
                value=f"Rp {int(sisa_omset):,}".replace(",", "."),
                delta="Surplus" if sisa_omset > 0 else "Defisit",
                delta_color="normal" if sisa_omset > 0 else "inverse"
            ) 
            
            
            st.markdown("----")
            st.subheader("Hasil Evaluasi Sistem:")
            
            
            if cicilan_per_bulan > batas_aman_cicilan:
                st.error("❌ **TIDAK LAYAK (REJECTED BY SYSTEM RULE)**")
                st.write(f"Sistem menolak otomatis. Rasio cicilan (**{rasio_cicilan:.1f}%**)melebihi batas toleransi risiko kredit perbankan (**maksimal 40% dari omset**).")
                
                
                import math 
                tenor_rekomendasi = math.ceil(jumlah_pinjaman / batas_aman_cicilan)
                pinjaman_maks_rekomendasi = batas_aman_cicilan * tenor_pinjaman
                st.info("**Rekomendasi Solusi dari Sistem (Simulasi Restrukturisasi)**")
                
                
                if tenor_rekomendasi <= 240:
                    cicilan_baru = jumlah_pinjaman / tenor_rekomendasi
                    rasio_baru = (cicilan_baru / omset) * 100
                    st.write(" Agar pengajuan ini memenuhi kriteria rasio aman perbankan (DSR $\le$ 40%), analis dapat menawarkan alternatif berikut:")
                    teks_opsi_1 = f"- **Opsi 1 (Perpanjang Tenor):** Naikan tenor dari **{int(tenor_pinjaman)} bulan** menjadi minimal **{tenor_rekomendasi} bulan** *(Estimasi cicilan baru menjadi **Rp {int(cicilan_baru):,}** /bulan dengan rasio beban **{rasio_baru:.1f}%**)*."
                    teks_opsi_2 = f"- **Opsi 2 (Sesuaikan plafon):** Jika nasabah ingin tetap tenor **{int(tenor_pinjaman)} bulan**, nominal pinjaman maksimal yang disarankan adalah **Rp {int(pinjaman_maks_rekomendasi):,}**."
                    st.markdown(f"{teks_opsi_1}\n{teks_opsi_2}".replace(",", "."))
                else:
                    st.write(f"Nominal pinjaman yang diajukan (**Rp {int(jumlah_pinjaman):,}**) terlalu jauh melampaui kapasitas omset bulanan nasabah (**Rp {int(omset):,}**).".replace(",", "."))
                    st.markdown(f" - ⚠️ Disarankan nasabah meningkatkan skala omset usaha terlebih dahulu  atau mengajukan  plafon pinjaman mikro yang lebih proposional.")
                
                
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
                    st.write("Nasabah ini lolos kriteria finansial dan diprediksi oleh AI memiliki risiko gagal bayar yang rendah.")
                else:
                    st.error("❌ **RISIKO GAGAL BAYAR TINGGI (REJECTED BY AI)**")
                    st.write("Nasabah lolos secara rasio finansial, namun AI mendeteksi pola historis yang berpotensi tinggi mengakibatkan kredit macet.")
                    
                    
                    st.info(" **Saran Mitigasi Risiko untuk analis kredit:**\n"
                            "- Lakukan verifikasi fisik lapangan terhadap tempat usaha dan chek mutasi rekening 3 bulan terakhir.\n"
                            "- Pertimbangkan opsi penambahan  agunan fisik untuk syarat penjamin (*guarantor*) sebelum mengambil keputusan akhir.")


with tab2:
    st.header("Evaluasi kelayakan kredit massal via file csv")
    st.write("Unggah file calon debitur untuk memproses puluhan hingga ratusan data pengajuan sekaligus.")
    
    contoh_data = pd.DataFrame({
        'usia': [35, 28, 45],
        'jenis_kelamin': ['laki-laki', 'perempuan', 'laki-laki'],
        'status': ['wirausaha', 'karyawan', 'wirausaha'],
        'omset': [15000000, 5000000, 25000000],
        'jumlah_pinjaman': [30000000, 40000000, 50000000],
        'tenor_pinjaman_(bulan)': [12, 6, 24],
        'jumlah_anak': [2, 0, 3],
        'riwayat_telat_bayar': [1, 0, 1]
    })
    
    
    csv_template = contoh_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Unduh Template CSV",
        data=csv_template,
        file_name="template_pengujian_kur.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    uploaded_file = st.file_uploader(" pilih file CSV calon nasabah", type=["csv"])
    
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"Berhasil memuat {len(df_upload)} baris data calon debitur")
            
            st.subheader("Pratinjau Data:")
            st.dataframe(df_upload.head())
            
            #normalisasi dari tenor_pinjaman_(bulan) -> tenor_pinjaman
            if 'tenor_pinjaman' in df_upload.columns and 'tenor_pinjaman_(bulan)' not in df_upload.columns:
                df_upload.rename(columns={'tenor_pinjaman': 'tenor_pinjaman_(bulan)'}, inplace=True)
                
            kolom_wajib = [
                'usia', 
                'jenis_kelamin', 
                'status', 
                'omset', 
                'jumlah_pinjaman', 
                'tenor_pinjaman_(bulan)', 
                'jumlah_anak', 
                'riwayat_telat_bayar'
            ]
            
            
            #validasi user wajib input semua
            kolom_kurang = [co1 for co1 in kolom_wajib if co1 not in df_upload.columns]
            if kolom_kurang:
                st.error(f"❌ File CSV tidak valid! Kolom berikut tidak ditemukan: {kolom_kurang}")
                st.info("Silahkan unduh dan gunakan template contoh diatas guna memastikan format kolom yang sesuai.")
            else:
                if st.button("Mulai evaluasi massal"):
                    with st.spinner("Sedang memproses data & mengevaluasi massal kelayakan risiko kredit (Hard Rule & AI Ensemble)..."):
                        time.sleep(3.5)
                        
                        df_hasil = df_upload.copy()

st.markdown("<br><br><br><br>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; margin-bottom: 5px;'>"
    "Copyright &copy; 2026 Hanifudin Robbani | All Rights Reserved."
    "</p>", 
    unsafe_allow_html=True
)
            