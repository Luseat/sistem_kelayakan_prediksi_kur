# 🏦 Sistem Prediksi Kelayakan Kredit Usaha Rakyat (KUR) UMKM

Aplikasi berbasis web untuk memprediksi kelayakan dan risiko gagal bayar calon debitur Kredit Usaha Rakyat (KUR) di sektor UMKM. Sistem ini mengadopsi pendekatan **Hybrid Evaluation Architecture**: memadukan *Financial Hard Business Rule* (analisis rasio kapasitas angsuran perbankan), *Machine Learning Ensemble* (**Random Forest** + **Bagging Classifier** dengan teknik **Voting Classifier** & **SMOTE**), serta modul cerdas **What-If Recommendation Engine** untuk simulasi restrukturisasi kredit.

---

##  Latar Belakang & Masalah

Pemberian fasilitas kredit bagi pelaku Usaha Mikro, Kecil, dan Menengah (UMKM) memegang peranan krusial dalam pertumbuhan ekonomi daerah. Namun, proses evaluasi kelayakan kredit yang dilakukan secara manual sering kali menghadapi kendala:
- **Subjektivitas & Human Error**: Penilaian analis kredit berisiko inkonsisten antar-staf verifikator.
- **Efisiensi Waktu**: Proses analisis kelayakan berkas fisik memakan waktu yang cukup lama.
- **Risiko Kredit Macet (NPL)**: Potensi kerugian finansial akibat salah meloloskan calon debitur berisiko gagal bayar tinggi (*False Positive*).
- **Ketiadaan Solusi Alternatif**: Penolakan kredit sering kali bersifat final tanpa memberikan opsi alternatif penyesuaian fasilitas pinjaman bagi nasabah yang potensial.

Sistem ini dikembangkan sebagai solusi otomatisasi analisis kredit yang objektif, transparan, cepat, dan presisi tinggi guna meminimalisir risiko kredit macet sekaligus memberikan rekomendasi finansial yang adaptif.

---

##  Fitur Utama & Cara Kerja Sistem (Hybrid Architecture)

Sistem mengadopsi arsitektur evaluasi dua lapis (*Dual-Layer Decision Model*) yang terintegrasi dengan modul analitik dan simulasi bisnis:

```
                       [ Input Data Calon Debitur ]
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   Simulasi Pemrosesan & Visual Feedback (st.spinner)   │
       │    Analisis profil risiko nasabah secara real-time     │
       └────────────────────────────┬───────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   📊 Kartu Ringkasan Kapasitas Finansial (st.metric)   │
       │    - Estimasi Angsuran / Bulan (Rp)                    │
       │    - Debt Service Ratio / DSR (% vs batas aman 40%)    │
       │    - Sisa Omset Bersih (Status Surplus / Defisit)      │
       └────────────────────────────┬───────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   Lapis 1: Hard Business Rule (Rasio Finansial Bank)   │
       │     Cicilan per Bulan > 40% Omset Bulanan?             │
       └────────────────────────────┬───────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                   Ya                               Tidak
                    │                               │
                    ▼                               ▼
       ❌ REJECTED BY SYSTEM RULE      ┌─────────────────────────────┐
        (Kapasitas Finansial Kurang)   │ Lapis 2: Machine Learning   │
                    │                  │    Pipeline (Scikit-Learn)  │
                    ▼                  │  - Scaling & One-Hot Encode │
          What-If Recommendation Engine│  - Voting Classifier        │
        - Opsi 1: Perpanjangan Tenor   │    (Random Forest + Bagging)│
        - Opsi 2: Penyesuaian Plafon   └──────────────┬──────────────┘
                                                      │
                                      ┌───────────────┴───────────────┐
                                      ▼                               ▼
                           ✅ APPROVED BY AI               ❌ REJECTED BY AI
                        (Risiko Rendah / Layak)          (Pola Risiko Macet Tinggi)
                                                                      │
                                                                      ▼
                                                         💡 Saran Mitigasi Risiko
                                                         (Survei, Mutasi, Agunan)
```

### 1. 📊 Kartu Ringkasan Kapasitas Finansial (Financial Metrics Cards)
Sebelum hasil keputusan ditampilkan, sistem menyajikan 3 metrik kesehatan finansial calon debitur menggunakan widget `st.metric`:
- **Estimasi Cicilan per Bulan**: Nominal cicilan tetap yang dihitung dari `jumlah_pinjaman / tenor_pinjaman`.
- **Rasio Beban Cicilan (Debt Service Ratio / DSR)**: Persentase beban cicilan terhadap omset bulanan, dilengkapi indikator warna dinamis (berwarna hijau jika dalam batas aman $\le 40\%$, dan otomatis merah jika melampaui batas aman $> 40\%$).
- **Sisa Omset Bersih (Disposable Income)**: Estimasi dana tersisa setelah dipotong angsuran, lengkap dengan penanda status **Surplus** atau **Defisit**.

### 2. 💡 Fitur Rekomendasi Alternatif (What-If Analysis Engine)
Ketika pengajuan ditolak pada Lapis 1 karena rasio cicilan melampaui batas toleransi risiko ($> 40\%$), sistem tidak hanya menolak, tetapi secara proaktif menghitung **solusi restrukturisasi kredit** secara otomatis:
- **Opsi 1 (Perpanjangan Tenor)**: Menghitung tenor pengembalian minimal agar cicilan bulanan turun hingga memenuhi batas aman rasio keuangan:
  $$\text{Tenor Rekomendasi} = \left\lceil \frac{\text{Jumlah Pinjaman}}{\text{Batas Aman Cicilan}} \right\rceil$$
- **Opsi 2 (Penyesuaian Plafon Pinjaman)**: Menghitung nominal pinjaman maksimal yang realistis berdasarkan jangka waktu (tenor) yang diinginkan nasabah:
  $$\text{Plafon Maksimal Rekomendasi} = \text{Batas Aman Cicilan} \times \text{Tenor Pinjaman}$$
- **Proteksi Pinjaman Ekstrem**: Jika nilai pinjaman terlalu jauh melampaui kapasitas omset bulanan (misal melebihi batas tenor 20 tahun), sistem memberikan arahan bagi nasabah untuk meningkatkan skala omset usaha terlebih dahulu atau mengajukan fasilitas kredit mikro yang proporsional.

### 3. 🛡️ Lapis 1 - Financial Hard Rule (Akal Sehat Finansial)
- Menguji kelayakan rasio kapasitas bayar calon debitur.
- Jika cicilan per bulan melebihi **40% dari total omset bulanan**, pengajuan akan **ditolak secara otomatis oleh sistem (Rejected by System Rule)** demi mencegah *over-indebtedness* (gali lubang tutup lubang) tanpa membebani model AI.

### 4. 🤖 Lapis 2 - Machine Learning Ensemble Pipeline
- Jika calon debitur lolos evaluasi finansial Lapis 1, data dialirkan ke pipeline Machine Learning.
- Model memadukan **Tuned Random Forest Classifier** dan **Tuned Bagging Classifier** melalui mekanisme konsensus **Hard Voting**.
- Ketimpangan kelas (*class imbalance*) ditangani menggunakan teknik **SMOTE (Synthetic Minority Over-sampling Technique)** pada saat pelatihan agar sistem memiliki sensitivitas tinggi (*Recall*) dalam mendeteksi potensi debitur bermasalah.
- **Saran Mitigasi Risiko**: Jika nasabah lolos rasio finansial namun ditolak oleh AI, sistem memberikan panduan audit lapangan (verifikasi tempat usaha, cek mutasi rekening 3 bulan terakhir, dan pertimbangan agunan tambahan).

### 5.  Animasi Pemrosesan Interaktif (Smart Loading Spinner)
Sistem dilengkapi animasi pemrosesan (`st.spinner`) dan jeda cerdas (*processing delay*) saat tombol evaluasi ditekan. Hal ini memberikan transparansi serta pengalaman pengguna (UX) yang realistis bahwa sistem sedang menjalankan komputasi analisis risiko mendalam.

### 6.  Validasi Input Form Dinamis
- Input angka dirancang tanpa nilai bawaan (*value=None*) disertai *placeholder* informatif, mengharuskan user mengisi data secara manual.
- Dilengkapi sistem penahan (*input validation guardrail*) untuk mencegah kesalahan sistem jika ada parameter yang belum diisi.

---

## 📊 Atribut Data Input

| Parameter | Tipe Data | Format Input | Deskripsi |
| :--- | :--- | :--- | :--- |
| `usia` | Numerik | 18 - 100 Tahun | Usia calon debitur |
| `jenis_kelamin` | Kategorikal | Laki-laki / Perempuan | Jenis kelamin nasabah |
| `status` | Kategorikal | Wirausaha / Karyawan | Kategori pekerjaan debitur |
| `jumlah_anak` | Numerik | 0 - 20 Anak | Jumlah anak / tanggungan keluarga |
| `omset` | Numerik | Rupiah (Rp) | Estimasi omset/pendapatan bersih per bulan |
| `jumlah_pinjaman` | Numerik | Rupiah (Rp) | Plafon pinjaman yang diajukan |
| `tenor_pinjaman_(bulan)` | Numerik | 1 - 240 Bulan | Jangka waktu pengembalian kredit |
| `riwayat_telat_bayar` | Biner | Tidak Pernah (0) / Pernah (1) | Rekam jejak kolektibilitas angsuran sebelumnya |

**Label Hasil Keputusan:**
- `0`: **Approved** (Risiko gagal bayar rendah / Layak diberikan fasilitas kredit)
- `1`: **Rejected** (Risiko gagal bayar tinggi / Ditolak oleh AI atau System Rule)

---

## 📂 Struktur Direktori Proyek

```text
kredit_usaha_rakyat/
│
├── .gitignore                                     # Mengabaikan folder env, venv, cache pyc
├── app.py                                         # Aplikasi web Streamlit (UI, Hard Rule, What-If Engine, & Integrasi AI)
├── pembuatan_model_random_forest_&_bagging.ipynb  # Notebook eksplorasi data, SMOTE, GridSearchCV, & ekspor model
├── README.md                                      # Dokumentasi teknis proyek
│
├── model/
│   └── model_kredit_usaha_rakyat.pkl              # Pipeline model ter-serialisasi (Scikit-Learn & ImbPipeline)
│
└── env/                                           # Virtual environment lokal (Python)
```

---

## 🛠️ Panduan Instalasi & Menjalankan Aplikasi

### 1. Klon Repositori
```bash
git clone https://github.com/Luseat/sistem_kelayakan_prediksi_kur.git
cd sistem_kelayakan_prediksi_kur
```

### 2. Siapkan Virtual Environment
Gunakan Python 3.10+ (disarankan mengisolasi pustaka via virtual environment):
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux / MacOS
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependensi yang Dibutuhkan
```bash
pip install streamlit pandas scikit-learn imbalanced-learn joblib numpy
```

### 4. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Aplikasi akan langsung terbuka di browser lokal pada alamat `http://localhost:8501`.

---

## 📈 Metodologi Pembelajaran Mesin

1. **Preprocessing Data Pipeline**:
   - `StandardScaler`: Normalisasi fitur skala numerik (`usia`, `omset`, `jumlah_pinjaman`, `tenor_pinjaman_(bulan)`, `jumlah_anak`).
   - `OneHotEncoder`: Transformasi variabel kategorikal (`jenis_kelamin`, `status`) ke representasi numerik biner.
2. **Resampling Data (Handling Imbalanced Class)**:
   - `SMOTE` diintegrasikan langsung ke dalam `imblearn.pipeline.Pipeline` untuk mencegah kebocoran data (*data leakage*) selama validasi silang (*cross-validation*).
3. **Ensemble Modeling & Hyperparameter Tuning**:
   - Algoritma Dasar: **Random Forest** & **Bagging Classifier**.
   - Optimasi Parameter: Menggunakan `GridSearchCV` untuk mencari kombinasi parameter terbaik.
   - Penentuan Keputusan Akhir: **VotingClassifier (Hard Voting)** yang menggabungkan kedua estimator ter-tuning untuk menghasilkan prediksi yang lebih stabil, objektif, dan minim variansi.

---

##  Kontributor & Lisensi
Proyek ini dikembangkan untuk keperluan penelitian skripsi dan implementasi sistem pendukung keputusan penyaluran kredit UMKM.
Lisensi: Open-Source untuk tujuan edukasi dan riset.
