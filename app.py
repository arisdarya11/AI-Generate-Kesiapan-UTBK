"""
AI UTBK Readiness Dashboard
Sistem analisis kesiapan UTBK berbasis AI dengan pendekatan holistik
"""

import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
from typing import Dict, Tuple


# ======================================
# LOAD MODEL LGBM
# ======================================

@st.cache_resource
def load_lgbm_model():
    """Load model LightGBM dari file .pkl"""
    model_path = os.path.join(os.path.dirname(__file__), "lgbm_model_2_.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model, True
    except FileNotFoundError:
        return None, False
    except Exception as e:
        st.warning(f"⚠️ Model LGBM tidak dapat dimuat: {e}. Menggunakan kalkulasi manual.")
        return None, False


LABEL_STRATEGI = [
    "Intensif & Terstruktur",
    "Penguatan Mental",
    "Optimasi & Review",
    "Pertahankan & Tingkatkan"
]

DESKRIPSI_STRATEGI = {
    "Intensif & Terstruktur": {
        "icon": "🔴",
        "deskripsi": "Kebiasaan belajar dan kondisi psikologis perlu ditingkatkan secara bersamaan.",
        "tips": [
            "Buat jadwal belajar harian yang ketat dan konsisten",
            "Mulai dari 2 jam/hari lalu tingkatkan bertahap",
            "Gunakan metode Pomodoro (25 menit fokus, 5 menit istirahat)",
            "Cari teman belajar atau bergabung dengan kelompok belajar",
            "Konsultasi dengan guru/mentor untuk panduan belajar"
        ]
    },
    "Penguatan Mental": {
        "icon": "🟠",
        "deskripsi": "Kebiasaan belajar sudah cukup baik, namun kondisi psikologis perlu diperkuat.",
        "tips": [
            "Latihan mindfulness atau meditasi 10 menit sebelum belajar",
            "Buat target kecil harian agar rasa percaya diri meningkat",
            "Kurangi perbandingan diri dengan orang lain",
            "Tetapkan rutinitas tidur yang baik untuk mengurangi kecemasan",
            "Lakukan simulasi ujian (tryout) secara rutin untuk membiasakan diri"
        ]
    },
    "Optimasi & Review": {
        "icon": "🟡",
        "deskripsi": "Kebiasaan dan mental sudah baik, tingkatkan kualitas review dan evaluasi soal.",
        "tips": [
            "Perbanyak review soal-soal yang pernah salah",
            "Analisis pola kesalahan di setiap subtes",
            "Tingkatkan frekuensi tryout menjadi minimal 2x/bulan",
            "Buat catatan ringkasan materi yang sering keluar",
            "Fokus pada efisiensi waktu mengerjakan soal"
        ]
    },
    "Pertahankan & Tingkatkan": {
        "icon": "🟢",
        "deskripsi": "Kebiasaan belajar dan kondisi psikologis sudah sangat baik!",
        "tips": [
            "Pertahankan konsistensi dan jangan lengah",
            "Tingkatkan target skor tryout secara bertahap",
            "Mulai fokus pada strategi manajemen waktu saat ujian",
            "Bantu teman yang kesulitan — mengajar memperkuat pemahaman",
            "Jaga kesehatan fisik agar performa tetap optimal"
        ]
    }
}


def prediksi_lgbm(model, input_data: Dict) -> Dict:
    """
    Melakukan prediksi strategi belajar menggunakan model LightGBM Classifier.
    
    Fitur: 9 kolom kebiasaan belajar + psikologi (TANPA skor TPS — bebas leakage)
    Output: Rekomendasi strategi belajar (4 kategori)
    """
    try:
        # Susun 9 fitur — tanpa skor TPS
        fitur = pd.DataFrame([{
            "Jam_Belajar"      : input_data["jam_belajar"],
            "Hari_Belajar"     : input_data["hari_belajar"],
            "Latihan_Soal"     : input_data["latihan_soal"],
            "Frekuensi_Tryout" : input_data["frekuensi_tryout"],
            "Review_Soal"      : input_data["review_soal"],
            "Fokus"            : input_data["fokus"],
            "Percaya_Diri"     : input_data["percaya_diri"],
            "Kecemasan_Rev"    : 6 - input_data["kecemasan"],  # reverse scoring
            "Distraksi_Rev"    : 6 - input_data["distraksi"],  # reverse scoring
        }])

        # Sesuaikan urutan kolom dengan model
        if hasattr(model, "feature_name_"):
            fitur = fitur.reindex(columns=model.feature_name_, fill_value=0)
        elif hasattr(model, "feature_names_in_"):
            fitur = fitur.reindex(columns=model.feature_names_in_, fill_value=0)

        # Prediksi kelas & probabilitas
        kode_strategi = int(model.predict(fitur)[0])
        label_strategi = LABEL_STRATEGI[kode_strategi] if kode_strategi < len(LABEL_STRATEGI) else "Pertahankan & Tingkatkan"

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(fitur)[0]
            kepercayaan = float(proba[kode_strategi]) * 100
        else:
            proba = None
            kepercayaan = None

        return {
            "sukses"        : True,
            "kode"          : kode_strategi,
            "strategi"      : label_strategi,
            "kepercayaan"   : kepercayaan,
            "probabilitas"  : proba.tolist() if proba is not None else None,
            "detail"        : DESKRIPSI_STRATEGI.get(label_strategi, {})
        }

    except Exception as e:
        return {"sukses": False, "error": str(e)}


# ====================================== 
# KONFIGURASI APLIKASI
# ====================================== 

def setup_page():
    """Konfigurasi halaman aplikasi"""
    st.set_page_config(
        page_title="AI UTBK Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ====================================== 
# KONSTANTA DAN DATA
# ====================================== 

DAFTAR_JURUSAN = [
    "Kedokteran", "Kedokteran Gigi",
    "Teknik Sipil", "Teknik Mesin", "Teknik Elektro",
    "Teknik Industri", "Teknik Kimia", "Teknik Informatika",
    "Matematika", "Fisika", "Kimia", "Biologi",
    "Statistika", "Aktuaria",
    "Farmasi", "Gizi", "Keperawatan", "Kesehatan Masyarakat",
    "Ilmu Hukum",
    "Ekonomi", "Manajemen", "Akuntansi", "Bisnis",
    "Psikologi", "Ilmu Komunikasi", "Hubungan Internasional",
    "Administrasi Publik",
    "Sastra Inggris", "Pendidikan Bahasa Indonesia",
    "Pendidikan Bahasa Inggris",
    "Sosiologi", "Ilmu Politik", "Sejarah", "Geografi"
]

# Bobot untuk setiap kelompok jurusan
BOBOT_JURUSAN = {
    "kesehatan_utama": {
        "jurusan": ["Kedokteran", "Kedokteran Gigi"],
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.15, "LBI": 0.10, "LBE": 0.10, "PM": 0.20}
    },
    "teknik": {
        "jurusan": ["Teknik Sipil", "Teknik Mesin", "Teknik Elektro", "Teknik Industri", "Teknik Kimia", "Teknik Informatika"],
        "bobot": {"PU": 0.20, "PPU": 0.10, "PBM": 0.05, "PK": 0.20, "LBI": 0.05, "LBE": 0.10, "PM": 0.30}
    },
    "saintek_murni": {
        "jurusan": ["Matematika", "Fisika", "Kimia", "Biologi", "Statistika", "Aktuaria"],
        "bobot": {"PU": 0.20, "PPU": 0.10, "PBM": 0.05, "PK": 0.20, "LBI": 0.05, "LBE": 0.05, "PM": 0.35}
    },
    "kesehatan_terapan": {
        "jurusan": ["Farmasi", "Gizi", "Keperawatan", "Kesehatan Masyarakat"],
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.15, "LBI": 0.15, "LBE": 0.10, "PM": 0.15}
    },
    "hukum": {
        "jurusan": ["Ilmu Hukum"],
        "bobot": {"PU": 0.20, "PPU": 0.20, "PBM": 0.20, "PK": 0.05, "LBI": 0.20, "LBE": 0.10, "PM": 0.05}
    },
    "ekonomi_bisnis": {
        "jurusan": ["Ekonomi", "Manajemen", "Akuntansi", "Bisnis"],
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.20, "LBI": 0.10, "LBE": 0.10, "PM": 0.15}
    },
    "psikologi": {
        "jurusan": ["Psikologi"],
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.20, "PK": 0.10, "LBI": 0.15, "LBE": 0.10, "PM": 0.10}
    },
    "komunikasi_hubungan": {
        "jurusan": ["Ilmu Komunikasi", "Hubungan Internasional", "Administrasi Publik"],
        "bobot": {"PU": 0.15, "PPU": 0.20, "PBM": 0.20, "PK": 0.05, "LBI": 0.20, "LBE": 0.15, "PM": 0.05}
    },
    "bahasa": {
        "jurusan": ["Sastra Inggris", "Pendidikan Bahasa Indonesia", "Pendidikan Bahasa Inggris"],
        "bobot": {"PU": 0.10, "PPU": 0.15, "PBM": 0.25, "PK": 0.05, "LBI": 0.25, "LBE": 0.15, "PM": 0.05}
    },
    "sosial_humaniora": {
        "jurusan": ["Sosiologi", "Ilmu Politik", "Sejarah", "Geografi"],
        "bobot": {"PU": 0.15, "PPU": 0.20, "PBM": 0.25, "PK": 0.05, "LBI": 0.20, "LBE": 0.10, "PM": 0.05}
    },
    "default": {
        "jurusan": [],
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.15, "PK": 0.10, "LBI": 0.15, "LBE": 0.10, "PM": 0.15}
    }
}

# Data PTN Favorit dengan Klasterisasi
PTN_DATA = {
    "klaster_1": {
        "nama": "Klaster 1 - Top Tier",
        "universitas": [
            "Universitas Indonesia (UI)",
            "Universitas Gadjah Mada (UGM)",
            "Universitas Padjadjaran (Unpad)",
            "Institut Teknologi Bandung (ITB)",
            "Institut Pertanian Bogor (IPB)"
        ],
        "skor_aman": (640, 680),
        "warna": "🔴",
        "keterangan": "PTN dengan persaingan paling ketat dan standar tertinggi"
    },
    "klaster_2": {
        "nama": "Klaster 2 - Menengah Atas",
        "universitas": [
            "Universitas Diponegoro (Undip)",
            "Universitas Sebelas Maret (UNS)",
            "Universitas Brawijaya (UB)",
            "Universitas Airlangga (Unair)",
            "Institut Teknologi Sepuluh Nopember (ITS)",
            "Universitas Hasanuddin (Unhas)"
        ],
        "skor_aman": (580, 630),
        "warna": "🟠",
        "keterangan": "PTN favorit dengan standar tinggi"
    },
    "klaster_3": {
        "nama": "Klaster 3 - Menengah",
        "universitas": [
            "Universitas Negeri Yogyakarta (UNY)",
            "Universitas Negeri Semarang (UNNES)",
            "Universitas Negeri Malang (UM)",
            "Universitas Andalas (Unand)",
            "Universitas Sumatera Utara (USU)"
        ],
        "skor_aman": (530, 570),
        "warna": "🟡",
        "keterangan": "PTN dengan standar menengah dan persaingan moderat"
    },
    "klaster_4": {
        "nama": "Klaster 4 - PTN Regional",
        "universitas": [
            "Universitas Sriwijaya (Unsri)",
            "Universitas Lampung (Unila)",
            "Universitas Jember (Unej)",
            "Universitas Riau (Unri)"
        ],
        "skor_aman": (480, 520),
        "warna": "🟢",
        "keterangan": "PTN di luar Jawa dan PTN baru dengan peluang lebih besar"
    }
}

# Daftar semua PTN untuk selectbox (20 PTN)
DAFTAR_PTN = [
    "Universitas Indonesia (UI)",
    "Universitas Gadjah Mada (UGM)",
    "Universitas Padjadjaran (Unpad)",
    "Institut Teknologi Bandung (ITB)",
    "Institut Pertanian Bogor (IPB)",
    "Universitas Diponegoro (Undip)",
    "Universitas Sebelas Maret (UNS)",
    "Universitas Brawijaya (UB)",
    "Universitas Airlangga (Unair)",
    "Institut Teknologi Sepuluh Nopember (ITS)",
    "Universitas Hasanuddin (Unhas)",
    "Universitas Negeri Yogyakarta (UNY)",
    "Universitas Negeri Semarang (UNNES)",
    "Universitas Negeri Malang (UM)",
    "Universitas Andalas (Unand)",
    "Universitas Sumatera Utara (USU)",
    "Universitas Sriwijaya (Unsri)",
    "Universitas Lampung (Unila)",
    "Universitas Jember (Unej)",
    "Universitas Riau (Unri)"
]


# ====================================== 
# FUNGSI PERHITUNGAN AKADEMIK
# ====================================== 

def get_bobot_jurusan(jurusan: str) -> Dict[str, float]:
    """Mendapatkan bobot untuk jurusan tertentu"""
    for kategori, data in BOBOT_JURUSAN.items():
        if jurusan in data["jurusan"]:
            return data["bobot"]
    return BOBOT_JURUSAN["default"]["bobot"]


def hitung_skor_akademik(jurusan: str, PU: int, PPU: int, PBM: int, 
                         PK: int, LBI: int, LBE: int, PM: int) -> float:
    """
    Menghitung skor akademik berdasarkan bobot jurusan
    
    Args:
        jurusan: Nama jurusan target
        PU, PPU, PBM, PK, LBI, LBE, PM: Skor masing-masing subtes
        
    Returns:
        Skor akademik tertimbang
    """
    bobot = get_bobot_jurusan(jurusan)
    
    skor = (
        bobot["PU"] * PU +
        bobot["PPU"] * PPU +
        bobot["PBM"] * PBM +
        bobot["PK"] * PK +
        bobot["LBI"] * LBI +
        bobot["LBE"] * LBE +
        bobot["PM"] * PM
    )
    
    return skor


def hitung_skor_psikologis(fokus: int, percaya_diri: int, 
                          kecemasan: int, distraksi: int) -> float:
    """
    Menghitung skor psikologis dari faktor mental
    
    Args:
        fokus: Tingkat fokus (1-5)
        percaya_diri: Tingkat percaya diri (1-5)
        kecemasan: Tingkat kecemasan (1-5)
        distraksi: Tingkat distraksi (1-5)
        
    Returns:
        Skor psikologis (0-100)
    """
    skor = (
        fokus * 1.2 + 
        percaya_diri * 1.2 + 
        (6 - kecemasan) + 
        (6 - distraksi)
    ) * 5
    
    return skor


def hitung_skor_kesiapan(skor_akademik: float, skor_psikologis: float, 
                        skor_kebiasaan: float = 0) -> float:
    """
    Menghitung skor kesiapan total (gabungan akademik, psikologis, dan kebiasaan belajar)
    
    Args:
        skor_akademik: Skor akademik tertimbang
        skor_psikologis: Skor psikologis
        skor_kebiasaan: Skor kebiasaan belajar (opsional)
        
    Returns:
        Skor kesiapan total (0-100)
    """
    if skor_kebiasaan > 0:
        # Dengan kebiasaan belajar: 50% akademik, 25% psikologis, 25% kebiasaan
        return 0.5 * (skor_akademik / 10) + 0.25 * skor_psikologis + 0.25 * skor_kebiasaan
    else:
        # Tanpa kebiasaan belajar: 70% akademik, 30% psikologis
        return 0.7 * (skor_akademik / 10) + 0.3 * skor_psikologis


def hitung_peluang_lolos_lgbm(skor_akademik: float, kampus: str, 
                               lgbm_peluang: float = None) -> Tuple[float, str, str]:
    """
    Menghitung peluang lolos dengan mempertimbangkan prediksi model LGBM.
    Jika LGBM tersedia, hasilnya digabungkan dengan perhitungan manual (60% LGBM, 40% manual).
    """
    # Hitung manual terlebih dahulu
    peluang_manual, _, _ = hitung_peluang_lolos(skor_akademik, kampus)
    
    if lgbm_peluang is not None:
        # Gabungkan: 60% dari LGBM, 40% dari formula manual
        peluang_final = 0.6 * lgbm_peluang + 0.4 * peluang_manual
    else:
        peluang_final = peluang_manual
    
    # Tentukan kategori
    if peluang_final >= 0.75:
        kategori = "Sangat Tinggi"
        keterangan = f"Prediksi AI menunjukkan peluang sangat besar untuk diterima ({peluang_final*100:.0f}%)"
    elif peluang_final >= 0.60:
        kategori = "Tinggi"
        keterangan = f"Prediksi AI menunjukkan peluang cukup besar untuk diterima ({peluang_final*100:.0f}%)"
    elif peluang_final >= 0.40:
        kategori = "Sedang"
        keterangan = f"Prediksi AI menunjukkan peluang moderat, perlu peningkatan ({peluang_final*100:.0f}%)"
    elif peluang_final >= 0.25:
        kategori = "Rendah"
        keterangan = f"Prediksi AI menunjukkan peluang masih rendah, tingkatkan persiapan ({peluang_final*100:.0f}%)"
    else:
        kategori = "Sangat Rendah"
        keterangan = f"Prediksi AI menunjukkan peluang sangat kecil, butuh perbaikan signifikan ({peluang_final*100:.0f}%)"
    
    return peluang_final, kategori, keterangan


def hitung_peluang_lolos(skor_akademik: float, kampus: str) -> Tuple[float, str, str]:
    """
    Menghitung peluang lolos MURNI dari skor TPS vs threshold kampus
    
    Args:
        skor_akademik: Skor akademik tertimbang
        kampus: Nama kampus target
        
    Returns:
        Tuple (persentase_peluang, kategori, keterangan)
    """
    klaster = get_klaster_kampus(kampus)
    skor_min = klaster["skor_min"]
    skor_max = klaster["skor_max"]
    
    # Hitung peluang berdasarkan posisi skor
    if skor_akademik >= skor_max:
        peluang = 0.85
        kategori = "Sangat Tinggi"
        keterangan = f"Skor kamu ({skor_akademik:.0f}) berada di atas batas aman maksimum ({skor_max})"
    elif skor_akademik >= skor_min:
        # Linear interpolation antara min dan max
        progress = (skor_akademik - skor_min) / (skor_max - skor_min)
        peluang = 0.65 + (progress * 0.15)  # 65% - 80%
        kategori = "Tinggi"
        keterangan = f"Skor kamu ({skor_akademik:.0f}) berada dalam zona aman ({skor_min}-{skor_max})"
    elif skor_akademik >= skor_min - 30:
        # Zona kompetitif
        gap = skor_min - skor_akademik
        peluang = 0.40 + ((30 - gap) / 30 * 0.20)  # 40% - 60%
        kategori = "Sedang"
        keterangan = f"Skor kamu ({skor_akademik:.0f}) mendekati zona aman, butuh +{gap:.0f} poin"
    elif skor_akademik >= skor_min - 60:
        # Zona berisiko rendah
        gap = skor_min - skor_akademik
        peluang = 0.20 + ((60 - gap) / 30 * 0.15)  # 20% - 35%
        kategori = "Rendah"
        keterangan = f"Skor kamu ({skor_akademik:.0f}) masih {gap:.0f} poin di bawah zona aman"
    else:
        # Zona berisiko tinggi
        gap = skor_min - skor_akademik
        peluang = 0.15
        kategori = "Sangat Rendah"
        keterangan = f"Skor kamu ({skor_akademik:.0f}) masih {gap:.0f} poin di bawah zona aman"
    
    return peluang, kategori, keterangan


def hitung_stabilitas_mental(fokus: int, percaya_diri: int, 
                             kecemasan: int, distraksi: int) -> Tuple[float, str, str]:
    """
    Menghitung stabilitas mental (kemampuan perform konsisten saat ujian)
    
    Returns:
        Tuple (skor_stabilitas, kategori, keterangan)
    """
    # Faktor positif
    positif = (fokus * 1.5 + percaya_diri * 1.5) * 10
    
    # Faktor negatif
    negatif = (kecemasan * 1.2 + distraksi * 1.2) * 8
    
    # Skor stabilitas (0-100)
    stabilitas = max(0, min(100, positif - negatif + 50))
    
    if stabilitas >= 80:
        kategori = "Sangat Stabil"
        keterangan = "Mental kamu sangat siap menghadapi tekanan ujian"
    elif stabilitas >= 65:
        kategori = "Stabil"
        keterangan = "Mental kamu cukup stabil, pertahankan kondisi ini"
    elif stabilitas >= 50:
        kategori = "Cukup Stabil"
        keterangan = "Mental perlu penguatan untuk hasil maksimal"
    else:
        kategori = "Kurang Stabil"
        keterangan = "Mental memerlukan perhatian serius untuk menghindari underperform"
    
    return stabilitas, kategori, keterangan


def hitung_indeks_konsistensi(jam_belajar: int, hari_belajar: int, 
                              latihan_soal: int, frekuensi_tryout: int, 
                              review_soal: int) -> Tuple[float, str, str]:
    """
    Menghitung indeks konsistensi belajar (kemampuan maintain/improve skor)
    
    Returns:
        Tuple (indeks_konsistensi, kategori, keterangan)
    """
    # Weighted scoring
    skor = (
        jam_belajar * 2.0 +      # Durasi belajar
        hari_belajar * 2.2 +     # Konsistensi (paling penting)
        latihan_soal * 1.8 +     # Practice
        frekuensi_tryout * 1.5 + # Simulasi
        review_soal * 1.5        # Evaluasi
    ) * 2.0  # Normalisasi ke 0-100
    
    # Cap at 100
    konsistensi = min(100, skor)
    
    if konsistensi >= 80:
        kategori = "Sangat Konsisten"
        keterangan = "Pola belajar kamu sangat mendukung peningkatan skor"
    elif konsistensi >= 65:
        kategori = "Konsisten"
        keterangan = "Pola belajar sudah baik, tingkatkan untuk hasil optimal"
    elif konsistensi >= 50:
        kategori = "Cukup Konsisten"
        keterangan = "Pola belajar perlu ditingkatkan untuk maintain skor"
    else:
        kategori = "Kurang Konsisten"
        keterangan = "Pola belajar berisiko menyebabkan skor tidak stabil"
    
    return konsistensi, kategori, keterangan


def hitung_risiko_underperform(stabilitas_mental: float, 
                               konsistensi_belajar: float) -> Tuple[str, str, str]:
    """
    Menghitung risiko underperform saat ujian
    
    Returns:
        Tuple (level_risiko, emoji, keterangan)
    """
    # Gabungan stabilitas mental dan konsistensi
    skor_gabungan = (stabilitas_mental * 0.6 + konsistensi_belajar * 0.4)
    
    if skor_gabungan >= 75:
        level = "Rendah"
        emoji = "✅"
        keterangan = "Kemungkinan besar kamu akan perform sesuai atau di atas kemampuan"
    elif skor_gabungan >= 60:
        level = "Sedang"
        emoji = "⚠️"
        keterangan = "Ada potensi fluktuasi performa, jaga konsistensi"
    else:
        level = "Tinggi"
        emoji = "🔴"
        keterangan = "Risiko tinggi perform di bawah kemampuan, perlu perbaikan mental & kebiasaan"
    
    return level, emoji, keterangan


def hitung_risiko(fokus: int, percaya_diri: int, 
                 kecemasan: int, distraksi: int) -> Tuple[float, str, str]:
    """
    Menghitung tingkat risiko performa
    
    Returns:
        Tuple (nilai_risiko, level_risiko, keterangan)
    """
    risiko = (
        kecemasan * 2 + 
        distraksi * 2 + 
        (6 - fokus) * 1.5 + 
        (6 - percaya_diri) * 1.5
    )
    
    if risiko >= 20:
        level = "Tinggi"
        keterangan = "sangat berpotensi menurunkan performa secara signifikan"
    elif risiko >= 14:
        level = "Menengah"
        keterangan = "dapat menyebabkan fluktuasi hasil"
    else:
        level = "Rendah"
        keterangan = "mendukung kestabilan performa"
    
    return risiko, level, keterangan


def hitung_skor_kebiasaan_belajar(jam_belajar: int, hari_belajar: int, 
                                   latihan_soal: int, frekuensi_tryout: int, 
                                   review_soal: int) -> Tuple[float, str, str]:
    """
    Menghitung skor kebiasaan belajar dan memberikan evaluasi
    
    Args:
        jam_belajar: Rata-rata jam belajar per hari (1-5)
        hari_belajar: Hari belajar per minggu (1-5)
        latihan_soal: Frekuensi latihan soal per minggu (1-5)
        frekuensi_tryout: Frekuensi tryout per bulan (1-5)
        review_soal: Frekuensi review soal per minggu (1-5)
        
    Returns:
        Tuple (skor_total, kategori, keterangan)
    """
    # Bobot untuk setiap aspek
    skor = (
        jam_belajar * 2.0 +      # Jam belajar paling penting
        hari_belajar * 1.8 +     # Konsistensi hari belajar
        latihan_soal * 1.5 +     # Frekuensi latihan soal
        frekuensi_tryout * 1.2 + # Tryout sebagai simulasi
        review_soal * 1.5        # Review untuk perbaikan
    ) * 2.5  # Normalisasi ke skala 0-100
    
    # Kategorisasi
    if skor >= 75:
        kategori = "Excellent"
        keterangan = "Pola belajar kamu sudah sangat optimal dan disiplin"
        emoji = "🌟"
    elif skor >= 60:
        kategori = "Baik"
        keterangan = "Pola belajar kamu sudah cukup baik, tingkatkan konsistensi"
        emoji = "✅"
    elif skor >= 45:
        kategori = "Cukup"
        keterangan = "Pola belajar perlu ditingkatkan untuk hasil maksimal"
        emoji = "⚠️"
    else:
        kategori = "Perlu Perbaikan"
        keterangan = "Pola belajar perlu perhatian serius dan peningkatan signifikan"
        emoji = "🔴"
    
    return skor, kategori, keterangan, emoji


def klasifikasi_profil(fokus: int, percaya_diri: int, 
                      kecemasan: int, distraksi: int) -> str:
    """Mengklasifikasikan profil belajar siswa"""
    if fokus >= 4 and percaya_diri >= 4 and kecemasan <= 2:
        return "Stabil dan Percaya Diri"
    elif kecemasan >= 4 and percaya_diri <= 3:
        return "Cenderung Overthinking"
    elif distraksi >= 4:
        return "Potensial namun Kurang Konsisten"
    elif fokus >= 3 and percaya_diri >= 3:
        return "Sedang Berkembang"
    else:
        return "Perlu Penguatan Fundamental"


def get_klaster_kampus(kampus: str) -> Dict:
    """
    Mendapatkan informasi klaster dari kampus yang dipilih
    
    Args:
        kampus: Nama kampus yang dipilih
        
    Returns:
        Dictionary berisi informasi klaster
    """
    for klaster_id, data in PTN_DATA.items():
        if kampus in data["universitas"]:
            return {
                "id": klaster_id,
                "nama": data["nama"],
                "skor_min": data["skor_aman"][0],
                "skor_max": data["skor_aman"][1],
                "warna": data["warna"],
                "keterangan": data["keterangan"]
            }
    
    # Default jika tidak ditemukan
    return {
        "id": "klaster_3",
        "nama": "Klaster 3 - Menengah",
        "skor_min": 530,
        "skor_max": 570,
        "warna": "🟡",
        "keterangan": "PTN dengan standar menengah"
    }


def analisis_peluang_kampus(skor_akademik: float, kampus: str) -> Dict:
    """
    Menganalisis peluang masuk ke kampus berdasarkan skor akademik
    
    Args:
        skor_akademik: Skor akademik tertimbang
        kampus: Nama kampus target
        
    Returns:
        Dictionary berisi analisis peluang
    """
    klaster = get_klaster_kampus(kampus)
    skor_min = klaster["skor_min"]
    skor_max = klaster["skor_max"]
    
    # Hitung selisih skor
    selisih_min = skor_akademik - skor_min
    selisih_max = skor_akademik - skor_max
    
    # Tentukan kategori peluang
    if skor_akademik >= skor_max:
        kategori = "Sangat Aman"
        warna_status = "success"
        emoji = "🎯"
        persentase = 85
        keterangan = f"Skor kamu berada di atas ambang batas aman ({skor_max}). Peluang sangat besar!"
    elif skor_akademik >= skor_min:
        kategori = "Aman"
        warna_status = "success"
        emoji = "✅"
        persentase = 70
        keterangan = f"Skor kamu berada dalam rentang aman ({skor_min}-{skor_max}). Peluang cukup besar!"
    elif skor_akademik >= skor_min - 30:
        kategori = "Kompetitif"
        warna_status = "warning"
        emoji = "⚠️"
        persentase = 50
        keterangan = f"Skor kamu mendekati batas aman. Butuh {skor_min - skor_akademik:.0f} poin lagi untuk masuk zona aman."
    else:
        kategori = "Perlu Peningkatan"
        warna_status = "error"
        emoji = "🔴"
        persentase = 30
        keterangan = f"Skor kamu masih {skor_min - skor_akademik:.0f} poin di bawah batas aman. Tingkatkan persiapan secara intensif."
    
    return {
        "kategori": kategori,
        "warna_status": warna_status,
        "emoji": emoji,
        "persentase": persentase,
        "keterangan": keterangan,
        "selisih_min": selisih_min,
        "selisih_max": selisih_max,
        "klaster": klaster
    }


# ====================================== 
# FUNGSI UI COMPONENTS
# ====================================== 

def render_header(nama: str = "", show_greeting: bool = False):
    """Render header aplikasi dengan salam personal atau perkenalan umum"""
    st.title("🎯 AI UTBK Readiness Dashboard")
    
    # Salam personal jika sudah klik prediksi dan nama sudah diisi
    if show_greeting and nama:
        import datetime
        jam = datetime.datetime.now().hour
        
        if jam < 11:
            salam = "Selamat pagi"
        elif jam < 15:
            salam = "Selamat siang"
        elif jam < 18:
            salam = "Selamat sore"
        else:
            salam = "Selamat malam"
        
        st.markdown(f"### {salam}, **{nama}**! 👋")
        
        st.info("""
        🤖 **Perkenalkan, saya adalah Asisten AI UTBK**
        
        Saya hadir untuk membantu kamu menganalisis kesiapan menghadapi UTBK secara komprehensif. 
        Dengan memanfaatkan teknologi kecerdasan buatan, saya akan:
        
        - 📊 Menganalisis performa akademik berdasarkan skor TPS kamu
        - 🧠 Mengevaluasi kondisi psikologis dan kesiapan mental
        - ⚠️ Mengidentifikasi potensi risiko yang dapat memengaruhi hasil ujian
        - 🎯 Memberikan rekomendasi strategi belajar yang dipersonalisasi
        - 🎓 Menyarankan pilihan jurusan berdasarkan kemampuan dan peluang
        
        Mari kita mulai perjalanan persiapan UTBK kamu dengan data-driven approach untuk hasil yang optimal!
        """)
    elif show_greeting and not nama:
        # Jika sudah klik prediksi tapi nama belum diisi
        st.info("""
        🤖 **Perkenalkan, saya adalah Asisten AI UTBK**
        
        Saya hadir untuk membantu kamu menganalisis kesiapan menghadapi UTBK secara komprehensif. 
        Dengan memanfaatkan teknologi kecerdasan buatan, saya akan:
        
        - 📊 Menganalisis performa akademik berdasarkan skor TPS kamu
        - 🧠 Mengevaluasi kondisi psikologis dan kesiapan mental
        - ⚠️ Mengidentifikasi potensi risiko yang dapat memengaruhi hasil ujian
        - 🎯 Memberikan rekomendasi strategi belajar yang dipersonalisasi
        - 🎓 Menyarankan pilihan jurusan berdasarkan kemampuan dan peluang
        
        Mari kita mulai perjalanan persiapan UTBK kamu dengan data-driven approach untuk hasil yang optimal!
        """)
    else:
        # Tampilan awal sebelum klik prediksi
        st.markdown("""
        ### Selamat datang di AI UTBK Readiness Dashboard! 👋
        """)
        
        st.info("""
        🤖 **Perkenalkan, saya adalah Asisten AI UTBK**
        
        Saya adalah sistem kecerdasan buatan yang dirancang khusus untuk membantu siswa 
        mempersiapkan diri menghadapi UTBK dengan pendekatan yang komprehensif dan personal.
        
        **Apa yang bisa saya lakukan untuk kamu?**
        
        📊 **Analisis Akademik Mendalam**  
        Mengevaluasi performa kamu di semua subtes TPS dan memberikan penilaian tertimbang 
        sesuai dengan jurusan yang kamu targetkan.
        
        🧠 **Evaluasi Psikologis**  
        Mengukur kesiapan mental, tingkat fokus, kepercayaan diri, dan faktor-faktor 
        psikologis lain yang mempengaruhi performa ujian.
        
        📚 **Analisis Kebiasaan Belajar**  
        Menilai pola belajar kamu dan memberikan rekomendasi konkret untuk peningkatan 
        yang terukur dan efektif.
        
        ⚠️ **Identifikasi Risiko**  
        Mendeteksi potensi hambatan yang bisa mempengaruhi hasil ujian dan memberikan 
        strategi mitigasi yang tepat.
        
        🎯 **Strategi Personal**  
        Menyusun rencana belajar yang disesuaikan dengan profil unik kamu, lengkap dengan 
        timeline dan target yang realistis.
        
        🎓 **Rekomendasi Jurusan**  
        Memberikan saran pilihan jurusan alternatif berdasarkan analisis peluang dan 
        kemampuan akademik kamu.
        
        ---
        
        **Cara Menggunakan:**
        
        1. 📝 Isi semua data di sidebar sebelah kiri (Profil, Skor TPS, Psikologi, Kebiasaan Belajar)
        2. 🎯 Klik tombol **"CEK PREDIKSI SEKARANG"** di bagian bawah sidebar
        3. 📊 Lihat hasil analisis lengkap dan rekomendasi personal untuk kamu
        
        Mari kita mulai perjalanan persiapan UTBK yang terstruktur dan berbasis data! 🚀
        """)
        
        st.warning("⚠️ **Penting:** Pastikan semua data sudah diisi dengan lengkap dan jujur untuk mendapatkan hasil analisis yang akurat.")
    
    st.divider()


def render_sidebar() -> Dict:
    """
    Render sidebar dan kumpulkan input dari user
    
    Returns:
        Dictionary berisi semua input user
    """
    with st.sidebar:
        st.header("🎓 Profil Siswa")
        
        nama = st.text_input("Nama")
        jurusan = st.selectbox("Target Jurusan", DAFTAR_JURUSAN)
        kampus = st.selectbox("Target Kampus (PTN)", DAFTAR_PTN)
        
        st.divider()
        st.subheader("📊 Skor TPS")
        
        PU = st.slider("Penalaran Umum (PU)", 200, 900, 500)
        PPU = st.slider("Pemahaman & Penulisan Umum (PPU)", 200, 900, 500)
        PBM = st.slider("Pemahaman Bacaan & Menulis (PBM)", 200, 900, 500)
        PK = st.slider("Pengetahuan Kuantitatif (PK)", 200, 900, 500)
        LBI = st.slider("Literasi Bahasa Indonesia (LBI)", 200, 900, 500)
        LBE = st.slider("Literasi Bahasa Inggris (LBE)", 200, 900, 500)
        PM = st.slider("Penalaran Matematika (PM)", 200, 900, 500)
        
        st.divider()
        st.subheader("🧠 Faktor Psikologi")
        
        fokus = st.slider("Tingkat Fokus", 1, 5, 3, help="1 = Sangat rendah, 5 = Sangat tinggi")
        percaya_diri = st.slider("Percaya Diri", 1, 5, 3)
        kecemasan = st.slider("Tingkat Kecemasan", 1, 5, 3, help="1 = Sangat rendah, 5 = Sangat tinggi")
        distraksi = st.slider("Tingkat Distraksi", 1, 5, 3)
        
        st.divider()
        st.subheader("📚 Kebiasaan Belajar")
        
        jam_belajar = st.selectbox("Rata-rata jam belajar/hari:", ["<1 jam", "1-2 jam", "3-4 jam", "5-6 jam", ">6 jam"])
        map_jam = {"<1 jam": 1, "1-2 jam": 2, "3-4 jam": 3, "5-6 jam": 4, ">6 jam": 5}
        Jam_Belajar = map_jam[jam_belajar]
        
        hari_belajar = st.selectbox("Hari belajar/minggu:", ["<=1", "2", "3", "4-5", ">=6"])
        map_hari = {"<=1": 1, "2": 2, "3": 3, "4-5": 4, ">=6": 5}
        Hari_Belajar = map_hari[hari_belajar]
        
        Latihan_Soal = st.slider("Frekuensi latihan soal/minggu:", 1, 5, 3)
        
        Frekuensi_Tryout = st.slider("Frekuensi tryout/bulan:", 1, 5, 2)
        
        review = st.selectbox("Frekuensi review soal/minggu:", ["<=1", "2", "3", "4-5", ">=6"])
        Review_Soal = map_hari[review]
        
        st.divider()
        
        # Tombol Cek Prediksi
        cek_prediksi = st.button("🎯 CEK PREDIKSI SEKARANG", type="primary", use_container_width=True)
    
    return {
        "nama": nama,
        "jurusan": jurusan,
        "kampus": kampus,
        "PU": PU, "PPU": PPU, "PBM": PBM, "PK": PK,
        "LBI": LBI, "LBE": LBE, "PM": PM,
        "fokus": fokus,
        "percaya_diri": percaya_diri,
        "kecemasan": kecemasan,
        "distraksi": distraksi,
        "jam_belajar": Jam_Belajar,
        "hari_belajar": Hari_Belajar,
        "latihan_soal": Latihan_Soal,
        "frekuensi_tryout": Frekuensi_Tryout,
        "review_soal": Review_Soal,
        "cek_prediksi": cek_prediksi
    }


def render_metric_card(title: str, value: str, description: str, icon: str):
    """Render kartu metrik"""
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        st.metric("", value)
        st.caption(description)


def render_dashboard(data: Dict):
    """Render dashboard utama dengan 4 metrik terpisah"""
    st.subheader("📊 Dashboard Utama")
    
    # Tampilkan rekomendasi strategi dari model LGBM
    if data.get('lgbm_tersedia') and data.get('lgbm_hasil') and data['lgbm_hasil']['sukses']:
        hasil = data['lgbm_hasil']
        detail = hasil.get('detail', {})
        icon = detail.get('icon', '🤖')
        kepercayaan = f"{hasil['kepercayaan']:.1f}%" if hasil.get('kepercayaan') else ""
        st.success(f"""
        🤖 **Model AI LightGBM Aktif** — Rekomendasi Strategi Belajar:
        
        {icon} **{hasil['strategi']}** (Kepercayaan model: {kepercayaan})
        
        _{detail.get('deskripsi', '')}_
        """)
        if detail.get('tips'):
            with st.expander("📋 Lihat Tips Strategi Belajar dari AI"):
                for tip in detail['tips']:
                    st.write(f"- {tip}")
    elif data.get('lgbm_tersedia') and data.get('lgbm_hasil') and not data['lgbm_hasil']['sukses']:
        st.warning(f"⚠️ Model LGBM gagal: {data['lgbm_hasil'].get('error', '')}. Menggunakan kalkulasi manual.")
    else:
        st.info("📊 Peluang lolos dihitung menggunakan kalkulasi skor TPS vs passing grade kampus.")
    
    # Info box untuk penjelasan metrik
    st.info("""
    💡 **Penjelasan Metrik:**
    - **Peluang Lolos**: Kombinasi prediksi AI LightGBM + skor TPS vs passing grade kampus target
    - **Stabilitas Mental**: Kemampuan kamu untuk perform konsisten di bawah tekanan
    - **Konsistensi Belajar**: Seberapa baik pola belajar mendukung peningkatan skor
    - **Risiko**: Potensi perform di bawah kemampuan saat ujian sebenarnya
    """)
    
    st.markdown("---")
    
    # Row 1: Peluang & Stabilitas
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🎯 Peluang Lolos PTN")
            st.markdown(f"<h1 style='text-align: center; color: {'green' if data['peluang'] >= 0.65 else 'orange' if data['peluang'] >= 0.40 else 'red'};'>{data['peluang']*100:.0f}%</h1>", unsafe_allow_html=True)
            st.markdown(f"**Kategori:** {data['peluang_kategori']}")
            st.caption(f"📊 {data['peluang_keterangan']}")
            st.caption("*Berdasarkan skor TPS tertimbang vs passing grade kampus*")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🧠 Stabilitas Mental")
            st.markdown(f"<h1 style='text-align: center; color: {'green' if data['stabilitas'] >= 65 else 'orange' if data['stabilitas'] >= 50 else 'red'};'>{data['stabilitas']:.0f}%</h1>", unsafe_allow_html=True)
            st.markdown(f"**Kategori:** {data['stabilitas_kategori']}")
            st.caption(f"🧠 {data['stabilitas_keterangan']}")
            st.caption("*Kemampuan perform konsisten saat ujian*")
    
    # Row 2: Konsistensi & Risiko
    col3, col4 = st.columns(2)
    
    with col3:
        with st.container(border=True):
            st.markdown("### 📚 Konsistensi Belajar")
            st.markdown(f"<h1 style='text-align: center; color: {'green' if data['konsistensi'] >= 65 else 'orange' if data['konsistensi'] >= 50 else 'red'};'>{data['konsistensi']:.0f}%</h1>", unsafe_allow_html=True)
            st.markdown(f"**Kategori:** {data['konsistensi_kategori']}")
            st.caption(f"📖 {data['konsistensi_keterangan']}")
            st.caption("*Pola belajar mendukung peningkatan skor*")
    
    with col4:
        with st.container(border=True):
            st.markdown("### ⚠️ Risiko Underperform")
            st.markdown(f"<h1 style='text-align: center;'>{data['risiko_emoji']} {data['risiko_level']}</h1>", unsafe_allow_html=True)
            st.caption(f"⚡ {data['risiko_keterangan']}")
            st.caption("*Potensi perform di bawah kemampuan*")
    
    # Progress bar untuk skor akademik
    st.markdown("---")
    st.markdown("### 📊 Skor Akademik Tertimbang")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.progress(min(data['akademik'] / 900, 1.0))
    with col_b:
        st.metric("Skor", f"{data['akademik']:.0f}", delta="dari 900")
    
    st.caption(f"Skor ini sudah disesuaikan dengan bobot jurusan **{data['jurusan']}**")


# ====================================== 
# FUNGSI KONTEN TAB
# ====================================== 

def render_tab_peluang_kampus(data: Dict):
    """Render tab analisis peluang kampus dengan alternatif lengkap"""
    
    # Sapaan personal
    if data['nama']:
        st.markdown(f"### Analisis Peluang {data['nama']} di {data['kampus']} 🎯")
    else:
        st.markdown(f"### Analisis Peluang Masuk {data['kampus']} 🎯")
    
    # Analisis peluang
    peluang_kampus = analisis_peluang_kampus(data['akademik'], data['kampus'])
    klaster = peluang_kampus['klaster']
    
    # Tampilkan info klaster
    st.markdown(f"#### {klaster['warna']} {klaster['nama']}")
    st.caption(klaster['keterangan'])
    
    st.divider()
    
    # Metrik utama
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Skor Akademik Kamu",
            f"{data['akademik']:.0f}",
            delta=f"{peluang_kampus['selisih_min']:+.0f} dari minimum"
        )
    
    with col2:
        st.metric(
            "Rentang Skor Aman",
            f"{klaster['skor_min']} - {klaster['skor_max']}",
            delta=None
        )
    
    with col3:
        st.metric(
            "Estimasi Peluang",
            f"{peluang_kampus['persentase']}%",
            delta=peluang_kampus['kategori']
        )
    
    # Status peluang dengan warna
    st.divider()
    st.markdown("### 📊 Status Peluang & Rekomendasi")
    
    if peluang_kampus['warna_status'] == "success":
        st.success(f"""
        {peluang_kampus['emoji']} **Status: {peluang_kampus['kategori']}**
        
        {peluang_kampus['keterangan']}
        
        Dengan skor akademik **{data['akademik']:.0f}**, kamu memiliki peluang yang baik untuk diterima 
        di jurusan **{data['jurusan']}** di **{data['kampus']}**.
        
        **✅ Rekomendasi Aksi:**
        - ✓ Pertahankan performa akademik dengan konsistensi belajar
        - ✓ Fokus pada penguatan mental dan manajemen stres saat ujian
        - ✓ Lakukan tryout berkala (minimal 2x/bulan) untuk menjaga stabilitas
        - ✓ Pelajari pola soal tahun-tahun sebelumnya
        - ✓ Tetap siapkan pilihan kampus cadangan untuk strategi yang lebih aman
        """)
        
    elif peluang_kampus['warna_status'] == "warning":
        st.warning(f"""
        {peluang_kampus['emoji']} **Status: {peluang_kampus['kategori']}**
        
        {peluang_kampus['keterangan']}
        
        Skor akademik kamu saat ini **{data['akademik']:.0f}**, yang berarti kamu berada di zona kompetitif.
        Peluang masih ada, tetapi kamu perlu meningkatkan skor untuk masuk zona aman.
        
        **⚠️ Target Peningkatan:**
        - 🎯 Butuh tambahan **{klaster['skor_min'] - data['akademik']:.0f} poin** untuk mencapai zona aman minimum
        - 🎯 Butuh tambahan **{klaster['skor_max'] - data['akademik']:.0f} poin** untuk zona sangat aman
        
        **💪 Rekomendasi Aksi:**
        - ✓ Intensifkan latihan soal di subtes dengan skor terendah
        - ✓ Tingkatkan jam belajar efektif menjadi 4-5 jam/hari
        - ✓ Ikuti tryout minimal 2-3x per bulan untuk tracking progres
        - ✓ Fokus pada penguasaan konsep dasar yang sering keluar
        - ✓ Evaluasi dan perbaiki kesalahan dari setiap tryout
        """)
        
    else:
        st.error(f"""
        {peluang_kampus['emoji']} **Status: {peluang_kampus['kategori']}**
        
        {peluang_kampus['keterangan']}
        
        Skor akademik kamu saat ini **{data['akademik']:.0f}**, masih cukup jauh dari zona aman kampus ini.
        
        **🎯 Gap yang Harus Ditutup:**
        - ⚠️ Butuh tambahan **{klaster['skor_min'] - data['akademik']:.0f} poin** untuk mencapai zona aman minimum
        - ⚠️ Butuh tambahan **{klaster['skor_max'] - data['akademik']:.0f} poin** untuk zona sangat aman
        
        **🚨 Rekomendasi Penting:**
        - ✓ Lakukan evaluasi menyeluruh pada SEMUA subtes
        - ✓ Tingkatkan jam belajar menjadi 5-6 jam/hari dengan fokus tinggi
        - ✓ Konsultasi dengan guru/mentor untuk strategi belajar intensif
        - ✓ Ikuti bimbel atau kelas intensif jika memungkinkan
        - ✓ Target peningkatan 50-100 poin dalam 3 bulan ke depan
        """)
    
    # BAGIAN ALTERNATIF KAMPUS - PRIORITAS TINGGI
    st.divider()
    st.markdown("### 🎓 Rekomendasi Kampus: Strategi 3 Pilihan")
    
    st.info("""
    💡 **Strategi Pemilihan Kampus yang Cerdas:**
    
    Berdasarkan skor akademik kamu, berikut adalah rekomendasi kampus dengan strategi **3 pilihan**:
    - **Pilihan 1 (Ambisius):** Target kampus impian, meski sedikit di atas skor kamu
    - **Pilihan 2 (Realistis):** Kampus yang sesuai dengan skor dan peluang tinggi
    - **Pilihan 3 (Aman):** Safety net untuk memastikan kamu tetap lolos PTN
    """)
    
    skor_akademik = data['akademik']
    
    # Kategorisasi kampus berdasarkan skor
    kampus_sangat_aman = []
    kampus_aman = []
    kampus_kompetitif = []
    kampus_berisiko = []
    
    for klaster_id, klaster_data in PTN_DATA.items():
        skor_min = klaster_data["skor_aman"][0]
        skor_max = klaster_data["skor_aman"][1]
        
        for univ in klaster_data["universitas"]:
            status_data = {
                "kampus": univ,
                "klaster": klaster_data["nama"],
                "skor_min": skor_min,
                "skor_max": skor_max,
                "warna": klaster_data["warna"],
                "selisih": skor_akademik - skor_min
            }
            
            if skor_akademik >= skor_max:
                kampus_sangat_aman.append(status_data)
            elif skor_akademik >= skor_min:
                kampus_aman.append(status_data)
            elif skor_akademik >= skor_min - 30:
                kampus_kompetitif.append(status_data)
            else:
                kampus_berisiko.append(status_data)
    
    # Tampilkan rekomendasi berdasarkan kategori
    
    # 1. KAMPUS SANGAT AMAN
    if kampus_sangat_aman:
        st.success("### 🎯 Pilihan Sangat Aman (Peluang 80-90%)")
        st.write("Kampus-kampus ini sangat direkomendasikan karena skor kamu **di atas batas aman**:")
        
        for i, k in enumerate(kampus_sangat_aman[:5], 1):  # Tampilkan max 5
            with st.expander(f"{i}. {k['warna']} {k['kampus']} - **Skor Aman: {k['skor_min']}-{k['skor_max']}**"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Klaster:** {k['klaster']}")
                    st.write(f"**Skor Kamu:** {skor_akademik:.0f}")
                    st.write(f"**Selisih dari Minimum:** +{k['selisih']:.0f} poin")
                    st.success("✅ Peluang sangat besar! Skor kamu sudah melampaui batas aman.")
                with col2:
                    st.metric("Peluang", "85%", delta="Sangat Aman")
                
                st.write("**Rekomendasi:**")
                st.write("- Gunakan sebagai pilihan utama atau pilihan 2 (realistis)")
                st.write("- Fokus pada persiapan mental dan tryout berkala")
                st.write("- Jaga konsistensi hingga hari H")
    
    # 2. KAMPUS AMAN
    if kampus_aman:
        st.success("### ✅ Pilihan Aman (Peluang 60-75%)")
        st.write("Kampus-kampus ini berada **dalam zona aman** untuk skor kamu:")
        
        for i, k in enumerate(kampus_aman[:5], 1):
            with st.expander(f"{i}. {k['warna']} {k['kampus']} - **Skor Aman: {k['skor_min']}-{k['skor_max']}**"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Klaster:** {k['klaster']}")
                    st.write(f"**Skor Kamu:** {skor_akademik:.0f}")
                    st.write(f"**Selisih dari Minimum:** +{k['selisih']:.0f} poin")
                    st.info("✅ Peluang besar! Skor kamu sudah masuk zona aman.")
                with col2:
                    st.metric("Peluang", "70%", delta="Aman")
                
                st.write("**Rekomendasi:**")
                st.write("- Cocok sebagai pilihan 2 (realistis) atau pilihan 1 (ambisius)")
                st.write("- Tingkatkan skor untuk masuk zona sangat aman")
                st.write("- Latihan soal berkala untuk menjaga performa")
    
    # 3. KAMPUS KOMPETITIF
    if kampus_kompetitif:
        st.warning("### ⚠️ Pilihan Kompetitif (Peluang 40-55%)")
        st.write("Kampus-kampus ini masih **bisa dijangkau** dengan peningkatan skor:")
        
        for i, k in enumerate(kampus_kompetitif[:5], 1):
            gap = k['skor_min'] - skor_akademik
            with st.expander(f"{i}. {k['warna']} {k['kampus']} - **Butuh +{gap:.0f} poin**"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Klaster:** {k['klaster']}")
                    st.write(f"**Skor Kamu:** {skor_akademik:.0f}")
                    st.write(f"**Skor Minimum Aman:** {k['skor_min']}")
                    st.write(f"**Gap:** {gap:.0f} poin")
                    st.warning(f"⚠️ Butuh peningkatan {gap:.0f} poin untuk zona aman.")
                with col2:
                    st.metric("Peluang", "50%", delta="Kompetitif")
                
                st.write("**Rekomendasi:**")
                st.write(f"- Bisa dijadikan pilihan 1 (ambisius) jika kamu yakin bisa meningkatkan {gap:.0f} poin")
                st.write("- Intensifkan belajar 3 bulan terakhir sebelum UTBK")
                st.write("- Fokus pada subtes dengan bobot tinggi untuk jurusan kamu")
                st.write("- **Wajib** punya pilihan aman sebagai cadangan")
    
    # 4. KAMPUS BERISIKO (Hanya sebagai informasi)
    if kampus_berisiko and len(kampus_sangat_aman) == 0 and len(kampus_aman) == 0:
        st.error("### 🔴 Perhatian: Semua Kampus Berisiko Tinggi")
        st.write("""
        Berdasarkan skor saat ini, semua kampus masih berada di zona berisiko.
        **Ini bukan akhir!** Dengan strategi yang tepat, kamu masih bisa meningkatkan peluang.
        """)
        
        st.write("**📋 Kampus yang Paling Mungkin Dijangkau (dengan peningkatan skor):**")
        
        # Urutkan dari yang paling dekat
        kampus_berisiko_sorted = sorted(kampus_berisiko, key=lambda x: x['skor_min'])[:5]
        
        for i, k in enumerate(kampus_berisiko_sorted, 1):
            gap = k['skor_min'] - skor_akademik
            with st.expander(f"{i}. {k['warna']} {k['kampus']} - **Target +{gap:.0f} poin**"):
                st.write(f"**Klaster:** {k['klaster']}")
                st.write(f"**Skor Kamu Sekarang:** {skor_akademik:.0f}")
                st.write(f"**Skor Target Minimum:** {k['skor_min']}")
                st.write(f"**Peningkatan Dibutuhkan:** {gap:.0f} poin")
                
                # Estimasi waktu
                if gap <= 50:
                    waktu = "2-3 bulan"
                    tingkat = "Realistis"
                elif gap <= 100:
                    waktu = "3-5 bulan"
                    tingkat = "Menantang tapi Mungkin"
                else:
                    waktu = "5-6 bulan"
                    tingkat = "Sangat Menantang"
                
                st.info(f"**Estimasi Waktu:** {waktu} dengan belajar intensif ({tingkat})")
                
                st.write("**🎯 Roadmap Peningkatan:**")
                st.write(f"- **Target per bulan:** +{gap/3:.0f} poin")
                st.write(f"- **Target per minggu:** +{gap/12:.0f} poin")
                st.write("- Fokus pada subtes dengan bobot tinggi")
                st.write("- Tryout seminggu sekali untuk tracking")
                st.write("- Evaluasi dan perbaiki setiap kesalahan")
    
    # Ringkasan Rekomendasi Akhir
    st.divider()
    st.markdown("### 🎯 Kesimpulan & Rekomendasi Strategi Pemilihan")
    
    if kampus_sangat_aman or kampus_aman:
        # Tentukan label pilihan dengan aman (hindari IndexError)
        semua_aman = kampus_sangat_aman + kampus_aman
        
        pilihan1_label = data['kampus']
        if kampus_kompetitif:
            pilihan1_label += f" atau kampus dari {kampus_kompetitif[0]['klaster']}"
        elif kampus_aman:
            pilihan1_label += f" atau kampus dari {kampus_aman[0]['klaster']}"
        elif kampus_sangat_aman:
            pilihan1_label += f" atau kampus dari {kampus_sangat_aman[0]['klaster']}"
        
        if kampus_aman:
            pilihan2_label = kampus_aman[0]['kampus']
        elif kampus_sangat_aman:
            pilihan2_label = kampus_sangat_aman[0]['kampus']
        else:
            pilihan2_label = "Kampus zona aman terdekat"
        
        if kampus_sangat_aman:
            pilihan3_label = kampus_sangat_aman[0]['kampus']
        elif len(kampus_aman) > 1:
            pilihan3_label = kampus_aman[-1]['kampus']
        elif kampus_aman:
            pilihan3_label = kampus_aman[0]['kampus']
        else:
            pilihan3_label = "Kampus dari klaster lebih rendah"

        st.success(f"""
        **✅ Kabar Baik!** Kamu memiliki **{len(kampus_sangat_aman) + len(kampus_aman)} kampus** 
        dalam zona aman dengan skor saat ini.
        
        **Strategi Pemilihan yang Disarankan:**
        
        📌 **Pilihan 1 (Ambisius):** {pilihan1_label}  
        → Kampus target impian, meski sedikit menantang
        
        📌 **Pilihan 2 (Realistis):** {pilihan2_label}  
        → Peluang tinggi dengan skor saat ini
        
        📌 **Pilihan 3 (Aman):** {pilihan3_label}  
        → Safety net untuk memastikan lolos PTN
        
        **💡 Tips:** Gunakan strategi ini untuk memaksimalkan peluang sambil tetap punya opsi aman!
        """)
    elif kampus_kompetitif:
        st.warning(f"""
        **⚠️ Zona Kompetitif** - Kamu memiliki **{len(kampus_kompetitif)} kampus** yang masih bisa dijangkau.
        
        **Strategi Pemilihan yang Disarankan:**
        
        📌 **Pilihan 1 (Ambisius):** {kampus_kompetitif[0]['kampus']}  
        → Target peningkatan {kampus_kompetitif[0]['skor_min'] - skor_akademik:.0f} poin dalam 2-3 bulan
        
        📌 **Pilihan 2 (Realistis):** {kampus_kompetitif[-1]['kampus'] if len(kampus_kompetitif) > 1 else 'Kampus dari klaster lebih rendah'}  
        → Gap lebih kecil, lebih mudah dicapai
        
        📌 **Pilihan 3 (Aman):** Pilih dari **Klaster 4** (PTN Regional)  
        → Pastikan minimal 1 pilihan di zona aman
        
        **🚨 Penting:** Dengan peningkatan skor yang konsisten, peluang kamu akan naik signifikan!
        """)
    else:
        # Pastikan kampus_berisiko_sorted tersedia
        kampus_berisiko_sorted = sorted(kampus_berisiko, key=lambda x: x['skor_min']) if kampus_berisiko else []
        
        if not kampus_berisiko_sorted:
            st.error("**🔴 Data kampus tidak tersedia.** Silakan coba lagi.")
        else:
            pilihan1 = kampus_berisiko_sorted[0]['kampus']
            pilihan2 = kampus_berisiko_sorted[1]['kampus'] if len(kampus_berisiko_sorted) > 1 else 'Kampus klaster 4'
            pilihan3 = kampus_berisiko_sorted[2]['kampus'] if len(kampus_berisiko_sorted) > 2 else 'Kampus klaster 4'
            gap_min  = kampus_berisiko_sorted[0]['skor_min'] - skor_akademik
            skor_target = kampus_berisiko_sorted[0]['skor_min']

            st.error(f"""
        **🔴 Perhatian Serius Diperlukan** - Skor saat ini masih di bawah zona aman semua kampus.
        
        **Strategi Pemilihan & Peningkatan:**
        
        🎯 **Target Jangka Pendek (1-2 bulan):**
        - Tingkatkan skor minimal +{gap_min:.0f} poin
        - Fokus pada {pilihan1} sebagai target terdekat
        
        🎯 **Target Jangka Menengah (3-4 bulan):**
        - Capai skor {skor_target} untuk masuk zona aman Klaster 4
        - Belajar intensif 5-6 jam/hari
        
        📌 **Rekomendasi Pilihan Sementara:**
        1. **Pilihan 1:** {pilihan1} (target terdekat)
        2. **Pilihan 2:** {pilihan2}
        3. **Pilihan 3:** {pilihan3}
        
        **💪 Motivasi:** Gap masih bisa ditutup! Fokus, konsisten, dan evaluasi rutin adalah kuncinya.
        """)
    
    # Tabel perbandingan semua klaster
    st.divider()
    st.markdown("### 📊 Tabel Perbandingan Lengkap Semua Klaster")
    
    st.write("Gunakan tabel ini untuk memahami posisi skor kamu terhadap semua klaster PTN:")
    
    comparison_data = []
    for klaster_id, klaster_data in PTN_DATA.items():
        skor_min = klaster_data["skor_aman"][0]
        skor_max = klaster_data["skor_aman"][1]
        selisih = data['akademik'] - skor_min
        
        if data['akademik'] >= skor_max:
            status = "🎯 Sangat Aman"
            peluang = "85%"
        elif data['akademik'] >= skor_min:
            status = "✅ Aman"
            peluang = "70%"
        elif data['akademik'] >= skor_min - 30:
            status = "⚠️ Kompetitif"
            peluang = "50%"
        else:
            status = "🔴 Berisiko"
            peluang = "30%"
        
        comparison_data.append({
            "Klaster": f"{klaster_data['warna']} {klaster_data['nama']}",
            "Rentang Skor": f"{skor_min} - {skor_max}",
            "Skor Kamu": f"{data['akademik']:.0f}",
            "Selisih": f"{selisih:+.0f}",
            "Status": status,
            "Peluang": peluang
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Footer tips
    st.divider()
    st.info("""
    💡 **Tips Menggunakan Analisis Ini:**
    
    1. **Jangan hanya fokus pada 1 kampus** - Gunakan strategi 3 pilihan untuk memaksimalkan peluang
    2. **Evaluasi rutin** - Lakukan tryout berkala dan update analisis berdasarkan skor terbaru
    3. **Fleksibel tapi strategis** - Sesuaikan pilihan berdasarkan perkembangan skor kamu
    4. **Jangan takut gagal** - Pilihan aman tetap penting, tapi jangan takut untuk bermimpi tinggi!
    5. **Konsisten adalah kunci** - Peningkatan skor membutuhkan waktu dan usaha konsisten
    
    **Ingat:** Analisis ini berdasarkan data historis. Hasil akhir tetap bergantung pada performa kamu saat UTBK!
    """)


def render_tab_analisis(data: Dict):
    """Render tab analisis mendalam"""
    
    # Sapaan personal di awal analisis
    if data['nama']:
        st.markdown(f"### Hai {data['nama']}, mari kita telaah hasil analisis kamu secara mendalam! 🔍")
    else:
        st.subheader("Analisis Akademik & Psikologis Mendalam")
    
    # Klasifikasi Profil
    tipe = klasifikasi_profil(
        data['fokus'], 
        data['percaya_diri'], 
        data['kecemasan'], 
        data['distraksi']
    )
    
    st.markdown("### 📌 Interpretasi Profil Belajar")
    st.write(f"""
    Berdasarkan hasil pemodelan akademik dan psikologis, sistem mengklasifikasikan 
    profil belajar kamu sebagai **{tipe}**.
    
    Skor akademik sebesar **{data['akademik']:.0f}** menunjukkan bahwa secara kognitif, 
    kamu sudah memiliki kemampuan yang cukup untuk memahami pola soal UTBK, khususnya 
    pada bidang yang relevan dengan jurusan **{data['jurusan']}**.
    
    Namun, kesiapan menghadapi UTBK tidak hanya ditentukan oleh kecerdasan akademik, 
    tetapi juga oleh kestabilan mental, daya tahan belajar, serta kemampuan mengelola 
    tekanan selama proses ujian.
    """)
    
    # Analisis Kemampuan Akademik
    st.markdown("### 🧩 Analisis Kemampuan Akademik")
    
    level_pm = "kuat" if data['PM'] >= 600 else "cukup" if data['PM'] >= 450 else "perlu ditingkatkan"
    level_literasi = "baik" if data['LBI'] >= 550 and data['LBE'] >= 550 else "cukup" if data['LBI'] >= 450 else "perlu penguatan"
    level_pu = "stabil" if data['PU'] >= 550 else "fluktuatif"
    
    st.write(f"""
    Dari aspek akademik, performa kamu menunjukkan bahwa:
    
    - Kemampuan penalaran dan pemecahan masalah berada pada level **{level_pm}**
    - Kemampuan literasi bahasa menunjukkan tingkat **{level_literasi}**
    - Pemahaman umum dan logika dasar berada pada level **{level_pu}**
    
    Pola ini menunjukkan bahwa kamu sudah memiliki fondasi dasar yang memadai, namun 
    masih terdapat beberapa aspek yang perlu difokuskan agar performa lebih konsisten 
    di semua subtes.
    """)
    
    # Analisis Psikologis
    st.markdown("### 🧠 Analisis Psikologis & Mental Belajar")
    
    level_fokus = "sangat baik" if data['fokus'] >= 4 else "cukup" if data['fokus'] >= 3 else "rendah"
    level_pd = "kesiapan mental yang kuat" if data['percaya_diri'] >= 4 else "masih perlu penguatan"
    potensi_cemas = "mengganggu performa" if data['kecemasan'] >= 4 else "masih terkendali"
    
    st.write(f"""
    Dari sisi psikologis, hasil pengukuran menunjukkan bahwa:
    
    - Tingkat fokus belajar berada pada level **{data['fokus']}/5**, yang berarti **{level_fokus}**
    - Kepercayaan diri berada pada level **{data['percaya_diri']}/5**, yang menunjukkan **{level_pd}**
    - Tingkat kecemasan berada pada level **{data['kecemasan']}/5**, yang berpotensi **{potensi_cemas}**
    - Distraksi berada pada level **{data['distraksi']}/5**, yang menunjukkan tingkat gangguan eksternal dan internal saat belajar
    """)
    
    # Analisis Risiko
    st.markdown("### ⚠️ Analisis Risiko Performa Saat Ujian")
    
    nilai_risiko, level_risiko, ket_risiko = hitung_risiko(
        data['fokus'],
        data['percaya_diri'],
        data['kecemasan'],
        data['distraksi']
    )
    
    st.write(f"""
    Berdasarkan kombinasi faktor mental dan akademik, tingkat risiko kamu berada pada 
    kategori **{level_risiko}**. 
    
    Artinya, kondisi saat ini **{ket_risiko}** apabila tidak dikelola dengan strategi 
    belajar yang tepat. Risiko ini terutama dipengaruhi oleh tingkat kecemasan, konsistensi 
    fokus, dan kemampuan menjaga kepercayaan diri dalam situasi tekanan tinggi seperti UTBK.
    """)
    
    # Kesimpulan
    st.markdown("### 📈 Kesimpulan Analisis Menyeluruh")
    st.write(f"""
    Secara keseluruhan, profil belajar kamu menunjukkan bahwa:
    
    - Kamu memiliki potensi akademik yang cukup kompetitif
    - Fondasi pemahaman materi sudah terbentuk
    - Faktor mental masih menjadi variabel penting yang perlu diperkuat
    - Dengan pola latihan yang tepat, peluang peningkatan skor masih sangat besar
    
    Dengan pendekatan belajar yang sistematis dan disiplin, kamu memiliki peluang 
    realistis untuk bersaing di jurusan **{data['jurusan']}**.
    """)
    
    # Analisis Kebiasaan Belajar
    st.markdown("### 📚 Analisis Kebiasaan & Pola Belajar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Jam Belajar/Hari", f"Level {data['jam_belajar']}/5")
        st.metric("Hari Belajar/Minggu", f"Level {data['hari_belajar']}/5")
        st.metric("Latihan Soal/Minggu", f"Level {data['latihan_soal']}/5")
    
    with col2:
        st.metric("Tryout/Bulan", f"Level {data['frekuensi_tryout']}/5")
        st.metric("Review Soal/Minggu", f"Level {data['review_soal']}/5")
        st.metric("Skor Kebiasaan Total", f"{data['kebiasaan']:.0f}/100", 
                 delta=f"{data['kebiasaan_kategori']}")
    
    # Evaluasi kebiasaan belajar
    if data['kebiasaan'] >= 75:
        st.success(f"""
        {data['kebiasaan_emoji']} **{data['kebiasaan_keterangan']}**
        
        Pola belajar kamu menunjukkan disiplin dan konsistensi yang sangat baik. 
        Pertahankan momentum ini dan fokus pada peningkatan kualitas pemahaman materi.
        """)
    elif data['kebiasaan'] >= 60:
        st.info(f"""
        {data['kebiasaan_emoji']} **{data['kebiasaan_keterangan']}**
        
        Kamu sudah memiliki fondasi kebiasaan belajar yang baik. Untuk hasil maksimal, 
        pertimbangkan untuk meningkatkan intensitas latihan soal dan frekuensi tryout.
        """)
    elif data['kebiasaan'] >= 45:
        st.warning(f"""
        {data['kebiasaan_emoji']} **{data['kebiasaan_keterangan']}**
        
        Kebiasaan belajar kamu masih inkonsisten. Untuk bersaing di UTBK, diperlukan 
        peningkatan signifikan dalam jam belajar, latihan soal, dan review rutin.
        """)
    else:
        st.error(f"""
        {data['kebiasaan_emoji']} **{data['kebiasaan_keterangan']}**
        
        Pola belajar saat ini belum optimal untuk persiapan UTBK. Sangat disarankan untuk:
        - Meningkatkan jam belajar menjadi minimal 3-4 jam/hari
        - Belajar minimal 4-5 hari/minggu
        - Latihan soal minimal 3x/minggu
        - Tryout minimal 2x/bulan
        """)
    
    # Rekomendasi perbaikan kebiasaan
    st.markdown("#### 💡 Rekomendasi Perbaikan Kebiasaan Belajar")
    
    rekomendasi = []
    
    if data['jam_belajar'] < 3:
        rekomendasi.append("• **Tingkatkan jam belajar** menjadi minimal 3-4 jam/hari untuk hasil optimal")
    
    if data['hari_belajar'] < 4:
        rekomendasi.append("• **Tingkatkan konsistensi** belajar menjadi minimal 4-5 hari/minggu")
    
    if data['latihan_soal'] < 3:
        rekomendasi.append("• **Perbanyak latihan soal** menjadi minimal 3-4x/minggu untuk familiaritas dengan tipe soal")
    
    if data['frekuensi_tryout'] < 2:
        rekomendasi.append("• **Ikuti tryout lebih rutin** minimal 2x/bulan untuk simulasi kondisi ujian")
    
    if data['review_soal'] < 3:
        rekomendasi.append("• **Tingkatkan frekuensi review** menjadi minimal 3x/minggu untuk memperbaiki kesalahan")
    
    if rekomendasi:
        st.write("Berdasarkan analisis kebiasaan belajar, berikut adalah area yang perlu diperbaiki:\n")
        for rec in rekomendasi:
            st.write(rec)
    else:
        st.success("✅ Kebiasaan belajar kamu sudah sangat baik di semua aspek! Pertahankan!")


def render_tab_strategi(data: Dict):
    """Render tab strategi belajar"""
    
    # Sapaan personal
    if data['nama']:
        st.markdown(f"### {data['nama']}, berikut strategi belajar yang dirancang khusus untukmu! 🚀")
    else:
        st.subheader("Strategi Belajar Personal Terstruktur")
    
    st.write("""
    Strategi berikut dirancang secara personal berdasarkan profil akademik, kondisi 
    psikologis, serta target jurusan kamu. Pendekatan ini bertujuan untuk meningkatkan 
    performa secara bertahap, stabil, dan berkelanjutan.
    """)
    
    # Strategi Harian
    st.markdown("### 📅 Strategi Harian")
    st.write("""
    1. Lakukan sesi belajar 2–3 kali sehari dengan durasi 45–60 menit
    2. Setiap sesi fokus pada satu subtes utama
    3. Gunakan metode *active recall* dan latihan soal
    4. Hindari belajar pasif hanya dengan membaca materi
    5. Akhiri sesi dengan rangkuman pribadi
    """)
    
    # Strategi Penguatan Fokus
    st.markdown("### 🧠 Strategi Penguatan Fokus")
    
    if data['fokus'] <= 3:
        st.write("""
        Karena tingkat fokus kamu masih perlu ditingkatkan, disarankan untuk:
        
        - Menggunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)
        - Menyimpan ponsel di luar jangkauan saat belajar
        - Menentukan target kecil setiap sesi
        - Belajar di tempat yang minim distraksi
        - Gunakan aplikasi pemblokir website untuk menghindari gangguan
        """)
    else:
        st.write("""
        Tingkat fokus kamu sudah baik. Pertahankan dengan:
        
        - Menjaga konsistensi jadwal belajar
        - Menghindari multitasking
        - Tetap gunakan teknik Pomodoro untuk memaksimalkan produktivitas
        """)
    
    # Strategi Manajemen Stres
    st.markdown("### 😌 Strategi Manajemen Stres & Kecemasan")
    
    if data['kecemasan'] >= 3:
        st.write("""
        Karena tingkat kecemasan cukup tinggi, kamu disarankan untuk:
        
        - Melakukan tryout rutin minimal 2x per bulan
        - Membiasakan diri dengan batas waktu pengerjaan
        - Latihan pernapasan sebelum belajar (teknik 4-7-8)
        - Menghindari membandingkan diri dengan orang lain
        - Fokus pada progres pribadi
        - Journaling untuk mengidentifikasi sumber kecemasan
        """)
    else:
        st.write("""
        Tingkat kecemasan kamu relatif terkendali. Tetap pertahankan dengan:
        
        - Menjaga keseimbangan belajar dan istirahat
        - Tetap lakukan tryout berkala untuk menjaga familiaritas dengan format ujian
        """)
    
    # Strategi Akademik
    st.markdown("### 📊 Strategi Akademik Berbasis Data")
    
    # Identifikasi subtes terlemah
    skor_subtes = {
        "PU": data['PU'], "PPU": data['PPU'], "PBM": data['PBM'],
        "PK": data['PK'], "LBI": data['LBI'], "LBE": data['LBE'], "PM": data['PM']
    }
    terlemah = min(skor_subtes, key=skor_subtes.get)
    
    st.write(f"""
    Berdasarkan skor akademik kamu, fokus utama sebaiknya pada:
    
    - **{terlemah}** sebagai prioritas utama (skor terendah: {skor_subtes[terlemah]})
    - Subtes utama jurusan **{data['jurusan']}** sebagai target penguatan
    - Latihan soal minimal 300–500 soal per bulan
    - Evaluasi kesalahan secara tertulis dengan mencatat pola kesalahan
    - Buat bank soal untuk topik yang sering salah
    """)
    
    # Strategi Jangka Menengah
    st.markdown("### 🗓️ Strategi Jangka Menengah (3–6 Bulan)")
    st.write("""
    Dalam periode 3–6 bulan ke depan, lakukan:
    
    **✅ Bulan 1–2: Fondasi**
    - Penguatan konsep dasar
    - Perbaikan kelemahan utama
    - Identifikasi gap pengetahuan
    
    **✅ Bulan 3–4: Intensifikasi**
    - Intensifikasi latihan soal (target 50-100 soal/minggu)
    - Simulasi waktu ujian
    - Mulai tryout bulanan
    
    **✅ Bulan 5–6: Pemantapan**
    - Tryout mingguan
    - Review kesalahan berulang
    - Manajemen stamina mental dan fisik
    """)
    
    # Strategi Menjelang UTBK
    st.markdown("### 🎯 Strategi Menjelang UTBK (1 Bulan Terakhir)")
    st.write("""
    Pada fase akhir persiapan:
    
    - ❌ Kurangi belajar materi baru
    - ✅ Fokus pada review dan penguatan
    - ✅ Jaga pola tidur (minimal 7-8 jam/hari)
    - ✅ Jaga nutrisi dan hidrasi
    - ✅ Perbanyak tryout (minimal 2x per minggu)
    - ✅ Simulasi kondisi ujian sebenarnya
    
    **Tujuan utama:** Menjaga performa puncak dan stabilitas mental.
    """)
    
    # Rekomendasi Akhir
    st.markdown("### 📌 Rekomendasi Akhir")
    st.success(f"""
    Jika strategi ini dijalankan secara disiplin, kamu berpotensi meningkatkan skor 
    secara signifikan dalam 3–6 bulan ke depan. 
    
    **Kunci utama keberhasilan:**
    - Konsistensi dalam eksekusi
    - Evaluasi rutin (mingguan)
    - Pengelolaan mental yang baik
    - Fokus pada progres, bukan perfeksi
    
    Dengan pendekatan ini, peluang kamu di jurusan **{data['jurusan']}** akan semakin kompetitif.
    """)


def render_tab_jurusan(data: Dict):
    """Render tab rekomendasi jurusan"""
    
    # Sapaan personal
    if data['nama']:
        st.markdown(f"### Rekomendasi Jurusan untuk {data['nama']} 🎓")
    else:
        st.subheader("Rekomendasi Jurusan Alternatif")
    
    akademik = data['akademik']
    nama_panggil = data['nama'] if data['nama'] else "kamu"
    
    if akademik > 750:
        st.success(f"""
        ✅ **Peluang Sangat Kuat**
        
        Peluang {nama_panggil} di jurusan **{data['jurusan']}** masih sangat kuat dengan skor akademik {akademik:.0f}.
        
        **Alternatif jurusan yang bisa dipertimbangkan:**
        - Teknik Informatika
        - Kedokteran Gigi
        - Statistika
        - Farmasi
        - Manajemen
        
        Dengan skor ini, {nama_panggil} memiliki fleksibilitas untuk memilih berbagai jurusan kompetitif.
        """)
        
    elif akademik > 650:
        st.warning(f"""
        ⚠️ **Peluang Menengah-Atas**
        
        Peluang {nama_panggil} berada di level menengah-atas dengan skor akademik {akademik:.0f}.
        
        **Alternatif jurusan yang direkomendasikan:**
        - Teknik Industri
        - Ekonomi
        - Akuntansi
        - Psikologi
        - Administrasi Publik
        - Ilmu Komunikasi
        
        Dengan peningkatan skor 50-100 poin, peluang {nama_panggil} di jurusan pilihan utama akan meningkat signifikan.
        """)
        
    else:
        st.error(f"""
        🔴 **Persaingan Ketat**
        
        Persaingan di jurusan **{data['jurusan']}** cukup berat dengan skor akademik {akademik:.0f}.
        
        **Alternatif jurusan yang lebih aman:**
        - Sosiologi
        - Geografi
        - Sejarah
        - Pendidikan Bahasa
        - Bisnis
        - Kesehatan Masyarakat
        
        **Rekomendasi:**
        - Fokus pada peningkatan skor akademik 100-150 poin
        - Pertimbangkan jurusan dengan persaingan lebih moderat
        - Tetap siapkan pilihan cadangan yang strategis
        """)
    
    st.info("""
    **💡 Tips Memilih Jurusan:**
    
    1. **Minat & Passion:** Pilih jurusan yang sesuai dengan minat jangka panjang
    2. **Kemampuan:** Sesuaikan dengan kekuatan akademik kamu
    3. **Prospek Karir:** Pertimbangkan peluang kerja di masa depan
    4. **Peluang Kelulusan:** Realistis dengan skor yang dimiliki
    5. **Lokasi & Universitas:** Pertimbangkan preferensi lokasi dan akreditasi
    
    Memilih jurusan sebaiknya mempertimbangkan keseimbangan antara passion, kemampuan, 
    dan peluang kelulusan agar hasil UTBK dapat dimaksimalkan.
    """)


# ====================================== 
# MAIN APPLICATION
# ====================================== 

def main():
    """Fungsi utama aplikasi"""
    # Setup
    setup_page()
    
    # Load model LGBM
    lgbm_model, lgbm_tersedia = load_lgbm_model()
    
    # Initialize session state untuk menyimpan status prediksi
    if 'prediksi_clicked' not in st.session_state:
        st.session_state.prediksi_clicked = False
    
    # Kumpulkan input dari sidebar
    input_data = render_sidebar()
    
    # Update session state jika tombol diklik
    if input_data['cek_prediksi']:
        st.session_state.prediksi_clicked = True
    
    # Render header dengan kontrol greeting
    render_header(input_data['nama'], st.session_state.prediksi_clicked)
    
    # Tampilkan hasil hanya jika tombol sudah diklik
    if st.session_state.prediksi_clicked:
        # Hitung semua metrik
        skor_akademik = hitung_skor_akademik(
            input_data['jurusan'],
            input_data['PU'], input_data['PPU'], input_data['PBM'],
            input_data['PK'], input_data['LBI'], input_data['LBE'], input_data['PM']
        )
        
        # ===== PREDIKSI LGBM =====
        lgbm_hasil = None
        if lgbm_tersedia and lgbm_model is not None:
            lgbm_hasil = prediksi_lgbm(lgbm_model, input_data)

        # Peluang lolos tetap dihitung dari formula manual (skor TPS vs passing grade)
        peluang_lolos, peluang_kategori, peluang_ket = hitung_peluang_lolos(
            skor_akademik,
            input_data['kampus']
        )
        
        stabilitas_mental, stabilitas_kategori, stabilitas_ket = hitung_stabilitas_mental(
            input_data['fokus'],
            input_data['percaya_diri'],
            input_data['kecemasan'],
            input_data['distraksi']
        )
        
        konsistensi_belajar, konsistensi_kategori, konsistensi_ket = hitung_indeks_konsistensi(
            input_data['jam_belajar'],
            input_data['hari_belajar'],
            input_data['latihan_soal'],
            input_data['frekuensi_tryout'],
            input_data['review_soal']
        )
        
        risiko_level, risiko_emoji, risiko_ket = hitung_risiko_underperform(
            stabilitas_mental,
            konsistensi_belajar
        )
        
        # Backward compatibility: hitung skor kebiasaan untuk tab analisis
        skor_kebiasaan, kategori_kebiasaan, ket_kebiasaan, emoji_kebiasaan = hitung_skor_kebiasaan_belajar(
            input_data['jam_belajar'],
            input_data['hari_belajar'],
            input_data['latihan_soal'],
            input_data['frekuensi_tryout'],
            input_data['review_soal']
        )
        
        # Gabungkan semua data
        hasil_data = {
            **input_data,
            'akademik': skor_akademik,
            'peluang': peluang_lolos,
            'peluang_kategori': peluang_kategori,
            'peluang_keterangan': peluang_ket,
            'stabilitas': stabilitas_mental,
            'stabilitas_kategori': stabilitas_kategori,
            'stabilitas_keterangan': stabilitas_ket,
            'konsistensi': konsistensi_belajar,
            'konsistensi_kategori': konsistensi_kategori,
            'konsistensi_keterangan': konsistensi_ket,
            'risiko_level': risiko_level,
            'risiko_emoji': risiko_emoji,
            'risiko_keterangan': risiko_ket,
            # Backward compatibility untuk tab yang masih menggunakan
            'kebiasaan': skor_kebiasaan,
            'kebiasaan_kategori': kategori_kebiasaan,
            'kebiasaan_keterangan': ket_kebiasaan,
            'kebiasaan_emoji': emoji_kebiasaan,
            # LGBM info
            'lgbm_tersedia': lgbm_tersedia,
            'lgbm_hasil'   : lgbm_hasil,
        }
        
        # Render dashboard
        render_dashboard(hasil_data)
        
        # Render tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Peluang Kampus",
            "🧠 Analisis",
            "🚀 Strategi",
            "🎓 Jurusan"
        ])
        
        with tab1:
            render_tab_peluang_kampus(hasil_data)
        
        with tab2:
            render_tab_analisis(hasil_data)
        
        with tab3:
            render_tab_strategi(hasil_data)
        
        with tab4:
            render_tab_jurusan(hasil_data)
        
        # Footer
        st.divider()
        
        # Pesan penutup personal
        if input_data['nama']:
            st.success(f"""
            💪 **Pesan untuk {input_data['nama']}:**
            
            Perjalanan menuju UTBK adalah maraton, bukan sprint. Setiap langkah kecil yang kamu ambil hari ini 
            akan membawa dampak besar untuk masa depan. Tetap konsisten, percaya pada proses, dan jangan pernah 
            menyerah pada impian kamu!
            
            Ingat: Kesuksesan bukan hanya tentang nilai, tapi tentang bagaimana kamu berkembang menjadi 
            pribadi yang lebih baik dalam prosesnya. Saya akan selalu di sini untuk mendampingi perjalanan kamu. 
            
            **Semangat, {input_data['nama']}! Kamu pasti bisa! 🚀✨**
            """)
        
        st.caption("🤖 AI Education Intelligence System • Enhanced Version")
        st.caption("Dikembangkan dengan pendekatan holistik untuk persiapan UTBK yang optimal")
    else:
        # Tampilkan instruksi jika belum klik prediksi
        st.info("""
        📌 **Langkah Selanjutnya:**
        
        Silakan lengkapi semua informasi di sidebar, lalu klik tombol **"CEK PREDIKSI SEKARANG"** 
        untuk melihat hasil analisis lengkap kesiapan UTBK kamu.
        """)
        
        # Tampilkan preview fitur
        st.markdown("### ✨ Yang Akan Kamu Dapatkan:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 📊 Dashboard Komprehensif
            - Skor kesiapan keseluruhan
            - Estimasi peluang kelulusan
            - Analisis akademik mendalam
            """)
        
        with col2:
            st.markdown("""
            #### 🧠 Analisis Mendalam
            - Profil belajar personal
            - Evaluasi psikologis
            - Identifikasi risiko
            """)
        
        with col3:
            st.markdown("""
            #### 🎯 Rekomendasi Praktis
            - Strategi belajar terstruktur
            - Timeline persiapan
            - Alternatif jurusan
            """)
        
        st.divider()
        st.caption("🤖 AI Education Intelligence System • Enhanced Version")


# ====================================== 
# ENTRY POINT
# ====================================== 

if __name__ == "__main__":
    main()
