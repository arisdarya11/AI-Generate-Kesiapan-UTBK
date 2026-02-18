import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Tuple

# ====================================== 
# KONFIGURASI HALAMAN & STYLE
# ====================================== 
st.set_page_config(page_title="AI UTBK Readiness Dashboard Pro", layout="wide")

# Custom CSS untuk UI yang lebih modern dan clean
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    div[data-testid="stExpander"] { border: none; box-shadow: 0 2px 4px rgba(0,0,0,0.05); background: white; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; transition: 0.3s; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
</style>
""", unsafe_allow_html=True)

# ====================================== 
# SESSION STATE & NAVIGASI
# ====================================== 
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def move_to_step(next_step):
    st.session_state.step = next_step

# ====================================== 
# DATA KONSTRUKTOR
# ====================================== 
BOBOT_JURUSAN = {
    "Kedokteran": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.15, "LBI": 0.10, "LBE": 0.10, "PM": 0.20, "Aman": 760},
    "Teknik Informatika": {"PU": 0.20, "PPU": 0.10, "PBM": 0.05, "PK": 0.25, "LBI": 0.05, "LBE": 0.10, "PM": 0.25, "Aman": 740},
    "Ilmu Hukum": {"PU": 0.20, "PPU": 0.20, "PBM": 0.20, "PK": 0.05, "LBI": 0.20, "LBE": 0.10, "PM": 0.05, "Aman": 710},
    "Manajemen": {"PU": 0.15, "PPU": 0.15, "PBM": 0.15, "PK": 0.15, "LBI": 0.15, "LBE": 0.15, "PM": 0.10, "Aman": 690},
    "Psikologi": {"PU": 0.20, "PPU": 0.15, "PBM": 0.20, "PK": 0.10, "LBI": 0.15, "LBE": 0.10, "PM": 0.10, "Aman": 700}
}

DAFTAR_PTN = [
    "Universitas Indonesia (UI)", "Universitas Gadjah Mada (UGM)", "Institut Teknologi Bandung (ITB)", 
    "Universitas Airlangga (Unair)", "Universitas Brawijaya (UB)", "Universitas Padjadjaran (Unpad)"
]

# ====================================== 
# FUNGSI VISUALISASI
# ====================================== 
def draw_radar_chart(skor):
    categories = ['PU', 'PPU', 'PBM', 'PK', 'LBI', 'LBE', 'PM']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[skor[c] for c in categories],
        theta=categories,
        fill='toself',
        name='Skor Kamu',
        line_color='#1f77b4'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1000])),
        showlegend=False, title="Radar Kompetensi TPS"
    )
    return fig

def draw_comparison_pipe(skor, bobot):
    categories = ['PU', 'PPU', 'PBM', 'PK', 'LBI', 'LBE', 'PM']
    skor_vals = [skor[c] for c in categories]
    bobot_vals = [bobot[c] * 1000 for c in categories] # Skala 1000 untuk visualisasi proporsi
    
    fig = go.Figure(data=[
        go.Bar(name='Skor Kamu', x=categories, y=skor_vals, marker_color='#00d2ff'),
        go.Bar(name='Proporsi Ideal Jurusan', x=categories, y=bobot_vals, marker_color='#ff9a9e')
    ])
    fig.update_layout(barmode='group', title="Perbandingan Skor vs Kebutuhan Jurusan", height=400)
    return fig

# ====================================== 
# MULTI-STEP UI
# ====================================== 

# --- STEP 1: PROFIL & TARGET ---
if st.session_state.step == 1:
    st.title("🎯 Langkah 1: Profil & Target")
    with st.form("profil_form"):
        nama = st.text_input("Nama Lengkap", placeholder="Budi Santoso")
        ptn = st.selectbox("Kampus Impian", DAFTAR_PTN)
        jurusan = st.selectbox("Target Jurusan", list(BOBOT_JURUSAN.keys()))
        submitted = st.form_submit_button("Lanjut ke Input Skor ➡️")
        if submitted:
            st.session_state.user_data.update({"nama": nama, "ptn": ptn, "jurusan": jurusan})
            move_to_step(2)
            st.rerun()

# --- STEP 2: INPUT SKOR TPS ---
elif st.session_state.step == 2:
    st.title("📊 Langkah 2: Hasil Tryout (Skala 1000)")
    st.info("Masukkan nilai tryout terakhir kamu untuk setiap subtes.")
    with st.form("skor_form"):
        col1, col2 = st.columns(2)
        with col1:
            pu = st.slider("Penalaran Umum (PU)", 0, 1000, 500)
            ppu = st.slider("Pengetahuan Umum (PPU)", 0, 1000, 500)
            pbm = st.slider("Pemahaman Bacaan (PBM)", 0, 1000, 500)
            pk = st.slider("Pengetahuan Kuantitatif (PK)", 0, 1000, 500)
        with col2:
            lbi = st.slider("Literasi B. Indonesia", 0, 1000, 500)
            lbe = st.slider("Literasi B. Inggris", 0, 1000, 500)
            pm = st.slider("Penalaran Matematika", 0, 1000, 500)
        
        submitted = st.form_submit_button("Lanjut ke Evaluasi Psikologi ➡️")
        if submitted:
            st.session_state.user_data['skor'] = {"PU": pu, "PPU": ppu, "PBM": pbm, "PK": pk, "LBI": lbi, "LBE": lbe, "PM": pm}
            move_to_step(3)
            st.rerun()

# --- STEP 3: SURVEY PSIKOLOGI ---
elif st.session_state.step == 3:
    st.title("🧠 Langkah 3: Kondisi Psikologis")
    with st.form("psiko_form"):
        fokus = st.select_slider("Tingkat Fokus Belajar", options=[1, 2, 3, 4, 5])
        percaya_diri = st.select_slider("Tingkat Kepercayaan Diri", options=[1, 2, 3, 4, 5])
        kecemasan = st.select_slider("Tingkat Kecemasan Ujian", options=[1, 2, 3, 4, 5])
        
        submitted = st.form_submit_button("Lihat Dashboard Analisis 🚀")
        if submitted:
            st.session_state.user_data['psikologi'] = {"fokus": fokus, "percaya_diri": percaya_diri, "kecemasan": kecemasan}
            move_to_step(4)
            st.rerun()

# --- STEP 4: DASHBOARD UTAMA ---
elif st.session_state.step == 4:
    data = st.session_state.user_data
    skor = data['skor']
    bobot_info = BOBOT_JURUSAN[data['jurusan']]
    
    # Perhitungan Skor Akhir Tertimbang
    skor_akhir = sum(skor[k] * bobot_info[k] for k in skor)
    skor_aman = bobot_info['Aman']
    peluang = (skor_akhir / skor_aman) * 100

    st.title(f"📈 Dashboard Kesiapan: {data['nama']}")
    st.subheader(f"Target: {data['jurusan']} - {data['ptn']}")

    # --- ROW 1: METRICS ---
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Skor Tertimbang Kamu", f"{skor_akhir:.1f}", f"{skor_akhir - skor_aman:.1f} dari Target")
    col_m2.metric("Ambang Batas Aman", f"{skor_aman}")
    
    status_warna = "normal" if peluang < 100 else "inverse"
    col_m3.metric("Peluang Kelolosan", f"{min(peluang, 100):.1f}%")

    # --- ROW 2: ANALISIS GRAFIK ---
    st.divider()
    col_v1, col_v2 = st.columns([1, 1.5])
    
    with col_v1:
        st.plotly_chart(draw_radar_chart(skor), use_container_width=True)
        
    
    with col_v2:
        st.plotly_chart(draw_comparison_pipe(skor, bobot_info), use_container_width=True)
        

    # --- ROW 3: TABEL BOBOT & ALTERNATIF ---
    st.divider()
    t1, t2 = st.columns(2)
    
    with t1:
        st.subheader("📋 Detail Bobot & Kontribusi")
        df_bobot = pd.DataFrame({
            "Subtes": list(skor.keys()),
            "Skor Kamu": list(skor.values()),
            "Bobot Jurusan": [f"{bobot_info[k]*100}%" for k in skor.keys()],
            "Poin Kontribusi": [skor[k] * bobot_info[k] for k in skor.keys()]
        })
        st.table(df_bobot)

    with t2:
        st.subheader("🏁 Kesimpulan & Alternatif")
        if skor_akhir >= skor_aman:
            st.success(f"Selamat! Peluang kamu di {data['jurusan']} sangat tinggi. Pertahankan konsistensi!")
        else:
            st.warning(f"Skor kamu saat ini masih di bawah rata-rata aman. Fokus tingkatkan subtes dengan bobot terbesar!")
        
        st.markdown("---")
        st.write("**Jurusan Alternatif (Formalitas):**")
        st.info(f"1. Pendidikan {data['jurusan']} - {data['ptn']}")
        st.info(f"2. {data['jurusan']} (Program Paralel/Mandiri)")

    # --- PDF EXPORT (Simulation) ---
    st.divider()
    if st.button("📥 Save Result as PDF"):
        st.write("Silakan tekan `Ctrl + P` atau `Cmd + P` pada keyboard Anda untuk menyimpan halaman ini sebagai PDF.")

    if st.button("🔄 Mulai Analisis Ulang"):
        st.session_state.step = 1
        st.rerun()
