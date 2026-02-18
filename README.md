# 🎯 AI UTBK Readiness Dashboard

Aplikasi berbasis AI untuk menganalisis kesiapan siswa dalam menghadapi **UTBK (Ujian Tulis Berbasis Komputer)** secara holistik — mencakup aspek akademik, psikologis, dan kebiasaan belajar.

---

## 📌 Tentang Aplikasi

AI UTBK Readiness Dashboard adalah sistem analisis kesiapan UTBK yang dibangun menggunakan **Streamlit** dan model machine learning **LightGBM**. Aplikasi ini memberikan gambaran menyeluruh tentang kesiapan siswa dan merekomendasikan strategi belajar yang dipersonalisasi berdasarkan profil unik setiap pengguna.

---

## ✨ Fitur Utama

### 📊 Dashboard Komprehensif
- Skor kesiapan keseluruhan berdasarkan input akademik dan psikologis
- Estimasi peluang lolos ke kampus/jurusan yang dituju
- Visualisasi metrik performa secara real-time

### 🧠 Analisis Mendalam
- **Skor Akademik** — dihitung berdasarkan skor subtes TPS (PU, PPU, PBM, PK, LBI, LBE, PM) dengan bobot yang disesuaikan per jurusan
- **Stabilitas Mental** — evaluasi fokus, kepercayaan diri, kecemasan, dan distraksi
- **Indeks Konsistensi Belajar** — mengukur jam belajar, frekuensi latihan soal, tryout, dan review
- **Risiko Underperform** — deteksi dini potensi penurunan performa saat ujian

### 🚀 Rekomendasi Strategi Belajar (AI-Powered)
Menggunakan model **LightGBM Classifier** yang telah dilatih untuk memprediksi strategi belajar terbaik ke dalam 4 kategori:

| Kategori | Kondisi |
|----------|---------|
| 🔴 Intensif & Terstruktur | Kebiasaan belajar dan kondisi psikologis perlu ditingkatkan |
| 🟠 Penguatan Mental | Kebiasaan baik, namun psikologis perlu diperkuat |
| 🟡 Optimasi & Review | Siap namun perlu peningkatan evaluasi soal |
| 🟢 Pertahankan & Tingkatkan | Kebiasaan dan mental sudah sangat baik |

### 🎓 Analisis Jurusan
- Rekomendasi jurusan berdasarkan skor dan minat
- Bobot subtes yang disesuaikan untuk setiap kelompok jurusan (Kedokteran, Teknik, Saintek, Hukum, Ekonomi, dll.)
- Panduan memilih jurusan yang strategis

### 🏫 Peluang Kampus
- Analisis peluang lolos berdasarkan passing grade kampus tujuan
- Tampilan visual tingkat kompetisi

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| [Streamlit](https://streamlit.io) | Framework UI aplikasi web |
| [LightGBM](https://lightgbm.readthedocs.io) | Model ML untuk prediksi strategi belajar |
| [Pandas](https://pandas.pydata.org) | Pengolahan dan manipulasi data |
| [NumPy](https://numpy.org) | Komputasi numerik |
| Python 3.8+ | Bahasa pemrograman utama |

---

## 🚀 Cara Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/username/ai-utbk-dashboard.git
cd ai-utbk-dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Pastikan File Model Tersedia
Letakkan file model LightGBM (`lgbm_model_2_.pkl`) di direktori yang sama dengan `app.py`.

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

---

## 📋 Requirements

```
streamlit
lightgbm
pandas
numpy
scikit-learn
```

---

## 🧩 Struktur Proyek

```
ai-utbk-dashboard/
├── app.py                  # File utama aplikasi
├── lgbm_model_2_.pkl       # Model LightGBM (tidak disertakan di repo)
├── requirements.txt        # Daftar dependensi
└── README.md               # Dokumentasi ini
```

---

## 📥 Input yang Diperlukan

Pengguna mengisi data berikut melalui sidebar:

**Data Pribadi**
- Nama siswa
- Jurusan yang dituju
- Kampus tujuan

**Skor Subtes TPS**
- PU (Penalaran Umum)
- PPU (Pengetahuan dan Pemahaman Umum)
- PBM (Pemahaman Bacaan dan Menulis)
- PK (Pengetahuan Kuantitatif)
- LBI (Literasi Bahasa Indonesia)
- LBE (Literasi Bahasa Inggris)
- PM (Penalaran Matematika)

**Kebiasaan Belajar**
- Jam belajar per hari
- Hari belajar per minggu
- Frekuensi latihan soal
- Frekuensi tryout
- Intensitas review soal

**Kondisi Psikologis**
- Tingkat fokus
- Kepercayaan diri
- Tingkat kecemasan
- Tingkat distraksi

---

## 🤖 Tentang Model ML

Model LightGBM dilatih menggunakan **9 fitur** dari aspek kebiasaan belajar dan psikologis **(tanpa skor TPS)** untuk menghindari data leakage. Fitur yang digunakan:

- Jam_Belajar, Hari_Belajar, Latihan_Soal, Frekuensi_Tryout, Review_Soal
- Fokus, Percaya_Diri
- Kecemasan_Rev *(reverse scored)*
- Distraksi_Rev *(reverse scored)*

Model menghasilkan prediksi kelas strategi beserta probabilitas kepercayaan untuk setiap kategori.

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan edukasi. Silakan gunakan dan modifikasi sesuai kebutuhan.

---

> 💡 *"Perjalanan menuju UTBK adalah maraton, bukan sprint. Tetap konsisten, percaya pada proses, dan jangan pernah menyerah pada impian kamu!"*
