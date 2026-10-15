# 🏦 Sistem Prediksi Kelayakan Kredit Usaha Rakyat (KUR) UMKM

Aplikasi berbasis web untuk memprediksi kelayakan dan risiko gagal bayar calon debitur Kredit Usaha Rakyat (KUR) di sektor UMKM. Sistem ini menggabungkan pendekatan **Hybrid Evaluation**: *Financial Hard Business Rule* (penilaian rasio kapasitas bayar) dan *Machine Learning Ensemble* (**Random Forest** + **Bagging Classifier** dengan teknik **Voting Classifier** & **SMOTE**).

---

## 📌 Latar Belakang & Masalah

Pemberian fasilitas kredit bagi pelaku Usaha Mikro, Kecil, dan Menengah (UMKM) memegang peranan krusial dalam pertumbuhan ekonomi daerah. Namun, proses evaluasi kelayakan kredit yang dilakukan secara manual sering kali menghadapi kendala:
- **Subjektivitas & Human Error**: Penilaian analis kredit berisiko inkonsisten antar-staf.
- **Efisiensi Waktu**: Waktu verifikasi dan analisis berkas membutuhkan proses panjang.
- **Risiko Kredit Macet (NPL)**: Potensi kerugian finansial akibat salah meloloskan calon debitur berisiko gagal bayar tinggi (*False Positive*).

Sistem ini dikembangkan sebagai solusi otomatisasi analisis kredit yang objektif, cepat, dan presisi tinggi dengan pendekatan dua lapis evaluasi.

---

## 🚀 Fitur Utama & Cara Kerja Sistem (Dual-Layer Evaluation)

Sistem mengadopsi arsitektur evaluasi dua lapis (*Hybrid Decision Model*):

```
                       [ Input Data Calon Debitur ]
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
                                       │    Pipeline (Scikit-Learn)  │
                                       │  - Scaling & One-Hot Encode │
                                       │  - Voting Classifier        │
                                       │    (Random Forest + Bagging)│
                                       └──────────────┬──────────────┘
                                                      │
                                      ┌───────────────┴───────────────┐
                                      ▼                               ▼
                           ✅ APPROVED BY AI               ❌ REJECTED BY AI
                        (Risiko Rendah / Layak)          (Pola Risiko Macet Tinggi)
```

1. **Lapis 1 - Financial Hard Rule (Akal Sehat Perbankan)**:
   - Menghitung rasio cicilan bulanan terhadap omset calon debitur.
   - Jika rasio cicilan melebihi **40% dari total omset per bulan**, pengajuan otomatis **ditolak (Rejected by System Rule)** tanpa membebani model AI.
2. **Lapis 2 - Machine Learning Ensemble Pipeline**:
   - Jika lolos uji finansial lapis 1, data diproses ke pipeline machine learning yang sudah dilatih.
   - Menggunakan kombinasi **Tuned Random Forest** dan **Tuned Bagging Classifier** melalui mekanisme **Hard Voting**.
   - Penanganan ketimpangan kelas (*imbalanced dataset*) ditangani menggunakan **SMOTE (Synthetic Minority Over-sampling Technique)** pada saat training untuk meningkatkan daya tangkap (*Recall*) terhadap debitur gagal bayar.
3. **Antarmuka Interaktif (Streamlit)**:
   - Form input ramah pengguna (*User Friendly*) dengan *placeholder* dan validasi nilai kosong (*None validation*).

---

## 📊 Atribut Data Input

| Parameter | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `usia` | Numerik | Usia calon debitur (18 - 100 tahun) |
| `jenis_kelamin` | Kategorikal | Laki-laki / Perempuan |
| `status` | Kategorikal | Status pekerjaan (Wirausaha / Karyawan) |
| `jumlah_anak` | Numerik | Jumlah tanggungan keluarga |
| `omset` | Numerik | Estimasi pendapatan / omset bersih per bulan (Rp) |
| `jumlah_pinjaman` | Numerik | Nominal pinjaman yang diajukan (Rp) |
| `tenor_pinjaman_(bulan)` | Numerik | Jangka waktu pengembalian pinjaman (Bulan) |
| `riwayat_telat_bayar` | Biner | Rekam jejak kredit sebelumnya (`0` = Tidak Pernah, `1` = Pernah) |

**Target Prediksi:**
- `0`: **Approved** (Risiko gagal bayar rendah / Layak diberikan)
- `1`: **Rejected** (Risiko gagal bayar tinggi / Tidak disarankan)

---

## 📂 Struktur Direktori Proyek

```text
kredit_usaha_rakyat/
│
├── .gitignore                                 # Mengabaikan file env, venv, cache pyc
├── app.py                                     # Aplikasi UI Streamlit & integrasi model
├── pembuatan_model_random_forest_&_bagging.ipynb  # Eksplorasi data, preprocessing, & training model
├── README.md                                  # Dokumentasi proyek
│
├── model/
│   └── model_kredit_usaha_rakyat.pkl          # Pipeline model ter-serialisasi (Scikit-Learn & ImbPipeline)
│
└── env/                                       # Virtual environment Python (lokal)
```

---

## 🛠️ Panduan Instalasi & Menjalankan Aplikasi

### 1. Klon Repositori
```bash
git clone https://github.com/Luseat/sistem_kelayakan_prediksi_kur.git
cd sistem_kelayakan_prediksi_kur
```

### 2. Siapkan Virtual Environment
Gunakan Python 3.10+ (disarankan mengisolasi pustaka via venv):
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
Aplikasi akan otomatis terbuka pada peramban web di alamat `http://localhost:8501`.

---

## 📈 Metodologi Pembelajaran Mesin

1. **Preprocessing Data**:
   - `StandardScaler` untuk normalisasi skala fitur numerik (`usia`, `omset`, `jumlah_pinjaman`, `tenor`, `jumlah_anak`).
   - `OneHotEncoder` untuk representasi fitur kategorikal (`jenis_kelamin`, `status`).
2. **Resampling Data**:
   - `SMOTE` diintegrasikan dalam `imblearn.pipeline.Pipeline` untuk mencegah kebocoran data (*data leakage*) selama validasi silang (*cross-validation*).
3. **Model Ensembling**:
   - Model utama: **VotingClassifier (Hard Voting)** yang menggabungkan estimator terbaik hasil *Hyperparameter Tuning* (GridSearchCV) dari:
     - `RandomForestClassifier`
     - `BaggingClassifier`

---

## 👨‍💻 Kontributor & Lisensi
Proyek ini dikembangkan untuk keperluan penelitian dan implementasi sistem pendukung keputusan penyaluran kredit UMKM.
Lisensi: Open-Source untuk tujuan edukasi dan riset.
