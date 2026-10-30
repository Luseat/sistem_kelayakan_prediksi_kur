# 🏦 Sistem Prediksi Kelayakan Kredit Usaha Rakyat (KUR) UMKM

Aplikasi berbasis web untuk memprediksi kelayakan dan risiko gagal bayar calon debitur Kredit Usaha Rakyat (KUR) di sektor UMKM. Sistem ini mengadopsi pendekatan **Hybrid Evaluation Architecture**: memadukan *Financial Hard Business Rule* (analisis rasio kapasitas angsuran perbankan), *Machine Learning Ensemble* (**Random Forest** + **Bagging Classifier** dengan teknik **Voting Classifier** & **SMOTE**), modul cerdas **What-If Recommendation Engine** untuk simulasi restrukturisasi kredit, serta fitur **Batch Evaluation via Upload CSV** untuk pemrosesan data massal.

---

## 📌 Latar Belakang & Masalah

Pemberian fasilitas kredit bagi pelaku Usaha Mikro, Kecil, dan Menengah (UMKM) memegang peranan krusial dalam pertumbuhan ekonomi daerah. Namun, proses evaluasi kelayakan kredit yang dilakukan secara manual sering kali menghadapi kendala:
- **Subjektivitas & Human Error**: Penilaian analis kredit berisiko inkonsisten antar-staf verifikator.
- **Efisiensi Waktu**: Proses analisis kelayakan berkas fisik memakan waktu yang cukup lama terutama saat menangani ratusan pemohon kredit.
- **Risiko Kredit Macet (NPL)**: Potensi kerugian finansial akibat salah meloloskan calon debitur berisiko gagal bayar tinggi (*False Positive*).
- **Ketiadaan Solusi Alternatif**: Penolakan kredit sering kali bersifat final tanpa memberikan opsi alternatif penyesuaian fasilitas pinjaman bagi nasabah yang potensial.

Sistem ini dikembangkan sebagai solusi otomatisasi analisis kredit yang objektif, transparan, cepat, dan presisi tinggi guna meminimalisir risiko kredit macet sekaligus memberikan rekomendasi finansial yang adaptif.

---

## 🚀 Fitur Utama & Cara Kerja Sistem (Hybrid Architecture)

Sistem mengadopsi antarmuka berbasis tab (*Dual-Tab Interface*) dengan arsitektur evaluasi dua lapis (*Dual-Layer Decision Model*):

```
                   [ Input Data: Form Individu / File CSV Massal ]
                                         │
                                         ▼
       ┌──────────────────────────────────────────────────────────────────┐
       │     Simulasi Pemrosesan & Anti-Spam Click (st.session_state)     │
       │    Proteksi dobel klik & pemrosesan profil risiko real-time      │
       └─────────────────────────────────┬────────────────────────────────┘
                                         │
                                         ▼
       ┌──────────────────────────────────────────────────────────────────┐
       │   📊 Kartu Ringkasan Kapasitas Finansial (Individu / Batch)      │
       │    - Estimasi Angsuran / Bulan (Rp)                              │
       │    - Debt Service Ratio / DSR (% vs batas aman 40%)              │
       │    - Sisa Omset Bersih (Status Surplus / Defisit)                │
       └─────────────────────────────────┬────────────────────────────────┘
                                         │
                                         ▼
       ┌──────────────────────────────────────────────────────────────────┐
       │       Lapis 1: Hard Business Rule (Rasio Finansial Bank)         │
       │         Cicilan per Bulan > 40% Omset Bulanan?                   │
       └─────────────────────────────────┬────────────────────────────────┘
                                         │
                         ┌───────────────┴───────────────┐
                        Ya                               Tidak
                         │                               │
                         ▼                               ▼
       ❌ REJECTED BY SYSTEM RULE           ┌─────────────────────────────┐
        (Kapasitas Finansial Kurang)        │ Lapis 2: Machine Learning   │
                         │                  │    Pipeline (Scikit-Learn)  │
                         ▼                  │  - Scaling & One-Hot Encode │
            What-If Recommendation Engine   │  - Voting Classifier        │
         - Opsi 1: Perpanjangan Tenor       │    (Random Forest + Bagging)│
         - Opsi 2: Penyesuaian Plafon       └──────────────┬──────────────┘
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

### 1. 📝 Tab 1: Evaluasi Individu (Single Entry)
- **Kartu Ringkasan Finansial (`st.metric`)**: Menampilkan estimasi angsuran bulanan, rasio beban cicilan (Debt Service Ratio / DSR dengan indikator warna dinamis), serta sisa omset bersih (status Surplus atau Defisit).
- **Lapis 1 - Hard Business Rule (Akal Sehat Finansial)**: Menolak pengajuan secara otomatis (*Rejected by System Rule*) jika rasio cicilan $> 40\%$ omset bulanan demi mencegah kredit macet.
- **What-If Recommendation Engine**: Memberikan solusi restrukturisasi kredit otomatis saat ditolak Lapis 1 (perhitungan tenor minimal rekomendasi dan plafon maksimal rekomendasi).
- **Lapis 2 - Machine Learning Ensemble Pipeline**: Evaluasi berbasis model konsensus *Hard Voting* (Random Forest + Bagging Classifier) dengan proteksi data leakage via SMOTE.
- **Saran Mitigasi Risiko**: Panduan verifikasi fisik lapangan, cek mutasi rekening, dan opsi agunan tambahan bagi debitur yang ditolak AI.

### 2. 📁 Tab 2: Evaluasi Massal via Upload CSV (Batch Processing)
- **Unduh Template CSV**: Menyediakan contoh berkas CSV bawaan agar pengguna dapat memastikan format header kolom sesuai sebelum mengunggah.
- **Validasi Header Otomatis**: Memeriksa kelengkapan seluruh fitur wajib data calon debitur sebelum pemrosesan dimulai.
- **High-Speed Batch Evaluation**: Memproses puluhan hingga ratusan data nasabah sekaligus dalam hitungan detik menggunakan vektorisasi Pandas.
- **Ringkasan Statistik Massal**: Kartu indikator metrik total calon debitur, total pengajuan disetujui (*Approved*), dan total pengajuan ditolak (*Rejected*).
- **Tabel Keputusan Lengkap & Unduh Laporan**: Menampilkan rincian cicilan per bulan, persentase rasio cicilan, status keputusan, dan alasan evaluasi, serta tombol unduh hasil (*Export to CSV*).

### 3. 🛡️ Validasi Anti-Spam Click (Idempotent Session State Lock)
- Menggunakan `st.session_state` untuk merekam sidik jari input data terakhir (*last input signature*).
- Jika pengguna menekan tombol evaluasi berkali-kali secara cepat (*spam click / double-click*), sistem cerdas melewati animasi delay 3.5 detik dan langsung menyajikan hasil secara instan tanpa mengulang antrean loading yang memperlambat sistem.

### 4. ✍️ Validasi Input Form Dinamis
- Input form angka dirancang tanpa nilai bawaan (*value=None*) disertai *placeholder* informatif, mengharuskan pengguna mengisi data secara manual.
- Dilengkapi sistem penahan (*input validation guardrail*) untuk mencegah eksekusi jika ada parameter yang belum diisi.

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
├── requirements.txt                               # Daftar dependensi & pustaka proyek
├── app.py                                         # Aplikasi web Streamlit (Dual-Tab UI, Hard Rule, & Integrasi AI)
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
Instalasi seluruh pustaka yang tercantum pada file `requirements.txt`:
```bash
pip install -r requirements.txt
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

## 👨‍💻 Kontributor & Lisensi
Proyek ini dikembangkan untuk keperluan penelitian skripsi dan implementasi sistem pendukung keputusan penyaluran kredit UMKM.
Lisensi: Open-Source untuk tujuan edukasi dan riset.
