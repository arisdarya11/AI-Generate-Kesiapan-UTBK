"""
SKORIA — AI UTBK Readiness Dashboard v4.0
Platform kecerdasan buatan untuk analisis kesiapan UTBK secara holistik
Skor maksimal: 1000 | Jenjang S1 & D3 | Multi-halaman | Charts | PDF Export
Data skor aman berbasis SNPMB/BPPP Kemdikbud & referensi media pendidikan 2025/2026
per jurusan, jenjang (S1/D3), dan PTN
"""

import streamlit as st
import numpy as np
import pandas as pd
import pickle, os, base64, datetime, json
from typing import Dict, Tuple, List
import plotly.graph_objects as go
import plotly.express as px

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SKORIA — AI UTBK",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════
# GLOBAL CSS — Light clean theme, comfortable on eyes
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');

:root {
  --bg:       #f0f4f8;
  --surf:     #ffffff;
  --surf2:    #f7f9fc;
  --border:   #dde3ec;
  --accent:   #3b6cb7;
  --accent2:  #4a7fd4;
  --gold:     #c8890a;
  --gold2:    #e0a020;
  --green:    #1a8a4a;
  --green2:   #22a55e;
  --red:      #c0392b;
  --orange:   #d4620a;
  --purple:   #7048c8;
  --teal:     #0d8a80;
  --text:     #1a2540;
  --text2:    #3a4a65;
  --text3:    #6a7a95;
  --r:        10px;
  --shadow:   0 2px 8px rgba(30,50,100,.09);
}

html,body,[class*="css"],.stApp {
  background: var(--bg) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden }
.stDeployButton { display: none }
.block-container { padding: 1rem 1.5rem !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
  background: #ffffff;
  border-bottom: 2px solid var(--border);
  padding: .65rem 2rem;
  display: flex; align-items: center; gap: 1.2rem;
  margin: -1rem -1.5rem 1.5rem -1.5rem;
  position: sticky; top: 0; z-index: 999;
  box-shadow: 0 2px 8px rgba(30,50,100,.08);
}
.topbar-brand {
  font-family: 'Sora', sans-serif;
  font-size: 1.1rem; font-weight: 800;
  color: var(--accent) !important;
  display: flex; align-items: center; gap: .5rem;
}
.topbar-tag {
  font-size: .68rem; font-weight: 500;
  color: var(--text3); letter-spacing: .04em;
}
.step-pill {
  font-size: .75rem; font-weight: 600;
  padding: .28rem .85rem; border-radius: 99px;
  color: var(--text3); background: var(--surf2);
  border: 1px solid var(--border);
}
.step-pill.done  { background: #e8f5ee; color: var(--green); border-color: #b8e0c8; }
.step-pill.active{ background: #eef3fc; color: var(--accent); border-color: #b8cff0; }

/* ── HERO ── */
.hero {
  background: linear-gradient(135deg, #2a4a8c 0%, #3b6cb7 60%, #2d5fa0 100%);
  border-radius: 14px; padding: 2.2rem 2.8rem;
  margin-bottom: 1.6rem; position: relative; overflow: hidden;
  box-shadow: 0 4px 20px rgba(40,80,180,.18);
}
.hero::before {
  content: ''; position: absolute; top: -60px; right: -60px;
  width: 300px; height: 300px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,.07) 0%, transparent 65%);
}
.hero h1 {
  font-family: 'Sora', sans-serif !important;
  font-size: 1.9rem !important; font-weight: 800 !important;
  color: #ffffff !important; margin: 0 0 .5rem !important; line-height: 1.25 !important;
}
.hero h1 span { color: #ffd166; }
.hero p { color: rgba(255,255,255,.82) !important; font-size: .93rem; margin: 0; line-height: 1.65; }

/* ── CARDS ── */
.card {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.2rem 1.4rem;
  box-shadow: var(--shadow);
}
.card-dark {
  background: var(--surf2);
  border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.1rem 1.3rem;
}
.kpi-lbl {
  font-size: .68rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .09em; color: var(--text3); margin-bottom: .3rem;
}
.kpi-val {
  font-family: 'Sora', sans-serif;
  font-size: 1.85rem; font-weight: 700; line-height: 1; color: var(--text);
}
.kpi-sub { font-size: .72rem; color: var(--text3); margin-top: .2rem; }

/* Colors */
.c-gold   { color: var(--gold)!important; }
.c-green  { color: var(--green)!important; }
.c-red    { color: var(--red)!important; }
.c-orange { color: var(--orange)!important; }
.c-blue   { color: var(--accent2)!important; }
.c-purple { color: var(--purple)!important; }
.c-teal   { color: var(--teal)!important; }

/* ── SECTION TITLE ── */
.sec {
  font-family: 'Sora', sans-serif; font-size: .92rem; font-weight: 700;
  color: var(--text); margin: 1.5rem 0 .7rem;
  padding-bottom: .3rem; border-bottom: 2px solid var(--border);
}

/* ── ALERTS ── */
.al {
  border-radius: var(--r); padding: .9rem 1.2rem; margin-bottom: .8rem;
  border-left: 4px solid; font-size: .86rem; line-height: 1.7; color: var(--text2);
  box-shadow: var(--shadow);
}
.al h4 { margin: 0 0 .35rem; font-size: .88rem; font-weight: 700; color: var(--text); }
.al ul, .al ol { margin: .3rem 0 0; padding-left: 1.2rem; color: var(--text2); }
.al ul li, .al ol li { margin-bottom: .2rem; }
.al strong { color: var(--text); }
.al code { color: var(--accent); background: rgba(59,108,183,.1); padding: 1px 5px; border-radius: 4px; }
.al-s { background: #f0faf5; border-color: var(--green); }
.al-s h4 { color: var(--green); }
.al-w { background: #fff8f0; border-color: var(--orange); }
.al-w h4 { color: var(--orange); }
.al-d { background: #fff0f0; border-color: var(--red); }
.al-d h4 { color: var(--red); }
.al-i { background: #f0f5fc; border-color: var(--accent); }
.al-i h4 { color: var(--accent); }
.al-p { background: #f5f0fc; border-color: var(--purple); }
.al-p h4 { color: var(--purple); }

/* ── PROGRESS BARS ── */
.prog-wrap { margin-bottom: .7rem; }
.prog-lbl {
  display: flex; justify-content: space-between;
  font-size: .8rem; font-weight: 600; color: var(--text2); margin-bottom: 4px;
}
.prog-bg { background: var(--surf2); border-radius: 99px; height: 8px; overflow: hidden;
           border: 1px solid var(--border); }
.prog-fill { height: 100%; border-radius: 99px; }

/* ── STEP BAR ── */
.step-row {
  display: flex; margin-bottom: 1.8rem;
  background: var(--surf); border: 1px solid var(--border);
  border-radius: var(--r); overflow: hidden; box-shadow: var(--shadow);
}
.step-item {
  flex: 1; padding: .85rem; text-align: center;
  font-size: .75rem; font-weight: 600; color: var(--text3);
  border-right: 1px solid var(--border);
}
.step-item:last-child { border-right: none; }
.step-item.active { background: #eef3fc; color: var(--accent); }
.step-item.done   { background: #f0faf5; color: var(--green); }
.step-num {
  display: block; font-size: 1.15rem;
  font-family: 'Sora', sans-serif; font-weight: 800; margin-bottom: 1px;
}

/* ── FORM BOX ── */
.form-box {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.7rem 1.9rem; margin-bottom: 1.2rem;
  box-shadow: var(--shadow);
}
.form-box h3 {
  font-family: 'Sora', sans-serif; font-size: .95rem; font-weight: 700;
  color: var(--accent); margin: 0 0 1.1rem;
}

/* ── BOBOT CHIP ── */
.bobot-chip {
  display: inline-flex; flex-direction: column; align-items: center;
  background: #eef3fc; border: 1px solid #b8cff0;
  border-radius: 8px; padding: .4rem .6rem; margin: .12rem;
}
.bobot-chip .sk { font-size: .63rem; color: var(--text3); margin-bottom: 1px; }
.bobot-chip .bv {
  font-size: .95rem; font-weight: 700; color: var(--accent2);
  font-family: 'Sora', sans-serif;
}

/* ── WEEK TABLE ── */
.week-card {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: 10px; padding: .95rem 1.1rem; margin-bottom: .6rem;
  box-shadow: var(--shadow);
}
.week-num {
  font-family: 'Sora', sans-serif; font-size: .73rem; font-weight: 700;
  color: var(--accent); text-transform: uppercase; letter-spacing: .08em;
  margin-bottom: .25rem;
}
.week-target { font-size: .84rem; font-weight: 600; color: var(--text); margin-bottom: .22rem; }
.week-tasks { font-size: .8rem; color: var(--text2); line-height: 1.65; }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stButton"] button[kind="primary"] {
  background: linear-gradient(135deg, #3b6cb7, #2a4a8c) !important;
  color: #ffffff !important; font-weight: 700 !important;
  font-family: 'Sora', sans-serif !important;
  border: none !important; border-radius: 8px !important;
  font-size: .88rem !important;
}
div[data-testid="stButton"] button {
  background: var(--surf) !important; color: var(--text2) !important;
  border: 1px solid var(--border) !important; border-radius: 8px !important;
  font-weight: 600 !important;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
  font-family: 'Sora', sans-serif !important; font-weight: 600 !important;
  font-size: .8rem !important; color: var(--text3) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--accent) !important; border-bottom-color: var(--accent) !important;
}
div[data-testid="stMetric"] {
  background: var(--surf) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important; padding: 1rem 1.2rem !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stMetric"] label {
  color: var(--text3) !important; font-size: .7rem !important;
  font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: .07em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: var(--text) !important; font-family: 'Sora', sans-serif !important;
}
div[data-testid="stExpander"] {
  background: var(--surf) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important; box-shadow: var(--shadow) !important;
}
div[data-testid="stExpander"] summary { color: var(--text2) !important; font-weight: 600 !important; }
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stRadio"] label {
  color: var(--text2) !important; font-weight: 600 !important; font-size: .84rem !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
  background: var(--surf) !important; color: var(--text) !important;
  border-color: var(--border) !important; font-size: .9rem !important;
}
.stCaption, [data-testid="stCaptionContainer"], .stCaption p {
  color: var(--text3) !important; font-size: .77rem !important;
}
hr { border-color: var(--border) !important; margin: 1.1rem 0 !important; }
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden;
  box-shadow: var(--shadow); }
div[data-baseweb="select"] { background: var(--surf) !important; }
div[data-baseweb="select"] * { color: var(--text) !important; }

/* Slider labels */
div[data-testid="stSlider"] label {
  color: var(--text2) !important; font-weight: 600 !important; font-size: .84rem !important;
}
/* Table in markdown */
table { border-collapse: collapse; width: 100%; font-size: .85rem; }
th { background: #eef3fc; color: var(--text); padding: .55rem .9rem;
     border: 1px solid var(--border); font-weight: 600; text-align: left; }
td { padding: .5rem .9rem; border: 1px solid var(--border); color: var(--text2); }
tr:nth-child(even) td { background: #f7f9fc; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
DEFAULTS = {
    'page': 'home', 'step': 1,
    'data': {}, 'result': None,
    '_cid': 0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def ckey(prefix="c"):
    st.session_state._cid += 1
    return f"{prefix}_{st.session_state._cid}"


# ══════════════════════════════════════════════════════════
# KONSTANTA
# ══════════════════════════════════════════════════════════
SKOR_MIN_TPS = 200
SKOR_MAX_TPS = 1000

SUBTES = ["PU", "PPU", "PBM", "PK", "LBI", "LBE", "PM"]
SUBTES_FULL = {
    "PU":  "Penalaran Umum",
    "PPU": "Pem. & Pengetahuan Umum",
    "PBM": "Pemahaman Bacaan & Menulis",
    "PK":  "Pengetahuan Kuantitatif",
    "LBI": "Literasi Bahasa Indonesia",
    "LBE": "Literasi Bahasa Inggris",
    "PM":  "Penalaran Matematika",
}
SUBTES_CLR = {
    "PU": "#c8890a", "PPU": "#3b6cb7", "PBM": "#7048c8",
    "PK": "#c0392b", "LBI": "#1a8a4a", "LBE": "#0d8a80", "PM": "#d4620a",
}

# Jenjang pilihan
DAFTAR_JENJANG = ["S1 (Sarjana)", "D3 (Diploma Tiga)"]

# Jurusan S1
DAFTAR_JURUSAN_S1 = [
    "Kedokteran","Kedokteran Gigi",
    "Teknik Sipil","Teknik Mesin","Teknik Elektro","Teknik Industri","Teknik Kimia","Teknik Informatika",
    "Matematika","Fisika","Kimia","Biologi","Statistika","Aktuaria",
    "Farmasi","Gizi","Keperawatan","Kesehatan Masyarakat",
    "Ilmu Hukum","Ekonomi","Manajemen","Akuntansi","Bisnis",
    "Psikologi","Ilmu Komunikasi","Hubungan Internasional","Administrasi Publik",
    "Sastra Inggris","Pendidikan Bahasa Indonesia","Pendidikan Bahasa Inggris",
    "Sosiologi","Ilmu Politik","Sejarah","Geografi"
]

# Jurusan D3 — program vokasi yang tersedia di SNBT/UTBK
DAFTAR_JURUSAN_D3 = [
    # Teknik & Rekayasa
    "D3 Teknik Sipil","D3 Teknik Mesin","D3 Teknik Elektro","D3 Teknik Kimia",
    "D3 Teknik Komputer","D3 Teknologi Informasi","D3 Teknik Mekatronika",
    # Bisnis & Manajemen
    "D3 Manajemen","D3 Akuntansi","D3 Administrasi Bisnis","D3 Perbankan & Keuangan",
    "D3 Manajemen Pemasaran","D3 Perpajakan",
    # Kesehatan
    "D3 Keperawatan","D3 Kebidanan","D3 Farmasi","D3 Gizi","D3 Analis Kesehatan",
    "D3 Rekam Medis","D3 Fisioterapi","D3 Radiologi",
    # Seni & Komunikasi
    "D3 Komunikasi","D3 Hubungan Masyarakat","D3 Desain Grafis","D3 Animasi",
    # Pariwisata & Sosial
    "D3 Pariwisata","D3 Perhotelan","D3 Bahasa Inggris",
    # Pertanian & Lingkungan
    "D3 Agribisnis","D3 Teknologi Pangan",
]

# Gabungan untuk tampilan (dipisahkan per jenjang di UI)
DAFTAR_JURUSAN = DAFTAR_JURUSAN_S1  # default S1

def get_daftar_jurusan(jenjang):
    if "D3" in jenjang:
        return DAFTAR_JURUSAN_D3
    return DAFTAR_JURUSAN_S1

# Bobot per jurusan (total = 1.0)
BOBOT_MAP = {
    "Kedokteran":             {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Kedokteran Gigi":        {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Teknik Informatika":     {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Sipil":           {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Mesin":           {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Elektro":         {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Industri":        {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Kimia":           {"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Matematika":             {"PU":.15,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.45},
    "Fisika":                 {"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.40},
    "Kimia":                  {"PU":.18,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.05,"PM":.35},
    "Biologi":                {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Statistika":             {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Aktuaria":               {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Farmasi":                {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.28},
    "Gizi":                   {"PU":.18,"PPU":.12,"PBM":.10,"PK":.15,"LBI":.12,"LBE":.08,"PM":.25},
    "Keperawatan":            {"PU":.18,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.23},
    "Kesehatan Masyarakat":   {"PU":.20,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.21},
    "Ilmu Hukum":             {"PU":.22,"PPU":.18,"PBM":.20,"PK":.08,"LBI":.18,"LBE":.10,"PM":.04},
    "Ekonomi":                {"PU":.20,"PPU":.15,"PBM":.10,"PK":.20,"LBI":.10,"LBE":.10,"PM":.15},
    "Manajemen":              {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Akuntansi":              {"PU":.18,"PPU":.15,"PBM":.10,"PK":.22,"LBI":.10,"LBE":.10,"PM":.15},
    "Bisnis":                 {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Psikologi":              {"PU":.22,"PPU":.15,"PBM":.18,"PK":.10,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Komunikasi":        {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Hubungan Internasional": {"PU":.20,"PPU":.15,"PBM":.15,"PK":.08,"LBI":.17,"LBE":.20,"PM":.05},
    "Administrasi Publik":    {"PU":.22,"PPU":.15,"PBM":.18,"PK":.08,"LBI":.20,"LBE":.10,"PM":.07},
    "Sastra Inggris":         {"PU":.12,"PPU":.12,"PBM":.20,"PK":.05,"LBI":.15,"LBE":.31,"PM":.05},
    "Pendidikan Bahasa Indonesia": {"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Pendidikan Bahasa Inggris":   {"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Sosiologi":              {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Politik":           {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Sejarah":                {"PU":.20,"PPU":.20,"PBM":.18,"PK":.05,"LBI":.22,"LBE":.10,"PM":.05},
    "Geografi":               {"PU":.20,"PPU":.15,"PBM":.15,"PK":.12,"LBI":.15,"LBE":.08,"PM":.15},
}
DEFAULT_BOBOT = {"PU":.15,"PPU":.15,"PBM":.15,"PK":.15,"LBI":.15,"LBE":.15,"PM":.10}

# ── Bobot D3 — vokasi lebih menekankan kemampuan teknis & literasi praktis ──
BOBOT_MAP_D3 = {
    # Teknik & Rekayasa
    "D3 Teknik Sipil":         {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Teknik Mesin":         {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Teknik Elektro":       {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Teknik Kimia":         {"PU":.17,"PPU":.08,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.05,"PM":.38},
    "D3 Teknik Komputer":      {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.08,"PM":.37},
    "D3 Teknologi Informasi":  {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.08,"PM":.37},
    "D3 Teknik Mekatronika":   {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    # Bisnis & Manajemen
    "D3 Manajemen":            {"PU":.20,"PPU":.15,"PBM":.15,"PK":.18,"LBI":.15,"LBE":.10,"PM":.07},
    "D3 Akuntansi":            {"PU":.18,"PPU":.13,"PBM":.12,"PK":.25,"LBI":.12,"LBE":.08,"PM":.12},
    "D3 Administrasi Bisnis":  {"PU":.20,"PPU":.15,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.10,"PM":.07},
    "D3 Perbankan & Keuangan": {"PU":.18,"PPU":.13,"PBM":.12,"PK":.25,"LBI":.12,"LBE":.08,"PM":.12},
    "D3 Manajemen Pemasaran":  {"PU":.20,"PPU":.15,"PBM":.17,"PK":.12,"LBI":.18,"LBE":.12,"PM":.06},
    "D3 Perpajakan":           {"PU":.18,"PPU":.12,"PBM":.12,"PK":.25,"LBI":.13,"LBE":.08,"PM":.12},
    # Kesehatan
    "D3 Keperawatan":          {"PU":.18,"PPU":.13,"PBM":.13,"PK":.12,"LBI":.17,"LBE":.08,"PM":.19},
    "D3 Kebidanan":            {"PU":.18,"PPU":.14,"PBM":.13,"PK":.12,"LBI":.17,"LBE":.08,"PM":.18},
    "D3 Farmasi":              {"PU":.17,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.08,"PM":.26},
    "D3 Gizi":                 {"PU":.18,"PPU":.13,"PBM":.10,"PK":.15,"LBI":.13,"LBE":.08,"PM":.23},
    "D3 Analis Kesehatan":     {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
    "D3 Rekam Medis":          {"PU":.18,"PPU":.12,"PBM":.14,"PK":.15,"LBI":.16,"LBE":.08,"PM":.17},
    "D3 Fisioterapi":          {"PU":.19,"PPU":.13,"PBM":.12,"PK":.13,"LBI":.15,"LBE":.08,"PM":.20},
    "D3 Radiologi":            {"PU":.18,"PPU":.12,"PBM":.08,"PK":.20,"LBI":.10,"LBE":.07,"PM":.25},
    # Seni & Komunikasi
    "D3 Komunikasi":           {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "D3 Hubungan Masyarakat":  {"PU":.20,"PPU":.15,"PBM":.22,"PK":.07,"LBI":.22,"LBE":.10,"PM":.04},
    "D3 Desain Grafis":        {"PU":.18,"PPU":.10,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.12,"PM":.12},
    "D3 Animasi":              {"PU":.18,"PPU":.10,"PBM":.15,"PK":.15,"LBI":.17,"LBE":.12,"PM":.13},
    # Pariwisata & Sosial
    "D3 Pariwisata":           {"PU":.18,"PPU":.13,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.18,"PM":.07},
    "D3 Perhotelan":           {"PU":.18,"PPU":.12,"PBM":.17,"PK":.08,"LBI":.18,"LBE":.20,"PM":.07},
    "D3 Bahasa Inggris":       {"PU":.13,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.15,"LBE":.33,"PM":.04},
    # Pertanian & Lingkungan
    "D3 Agribisnis":           {"PU":.20,"PPU":.15,"PBM":.12,"PK":.15,"LBI":.15,"LBE":.08,"PM":.15},
    "D3 Teknologi Pangan":     {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
}

DEFAULT_BOBOT_D3 = {"PU":.18,"PPU":.12,"PBM":.13,"PK":.15,"LBI":.15,"LBE":.10,"PM":.17}

def get_bobot(j):
    if j in BOBOT_MAP_D3:
        return BOBOT_MAP_D3[j]
    return BOBOT_MAP.get(j, DEFAULT_BOBOT)

# ══════════════════════════════════════════════════════════
# PTN DATA — Skor aman per jurusan (berbasis UTBK 2023/2024)
# Format: {jurusan: {"mn": min_aman, "mx": maks_aman}}
# Diisi berdasarkan data passing grade UTBK 2023-2024 yang dipublikasikan
# ══════════════════════════════════════════════════════════

# Skor referensi per PTN per jurusan (UTBK 2023/2024, skala 1000)
# Sumber: LTMPT/SNPMB 2023-2024, berbagai referensi resmi dan situs akademik
PTN_JURUSAN_DATA = {
    "Universitas Indonesia (UI)": {
        "Kedokteran":             {"mn": 845, "mx": 910},
        "Kedokteran Gigi":        {"mn": 810, "mx": 875},
        "Teknik Informatika":     {"mn": 800, "mx": 870},
        "Teknik Sipil":           {"mn": 780, "mx": 845},
        "Teknik Mesin":           {"mn": 775, "mx": 840},
        "Teknik Elektro":         {"mn": 790, "mx": 855},
        "Teknik Industri":        {"mn": 785, "mx": 850},
        "Teknik Kimia":           {"mn": 775, "mx": 840},
        "Matematika":             {"mn": 765, "mx": 830},
        "Fisika":                 {"mn": 755, "mx": 820},
        "Kimia":                  {"mn": 755, "mx": 820},
        "Biologi":                {"mn": 745, "mx": 810},
        "Statistika":             {"mn": 770, "mx": 835},
        "Aktuaria":               {"mn": 780, "mx": 845},
        "Farmasi":                {"mn": 790, "mx": 855},
        "Gizi":                   {"mn": 760, "mx": 825},
        "Keperawatan":            {"mn": 730, "mx": 795},
        "Kesehatan Masyarakat":   {"mn": 745, "mx": 810},
        "Ilmu Hukum":             {"mn": 765, "mx": 830},
        "Ekonomi":                {"mn": 775, "mx": 840},
        "Manajemen":              {"mn": 770, "mx": 835},
        "Akuntansi":              {"mn": 775, "mx": 840},
        "Bisnis":                 {"mn": 770, "mx": 835},
        "Psikologi":              {"mn": 770, "mx": 835},
        "Ilmu Komunikasi":        {"mn": 760, "mx": 825},
        "Hubungan Internasional": {"mn": 775, "mx": 840},
        "Administrasi Publik":    {"mn": 750, "mx": 815},
        "Sastra Inggris":         {"mn": 745, "mx": 810},
        "Pendidikan Bahasa Indonesia": {"mn": 720, "mx": 785},
        "Pendidikan Bahasa Inggris":   {"mn": 730, "mx": 795},
        "Sosiologi":              {"mn": 745, "mx": 810},
        "Ilmu Politik":           {"mn": 755, "mx": 820},
        "Sejarah":                {"mn": 720, "mx": 785},
        "Geografi":               {"mn": 720, "mx": 785},
        "_default":               {"mn": 760, "mx": 830},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Gadjah Mada (UGM)": {
        "Kedokteran":             {"mn": 840, "mx": 905},
        "Kedokteran Gigi":        {"mn": 805, "mx": 870},
        "Teknik Informatika":     {"mn": 795, "mx": 865},
        "Teknik Sipil":           {"mn": 770, "mx": 840},
        "Teknik Mesin":           {"mn": 765, "mx": 835},
        "Teknik Elektro":         {"mn": 780, "mx": 850},
        "Teknik Industri":        {"mn": 775, "mx": 845},
        "Teknik Kimia":           {"mn": 765, "mx": 835},
        "Matematika":             {"mn": 755, "mx": 825},
        "Fisika":                 {"mn": 745, "mx": 815},
        "Kimia":                  {"mn": 745, "mx": 815},
        "Biologi":                {"mn": 740, "mx": 810},
        "Statistika":             {"mn": 765, "mx": 835},
        "Aktuaria":               {"mn": 775, "mx": 845},
        "Farmasi":                {"mn": 780, "mx": 850},
        "Gizi":                   {"mn": 750, "mx": 820},
        "Keperawatan":            {"mn": 720, "mx": 790},
        "Kesehatan Masyarakat":   {"mn": 735, "mx": 805},
        "Ilmu Hukum":             {"mn": 755, "mx": 825},
        "Ekonomi":                {"mn": 765, "mx": 835},
        "Manajemen":              {"mn": 760, "mx": 830},
        "Akuntansi":              {"mn": 765, "mx": 835},
        "Bisnis":                 {"mn": 760, "mx": 830},
        "Psikologi":              {"mn": 760, "mx": 830},
        "Ilmu Komunikasi":        {"mn": 750, "mx": 820},
        "Hubungan Internasional": {"mn": 765, "mx": 835},
        "Administrasi Publik":    {"mn": 740, "mx": 810},
        "Sastra Inggris":         {"mn": 735, "mx": 805},
        "Pendidikan Bahasa Indonesia": {"mn": 715, "mx": 785},
        "Pendidikan Bahasa Inggris":   {"mn": 725, "mx": 795},
        "Sosiologi":              {"mn": 740, "mx": 810},
        "Ilmu Politik":           {"mn": 750, "mx": 820},
        "Sejarah":                {"mn": 715, "mx": 785},
        "Geografi":               {"mn": 715, "mx": 785},
        "_default":               {"mn": 755, "mx": 825},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Institut Teknologi Bandung (ITB)": {
        "Teknik Informatika":     {"mn": 855, "mx": 930},
        "Teknik Sipil":           {"mn": 820, "mx": 895},
        "Teknik Mesin":           {"mn": 815, "mx": 890},
        "Teknik Elektro":         {"mn": 835, "mx": 910},
        "Teknik Industri":        {"mn": 825, "mx": 900},
        "Teknik Kimia":           {"mn": 815, "mx": 890},
        "Matematika":             {"mn": 800, "mx": 875},
        "Fisika":                 {"mn": 795, "mx": 870},
        "Kimia":                  {"mn": 790, "mx": 865},
        "Statistika":             {"mn": 810, "mx": 885},
        "Aktuaria":               {"mn": 815, "mx": 890},
        "Biologi":                {"mn": 780, "mx": 855},
        "Gizi":                   {"mn": 775, "mx": 850},
        "Farmasi":                {"mn": 785, "mx": 860},
        "Kedokteran":             {"mn": 870, "mx": 945},
        "Ilmu Komunikasi":        {"mn": 770, "mx": 845},
        "Manajemen":              {"mn": 790, "mx": 865},
        "_default":               {"mn": 810, "mx": 885},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Padjadjaran (Unpad)": {
        "Kedokteran":             {"mn": 810, "mx": 880},
        "Kedokteran Gigi":        {"mn": 775, "mx": 845},
        "Teknik Informatika":     {"mn": 760, "mx": 830},
        "Teknik Sipil":           {"mn": 740, "mx": 810},
        "Teknik Mesin":           {"mn": 735, "mx": 805},
        "Farmasi":                {"mn": 760, "mx": 830},
        "Matematika":             {"mn": 730, "mx": 800},
        "Biologi":                {"mn": 715, "mx": 785},
        "Kimia":                  {"mn": 720, "mx": 790},
        "Fisika":                 {"mn": 715, "mx": 785},
        "Statistika":             {"mn": 735, "mx": 805},
        "Akuntansi":              {"mn": 740, "mx": 810},
        "Manajemen":              {"mn": 738, "mx": 808},
        "Ilmu Hukum":             {"mn": 730, "mx": 800},
        "Psikologi":              {"mn": 735, "mx": 805},
        "Ilmu Komunikasi":        {"mn": 728, "mx": 798},
        "Hubungan Internasional": {"mn": 738, "mx": 808},
        "Gizi":                   {"mn": 725, "mx": 795},
        "Keperawatan":            {"mn": 700, "mx": 770},
        "Kesehatan Masyarakat":   {"mn": 710, "mx": 780},
        "_default":               {"mn": 730, "mx": 800},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Institut Pertanian Bogor (IPB)": {
        "Teknik Informatika":     {"mn": 750, "mx": 825},
        "Statistika":             {"mn": 745, "mx": 820},
        "Matematika":             {"mn": 730, "mx": 805},
        "Biologi":                {"mn": 720, "mx": 795},
        "Kimia":                  {"mn": 718, "mx": 793},
        "Fisika":                 {"mn": 715, "mx": 790},
        "Gizi":                   {"mn": 730, "mx": 805},
        "Farmasi":                {"mn": 738, "mx": 813},
        "Kesehatan Masyarakat":   {"mn": 710, "mx": 785},
        "Manajemen":              {"mn": 725, "mx": 800},
        "Akuntansi":              {"mn": 720, "mx": 795},
        "Ekonomi":                {"mn": 728, "mx": 803},
        "Teknik Sipil":           {"mn": 720, "mx": 795},
        "_default":               {"mn": 720, "mx": 795},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Diponegoro (Undip)": {
        "Kedokteran":             {"mn": 790, "mx": 855},
        "Kedokteran Gigi":        {"mn": 755, "mx": 820},
        "Teknik Informatika":     {"mn": 740, "mx": 808},
        "Teknik Sipil":           {"mn": 720, "mx": 788},
        "Teknik Mesin":           {"mn": 715, "mx": 783},
        "Teknik Elektro":         {"mn": 725, "mx": 793},
        "Teknik Industri":        {"mn": 720, "mx": 788},
        "Teknik Kimia":           {"mn": 715, "mx": 783},
        "Matematika":             {"mn": 705, "mx": 773},
        "Fisika":                 {"mn": 698, "mx": 766},
        "Statistika":             {"mn": 715, "mx": 783},
        "Farmasi":                {"mn": 730, "mx": 798},
        "Ilmu Hukum":             {"mn": 705, "mx": 773},
        "Manajemen":              {"mn": 710, "mx": 778},
        "Akuntansi":              {"mn": 715, "mx": 783},
        "Psikologi":              {"mn": 708, "mx": 776},
        "Ilmu Komunikasi":        {"mn": 700, "mx": 768},
        "Kesehatan Masyarakat":   {"mn": 698, "mx": 766},
        "_default":               {"mn": 705, "mx": 775},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Airlangga (Unair)": {
        "Kedokteran":             {"mn": 820, "mx": 885},
        "Kedokteran Gigi":        {"mn": 780, "mx": 845},
        "Farmasi":                {"mn": 760, "mx": 825},
        "Keperawatan":            {"mn": 715, "mx": 780},
        "Kesehatan Masyarakat":   {"mn": 720, "mx": 785},
        "Teknik Informatika":     {"mn": 740, "mx": 805},
        "Ilmu Hukum":             {"mn": 720, "mx": 785},
        "Manajemen":              {"mn": 725, "mx": 790},
        "Akuntansi":              {"mn": 725, "mx": 790},
        "Ekonomi":                {"mn": 728, "mx": 793},
        "Psikologi":              {"mn": 720, "mx": 785},
        "Ilmu Komunikasi":        {"mn": 715, "mx": 780},
        "Matematika":             {"mn": 705, "mx": 770},
        "_default":               {"mn": 720, "mx": 790},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Brawijaya (UB)": {
        "Kedokteran":             {"mn": 780, "mx": 845},
        "Kedokteran Gigi":        {"mn": 745, "mx": 810},
        "Teknik Informatika":     {"mn": 720, "mx": 785},
        "Teknik Sipil":           {"mn": 700, "mx": 765},
        "Farmasi":                {"mn": 730, "mx": 795},
        "Ilmu Hukum":             {"mn": 700, "mx": 765},
        "Manajemen":              {"mn": 705, "mx": 770},
        "Akuntansi":              {"mn": 705, "mx": 770},
        "Psikologi":              {"mn": 700, "mx": 765},
        "Ilmu Komunikasi":        {"mn": 695, "mx": 760},
        "Teknik Mesin":           {"mn": 695, "mx": 760},
        "Teknik Elektro":         {"mn": 705, "mx": 770},
        "Matematika":             {"mn": 688, "mx": 753},
        "Biologi":                {"mn": 685, "mx": 750},
        "Gizi":                   {"mn": 695, "mx": 760},
        "Kesehatan Masyarakat":   {"mn": 690, "mx": 755},
        "_default":               {"mn": 695, "mx": 765},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Institut Teknologi Sepuluh Nopember (ITS)": {
        "Teknik Informatika":     {"mn": 800, "mx": 870},
        "Teknik Elektro":         {"mn": 780, "mx": 850},
        "Teknik Sipil":           {"mn": 755, "mx": 825},
        "Teknik Mesin":           {"mn": 750, "mx": 820},
        "Teknik Industri":        {"mn": 758, "mx": 828},
        "Teknik Kimia":           {"mn": 745, "mx": 815},
        "Matematika":             {"mn": 735, "mx": 805},
        "Fisika":                 {"mn": 725, "mx": 795},
        "Kimia":                  {"mn": 720, "mx": 790},
        "Statistika":             {"mn": 740, "mx": 810},
        "_default":               {"mn": 750, "mx": 820},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Sebelas Maret (UNS)": {
        "Kedokteran":             {"mn": 755, "mx": 820},
        "Kedokteran Gigi":        {"mn": 720, "mx": 785},
        "Teknik Informatika":     {"mn": 700, "mx": 765},
        "Teknik Sipil":           {"mn": 680, "mx": 745},
        "Ilmu Hukum":             {"mn": 678, "mx": 743},
        "Manajemen":              {"mn": 680, "mx": 745},
        "Akuntansi":              {"mn": 682, "mx": 747},
        "Psikologi":              {"mn": 678, "mx": 743},
        "Farmasi":                {"mn": 698, "mx": 763},
        "Biologi":                {"mn": 658, "mx": 723},
        "Fisika":                 {"mn": 650, "mx": 715},
        "Matematika":             {"mn": 660, "mx": 725},
        "Gizi":                   {"mn": 665, "mx": 730},
        "Sosiologi":              {"mn": 650, "mx": 715},
        "Ilmu Komunikasi":        {"mn": 660, "mx": 725},
        "_default":               {"mn": 665, "mx": 735},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Hasanuddin (Unhas)": {
        "Kedokteran":             {"mn": 760, "mx": 825},
        "Kedokteran Gigi":        {"mn": 725, "mx": 790},
        "Teknik Informatika":     {"mn": 700, "mx": 765},
        "Teknik Sipil":           {"mn": 678, "mx": 743},
        "Teknik Mesin":           {"mn": 672, "mx": 737},
        "Farmasi":                {"mn": 710, "mx": 775},
        "Ilmu Hukum":             {"mn": 672, "mx": 737},
        "Manajemen":              {"mn": 668, "mx": 733},
        "Akuntansi":              {"mn": 670, "mx": 735},
        "Psikologi":              {"mn": 665, "mx": 730},
        "Matematika":             {"mn": 648, "mx": 713},
        "Biologi":                {"mn": 642, "mx": 707},
        "_default":               {"mn": 660, "mx": 730},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Negeri Yogyakarta (UNY)": {
        "Pendidikan Bahasa Indonesia": {"mn": 630, "mx": 700},
        "Pendidikan Bahasa Inggris":   {"mn": 640, "mx": 710},
        "Psikologi":              {"mn": 638, "mx": 708},
        "Ilmu Komunikasi":        {"mn": 625, "mx": 695},
        "Matematika":             {"mn": 635, "mx": 705},
        "Biologi":                {"mn": 618, "mx": 688},
        "Fisika":                 {"mn": 612, "mx": 682},
        "Ilmu Hukum":             {"mn": 620, "mx": 690},
        "Manajemen":              {"mn": 625, "mx": 695},
        "Akuntansi":              {"mn": 622, "mx": 692},
        "Sosiologi":              {"mn": 615, "mx": 685},
        "_default":               {"mn": 620, "mx": 695},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Semarang (UNNES)": {
        "Pendidikan Bahasa Indonesia": {"mn": 615, "mx": 685},
        "Pendidikan Bahasa Inggris":   {"mn": 622, "mx": 692},
        "Matematika":             {"mn": 618, "mx": 688},
        "Biologi":                {"mn": 605, "mx": 675},
        "Fisika":                 {"mn": 600, "mx": 670},
        "Ilmu Hukum":             {"mn": 608, "mx": 678},
        "Manajemen":              {"mn": 610, "mx": 680},
        "Sosiologi":              {"mn": 600, "mx": 670},
        "_default":               {"mn": 605, "mx": 678},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Malang (UM)": {
        "Pendidikan Bahasa Indonesia": {"mn": 612, "mx": 682},
        "Pendidikan Bahasa Inggris":   {"mn": 620, "mx": 690},
        "Matematika":             {"mn": 615, "mx": 685},
        "Psikologi":              {"mn": 625, "mx": 695},
        "Biologi":                {"mn": 603, "mx": 673},
        "Ilmu Hukum":             {"mn": 605, "mx": 675},
        "Akuntansi":              {"mn": 610, "mx": 680},
        "Manajemen":              {"mn": 608, "mx": 678},
        "Sosiologi":              {"mn": 598, "mx": 668},
        "_default":               {"mn": 605, "mx": 678},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Andalas (Unand)": {
        "Kedokteran":             {"mn": 728, "mx": 798},
        "Kedokteran Gigi":        {"mn": 695, "mx": 765},
        "Teknik Informatika":     {"mn": 675, "mx": 745},
        "Farmasi":                {"mn": 685, "mx": 755},
        "Ilmu Hukum":             {"mn": 655, "mx": 725},
        "Manajemen":              {"mn": 650, "mx": 720},
        "Teknik Sipil":           {"mn": 650, "mx": 720},
        "Biologi":                {"mn": 625, "mx": 695},
        "Matematika":             {"mn": 628, "mx": 698},
        "Psikologi":              {"mn": 648, "mx": 718},
        "_default":               {"mn": 640, "mx": 715},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sumatera Utara (USU)": {
        "Kedokteran":             {"mn": 720, "mx": 790},
        "Kedokteran Gigi":        {"mn": 685, "mx": 755},
        "Teknik Informatika":     {"mn": 660, "mx": 730},
        "Farmasi":                {"mn": 668, "mx": 738},
        "Ilmu Hukum":             {"mn": 640, "mx": 710},
        "Manajemen":              {"mn": 638, "mx": 708},
        "Teknik Sipil":           {"mn": 635, "mx": 705},
        "Biologi":                {"mn": 612, "mx": 682},
        "Matematika":             {"mn": 615, "mx": 685},
        "Psikologi":              {"mn": 635, "mx": 705},
        "Akuntansi":              {"mn": 640, "mx": 710},
        "_default":               {"mn": 625, "mx": 698},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sriwijaya (Unsri)": {
        "Kedokteran":             {"mn": 695, "mx": 765},
        "Kedokteran Gigi":        {"mn": 658, "mx": 728},
        "Teknik Informatika":     {"mn": 635, "mx": 705},
        "Teknik Sipil":           {"mn": 612, "mx": 682},
        "Farmasi":                {"mn": 638, "mx": 708},
        "Ilmu Hukum":             {"mn": 608, "mx": 678},
        "Manajemen":              {"mn": 605, "mx": 675},
        "Akuntansi":              {"mn": 608, "mx": 678},
        "Matematika":             {"mn": 595, "mx": 665},
        "Biologi":                {"mn": 588, "mx": 658},
        "_default":               {"mn": 600, "mx": 672},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Lampung (Unila)": {
        "Kedokteran":             {"mn": 682, "mx": 752},
        "Teknik Informatika":     {"mn": 618, "mx": 688},
        "Teknik Sipil":           {"mn": 598, "mx": 668},
        "Ilmu Hukum":             {"mn": 595, "mx": 665},
        "Manajemen":              {"mn": 592, "mx": 662},
        "Akuntansi":              {"mn": 592, "mx": 662},
        "Matematika":             {"mn": 582, "mx": 652},
        "Biologi":                {"mn": 575, "mx": 645},
        "Psikologi":              {"mn": 590, "mx": 660},
        "_default":               {"mn": 585, "mx": 658},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Jember (Unej)": {
        "Kedokteran":             {"mn": 680, "mx": 748},
        "Farmasi":                {"mn": 622, "mx": 690},
        "Teknik Informatika":     {"mn": 612, "mx": 680},
        "Teknik Sipil":           {"mn": 595, "mx": 663},
        "Ilmu Hukum":             {"mn": 590, "mx": 658},
        "Manajemen":              {"mn": 585, "mx": 653},
        "Akuntansi":              {"mn": 588, "mx": 656},
        "Matematika":             {"mn": 578, "mx": 646},
        "Biologi":                {"mn": 568, "mx": 636},
        "_default":               {"mn": 578, "mx": 650},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Riau (Unri)": {
        "Kedokteran":             {"mn": 668, "mx": 738},
        "Teknik Informatika":     {"mn": 605, "mx": 675},
        "Teknik Sipil":           {"mn": 582, "mx": 652},
        "Ilmu Hukum":             {"mn": 578, "mx": 648},
        "Manajemen":              {"mn": 572, "mx": 642},
        "Matematika":             {"mn": 562, "mx": 632},
        "Biologi":                {"mn": 555, "mx": 625},
        "Akuntansi":              {"mn": 568, "mx": 638},
        "Farmasi":                {"mn": 580, "mx": 650},
        "_default":               {"mn": 565, "mx": 638},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
}

DAFTAR_PTN = list(PTN_JURUSAN_DATA.keys())

# ══════════════════════════════════════════════════════════
# D3 PTN SCORE DATA — Skor aman per prodi D3 per PTN
# Berbasis SNPMB/BPPP Kemdikbud & media pendidikan 2025/2026
# D3 umumnya 35–80 poin lebih rendah dari S1 sejenis
# (persaingan tetap ada karena kuota D3 lebih kecil)
# ══════════════════════════════════════════════════════════
PTN_D3_DATA = {
    "Universitas Indonesia (UI)": {
        "D3 Teknik Sipil":         {"mn": 690, "mx": 760},
        "D3 Teknik Mesin":         {"mn": 685, "mx": 755},
        "D3 Teknik Elektro":       {"mn": 695, "mx": 765},
        "D3 Teknik Kimia":         {"mn": 685, "mx": 755},
        "D3 Teknologi Informasi":  {"mn": 698, "mx": 768},
        "D3 Teknik Komputer":      {"mn": 698, "mx": 768},
        "D3 Manajemen":            {"mn": 680, "mx": 748},
        "D3 Akuntansi":            {"mn": 682, "mx": 750},
        "D3 Administrasi Bisnis":  {"mn": 672, "mx": 740},
        "D3 Perbankan & Keuangan": {"mn": 675, "mx": 743},
        "D3 Keperawatan":          {"mn": 635, "mx": 703},
        "D3 Farmasi":              {"mn": 688, "mx": 756},
        "D3 Gizi":                 {"mn": 660, "mx": 728},
        "D3 Komunikasi":           {"mn": 665, "mx": 733},
        "D3 Hubungan Masyarakat":  {"mn": 658, "mx": 726},
        "_default":                {"mn": 665, "mx": 735},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Gadjah Mada (UGM)": {
        "D3 Teknik Sipil":         {"mn": 682, "mx": 752},
        "D3 Teknik Mesin":         {"mn": 678, "mx": 748},
        "D3 Teknik Elektro":       {"mn": 688, "mx": 758},
        "D3 Teknologi Informasi":  {"mn": 692, "mx": 762},
        "D3 Teknik Komputer":      {"mn": 692, "mx": 762},
        "D3 Manajemen":            {"mn": 672, "mx": 742},
        "D3 Akuntansi":            {"mn": 675, "mx": 745},
        "D3 Administrasi Bisnis":  {"mn": 665, "mx": 735},
        "D3 Perbankan & Keuangan": {"mn": 668, "mx": 738},
        "D3 Keperawatan":          {"mn": 625, "mx": 695},
        "D3 Farmasi":              {"mn": 680, "mx": 750},
        "D3 Gizi":                 {"mn": 652, "mx": 722},
        "D3 Komunikasi":           {"mn": 658, "mx": 728},
        "D3 Pariwisata":           {"mn": 615, "mx": 685},
        "D3 Perpajakan":           {"mn": 660, "mx": 730},
        "D3 Agribisnis":           {"mn": 620, "mx": 690},
        "_default":                {"mn": 658, "mx": 728},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Institut Teknologi Bandung (ITB)": {
        "D3 Teknik Sipil":         {"mn": 725, "mx": 800},
        "D3 Teknik Mesin":         {"mn": 720, "mx": 795},
        "D3 Teknik Elektro":       {"mn": 730, "mx": 805},
        "D3 Teknik Kimia":         {"mn": 718, "mx": 793},
        "D3 Teknologi Informasi":  {"mn": 732, "mx": 807},
        "D3 Teknik Komputer":      {"mn": 732, "mx": 807},
        "D3 Teknik Mekatronika":   {"mn": 715, "mx": 790},
        "D3 Desain Grafis":        {"mn": 685, "mx": 755},
        "D3 Animasi":              {"mn": 680, "mx": 750},
        "_default":                {"mn": 715, "mx": 790},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Padjadjaran (Unpad)": {
        "D3 Teknik Komputer":      {"mn": 648, "mx": 718},
        "D3 Teknologi Informasi":  {"mn": 648, "mx": 718},
        "D3 Manajemen":            {"mn": 632, "mx": 702},
        "D3 Akuntansi":            {"mn": 635, "mx": 705},
        "D3 Administrasi Bisnis":  {"mn": 625, "mx": 695},
        "D3 Perbankan & Keuangan": {"mn": 628, "mx": 698},
        "D3 Keperawatan":          {"mn": 598, "mx": 668},
        "D3 Kebidanan":            {"mn": 595, "mx": 665},
        "D3 Farmasi":              {"mn": 640, "mx": 710},
        "D3 Gizi":                 {"mn": 615, "mx": 685},
        "D3 Analis Kesehatan":     {"mn": 615, "mx": 685},
        "D3 Komunikasi":           {"mn": 618, "mx": 688},
        "D3 Hubungan Masyarakat":  {"mn": 612, "mx": 682},
        "D3 Pariwisata":           {"mn": 598, "mx": 668},
        "_default":                {"mn": 620, "mx": 690},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Institut Pertanian Bogor (IPB)": {
        "D3 Teknologi Pangan":     {"mn": 628, "mx": 698},
        "D3 Agribisnis":           {"mn": 618, "mx": 688},
        "D3 Manajemen":            {"mn": 605, "mx": 675},
        "D3 Akuntansi":            {"mn": 608, "mx": 678},
        "D3 Teknologi Informasi":  {"mn": 625, "mx": 695},
        "D3 Gizi":                 {"mn": 615, "mx": 685},
        "D3 Komunikasi":           {"mn": 595, "mx": 665},
        "D3 Farmasi":              {"mn": 618, "mx": 688},
        "_default":                {"mn": 608, "mx": 678},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Diponegoro (Undip)": {
        "D3 Teknik Sipil":         {"mn": 605, "mx": 675},
        "D3 Teknik Mesin":         {"mn": 600, "mx": 670},
        "D3 Teknik Elektro":       {"mn": 608, "mx": 678},
        "D3 Teknik Kimia":         {"mn": 598, "mx": 668},
        "D3 Teknologi Informasi":  {"mn": 618, "mx": 688},
        "D3 Teknik Komputer":      {"mn": 615, "mx": 685},
        "D3 Manajemen":            {"mn": 588, "mx": 658},
        "D3 Akuntansi":            {"mn": 590, "mx": 660},
        "D3 Perbankan & Keuangan": {"mn": 585, "mx": 655},
        "D3 Perpajakan":           {"mn": 588, "mx": 658},
        "D3 Keperawatan":          {"mn": 562, "mx": 632},
        "D3 Farmasi":              {"mn": 598, "mx": 668},
        "D3 Analis Kesehatan":     {"mn": 575, "mx": 645},
        "D3 Komunikasi":           {"mn": 575, "mx": 645},
        "_default":                {"mn": 585, "mx": 655},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Airlangga (Unair)": {
        "D3 Teknologi Informasi":  {"mn": 618, "mx": 688},
        "D3 Teknik Komputer":      {"mn": 615, "mx": 685},
        "D3 Manajemen":            {"mn": 600, "mx": 670},
        "D3 Akuntansi":            {"mn": 602, "mx": 672},
        "D3 Perbankan & Keuangan": {"mn": 595, "mx": 665},
        "D3 Keperawatan":          {"mn": 575, "mx": 645},
        "D3 Kebidanan":            {"mn": 568, "mx": 638},
        "D3 Farmasi":              {"mn": 618, "mx": 688},
        "D3 Gizi":                 {"mn": 580, "mx": 650},
        "D3 Analis Kesehatan":     {"mn": 582, "mx": 652},
        "D3 Rekam Medis":          {"mn": 565, "mx": 635},
        "D3 Komunikasi":           {"mn": 582, "mx": 652},
        "_default":                {"mn": 585, "mx": 658},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Brawijaya (UB)": {
        "D3 Teknik Sipil":         {"mn": 575, "mx": 645},
        "D3 Teknologi Informasi":  {"mn": 590, "mx": 660},
        "D3 Teknik Komputer":      {"mn": 588, "mx": 658},
        "D3 Manajemen":            {"mn": 572, "mx": 642},
        "D3 Akuntansi":            {"mn": 572, "mx": 642},
        "D3 Administrasi Bisnis":  {"mn": 565, "mx": 635},
        "D3 Perbankan & Keuangan": {"mn": 562, "mx": 632},
        "D3 Keperawatan":          {"mn": 548, "mx": 618},
        "D3 Kebidanan":            {"mn": 542, "mx": 612},
        "D3 Farmasi":              {"mn": 578, "mx": 648},
        "D3 Gizi":                 {"mn": 555, "mx": 625},
        "D3 Agribisnis":           {"mn": 538, "mx": 608},
        "D3 Teknologi Pangan":     {"mn": 545, "mx": 615},
        "D3 Komunikasi":           {"mn": 552, "mx": 622},
        "D3 Pariwisata":           {"mn": 525, "mx": 595},
        "_default":                {"mn": 558, "mx": 628},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Institut Teknologi Sepuluh Nopember (ITS)": {
        "D3 Teknik Sipil":         {"mn": 640, "mx": 712},
        "D3 Teknik Mesin":         {"mn": 635, "mx": 707},
        "D3 Teknik Elektro":       {"mn": 645, "mx": 717},
        "D3 Teknik Kimia":         {"mn": 628, "mx": 700},
        "D3 Teknologi Informasi":  {"mn": 652, "mx": 724},
        "D3 Teknik Komputer":      {"mn": 648, "mx": 720},
        "D3 Teknik Mekatronika":   {"mn": 632, "mx": 704},
        "D3 Manajemen":            {"mn": 605, "mx": 675},
        "D3 Desain Grafis":        {"mn": 598, "mx": 668},
        "_default":                {"mn": 628, "mx": 700},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Sebelas Maret (UNS)": {
        "D3 Teknik Sipil":         {"mn": 555, "mx": 625},
        "D3 Teknologi Informasi":  {"mn": 562, "mx": 632},
        "D3 Teknik Komputer":      {"mn": 558, "mx": 628},
        "D3 Manajemen":            {"mn": 545, "mx": 615},
        "D3 Akuntansi":            {"mn": 548, "mx": 618},
        "D3 Administrasi Bisnis":  {"mn": 538, "mx": 608},
        "D3 Perpajakan":           {"mn": 545, "mx": 615},
        "D3 Perbankan & Keuangan": {"mn": 542, "mx": 612},
        "D3 Keperawatan":          {"mn": 520, "mx": 590},
        "D3 Farmasi":              {"mn": 548, "mx": 618},
        "D3 Komunikasi":           {"mn": 525, "mx": 595},
        "D3 Pariwisata":           {"mn": 505, "mx": 575},
        "_default":                {"mn": 535, "mx": 608},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Hasanuddin (Unhas)": {
        "D3 Teknologi Informasi":  {"mn": 558, "mx": 628},
        "D3 Teknik Komputer":      {"mn": 555, "mx": 625},
        "D3 Manajemen":            {"mn": 535, "mx": 605},
        "D3 Akuntansi":            {"mn": 538, "mx": 608},
        "D3 Keperawatan":          {"mn": 512, "mx": 582},
        "D3 Kebidanan":            {"mn": 508, "mx": 578},
        "D3 Farmasi":              {"mn": 548, "mx": 618},
        "D3 Gizi":                 {"mn": 518, "mx": 588},
        "D3 Analis Kesehatan":     {"mn": 515, "mx": 585},
        "_default":                {"mn": 528, "mx": 598},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Negeri Yogyakarta (UNY)": {
        "D3 Teknik Sipil":         {"mn": 498, "mx": 568},
        "D3 Teknik Elektro":       {"mn": 502, "mx": 572},
        "D3 Teknologi Informasi":  {"mn": 510, "mx": 580},
        "D3 Manajemen":            {"mn": 495, "mx": 565},
        "D3 Akuntansi":            {"mn": 495, "mx": 565},
        "D3 Administrasi Bisnis":  {"mn": 488, "mx": 558},
        "D3 Bahasa Inggris":       {"mn": 498, "mx": 568},
        "D3 Pariwisata":           {"mn": 475, "mx": 545},
        "D3 Komunikasi":           {"mn": 480, "mx": 550},
        "_default":                {"mn": 490, "mx": 562},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Semarang (UNNES)": {
        "D3 Teknik Sipil":         {"mn": 488, "mx": 558},
        "D3 Teknik Elektro":       {"mn": 490, "mx": 560},
        "D3 Teknologi Informasi":  {"mn": 498, "mx": 568},
        "D3 Manajemen":            {"mn": 480, "mx": 550},
        "D3 Akuntansi":            {"mn": 482, "mx": 552},
        "D3 Keperawatan":          {"mn": 462, "mx": 532},
        "D3 Farmasi":              {"mn": 478, "mx": 548},
        "_default":                {"mn": 478, "mx": 550},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Malang (UM)": {
        "D3 Teknologi Informasi":  {"mn": 492, "mx": 562},
        "D3 Teknik Komputer":      {"mn": 490, "mx": 560},
        "D3 Manajemen":            {"mn": 478, "mx": 548},
        "D3 Akuntansi":            {"mn": 480, "mx": 550},
        "D3 Administrasi Bisnis":  {"mn": 472, "mx": 542},
        "D3 Keperawatan":          {"mn": 458, "mx": 528},
        "D3 Pariwisata":           {"mn": 455, "mx": 525},
        "D3 Bahasa Inggris":       {"mn": 465, "mx": 535},
        "_default":                {"mn": 472, "mx": 544},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Andalas (Unand)": {
        "D3 Teknologi Informasi":  {"mn": 522, "mx": 592},
        "D3 Teknik Komputer":      {"mn": 518, "mx": 588},
        "D3 Manajemen":            {"mn": 505, "mx": 575},
        "D3 Akuntansi":            {"mn": 508, "mx": 578},
        "D3 Keperawatan":          {"mn": 482, "mx": 552},
        "D3 Kebidanan":            {"mn": 478, "mx": 548},
        "D3 Farmasi":              {"mn": 518, "mx": 588},
        "D3 Gizi":                 {"mn": 488, "mx": 558},
        "D3 Analis Kesehatan":     {"mn": 485, "mx": 555},
        "D3 Pariwisata":           {"mn": 462, "mx": 532},
        "_default":                {"mn": 495, "mx": 565},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sumatera Utara (USU)": {
        "D3 Teknologi Informasi":  {"mn": 515, "mx": 585},
        "D3 Teknik Komputer":      {"mn": 512, "mx": 582},
        "D3 Manajemen":            {"mn": 498, "mx": 568},
        "D3 Akuntansi":            {"mn": 500, "mx": 570},
        "D3 Perbankan & Keuangan": {"mn": 495, "mx": 565},
        "D3 Perpajakan":           {"mn": 495, "mx": 565},
        "D3 Keperawatan":          {"mn": 472, "mx": 542},
        "D3 Kebidanan":            {"mn": 468, "mx": 538},
        "D3 Farmasi":              {"mn": 505, "mx": 575},
        "D3 Analis Kesehatan":     {"mn": 475, "mx": 545},
        "D3 Pariwisata":           {"mn": 452, "mx": 522},
        "D3 Agribisnis":           {"mn": 455, "mx": 525},
        "_default":                {"mn": 485, "mx": 556},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sriwijaya (Unsri)": {
        "D3 Teknik Sipil":         {"mn": 468, "mx": 538},
        "D3 Teknik Mesin":         {"mn": 462, "mx": 532},
        "D3 Teknologi Informasi":  {"mn": 478, "mx": 548},
        "D3 Manajemen":            {"mn": 455, "mx": 525},
        "D3 Akuntansi":            {"mn": 458, "mx": 528},
        "D3 Keperawatan":          {"mn": 435, "mx": 505},
        "D3 Kebidanan":            {"mn": 430, "mx": 500},
        "D3 Farmasi":              {"mn": 465, "mx": 535},
        "D3 Agribisnis":           {"mn": 432, "mx": 502},
        "_default":                {"mn": 450, "mx": 522},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Lampung (Unila)": {
        "D3 Teknik Sipil":         {"mn": 455, "mx": 525},
        "D3 Teknologi Informasi":  {"mn": 462, "mx": 532},
        "D3 Manajemen":            {"mn": 442, "mx": 512},
        "D3 Akuntansi":            {"mn": 445, "mx": 515},
        "D3 Keperawatan":          {"mn": 420, "mx": 490},
        "D3 Kebidanan":            {"mn": 415, "mx": 485},
        "D3 Agribisnis":           {"mn": 418, "mx": 488},
        "_default":                {"mn": 435, "mx": 507},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Jember (Unej)": {
        "D3 Teknik Sipil":         {"mn": 448, "mx": 518},
        "D3 Teknologi Informasi":  {"mn": 455, "mx": 525},
        "D3 Manajemen":            {"mn": 438, "mx": 508},
        "D3 Akuntansi":            {"mn": 440, "mx": 510},
        "D3 Keperawatan":          {"mn": 415, "mx": 485},
        "D3 Kebidanan":            {"mn": 410, "mx": 480},
        "D3 Farmasi":              {"mn": 445, "mx": 515},
        "D3 Agribisnis":           {"mn": 412, "mx": 482},
        "D3 Teknologi Pangan":     {"mn": 418, "mx": 488},
        "D3 Pariwisata":           {"mn": 395, "mx": 465},
        "_default":                {"mn": 428, "mx": 500},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Riau (Unri)": {
        "D3 Teknik Sipil":         {"mn": 440, "mx": 510},
        "D3 Teknologi Informasi":  {"mn": 448, "mx": 518},
        "D3 Manajemen":            {"mn": 428, "mx": 498},
        "D3 Akuntansi":            {"mn": 430, "mx": 500},
        "D3 Keperawatan":          {"mn": 405, "mx": 475},
        "D3 Kebidanan":            {"mn": 400, "mx": 470},
        "D3 Agribisnis":           {"mn": 402, "mx": 472},
        "D3 Pariwisata":           {"mn": 385, "mx": 455},
        "_default":                {"mn": 418, "mx": 490},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
}

def get_ptn_info(kampus, jurusan, jenjang="S1 (Sarjana)"):
    """Ambil info skor PTN berdasarkan kampus, jurusan, dan jenjang"""
    if "D3" in jenjang or jurusan.startswith("D3"):
        ptn = PTN_D3_DATA.get(kampus, {})
        if not ptn:
            # Fallback: gunakan data S1 dan kurangi 80 poin
            ptn_s1 = PTN_JURUSAN_DATA.get(kampus, {})
            base = ptn_s1.get(jurusan, ptn_s1.get("_default", {"mn":500,"mx":570}))
            return {
                "mn": max(380, base["mn"] - 80),
                "mx": max(450, base["mx"] - 80),
                "k": ptn_s1.get("_klaster", 4),
                "lbl": ptn_s1.get("_lbl", "🔸 Klaster 4 — Regional")
            }
        jurusan_data = ptn.get(jurusan, ptn.get("_default", {"mn":500,"mx":570}))
        return {
            "mn": jurusan_data["mn"],
            "mx": jurusan_data["mx"],
            "k": ptn.get("_klaster", 4),
            "lbl": ptn.get("_lbl", "🔸 Klaster 4 — Regional")
        }
    else:
        ptn = PTN_JURUSAN_DATA.get(kampus, {})
        if not ptn:
            return {"mn": 650, "mx": 720, "k": 4, "lbl": "🔸 Klaster 4 — Regional"}
        jurusan_data = ptn.get(jurusan, ptn.get("_default", {"mn": 650, "mx": 720}))
        return {
            "mn": jurusan_data["mn"],
            "mx": jurusan_data["mx"],
            "k": ptn.get("_klaster", 4),
            "lbl": ptn.get("_lbl", "🔸 Klaster 4 — Regional")
        }

# Untuk kompatibilitas fungsi lama
def get_ptn(k):
    ptn = PTN_JURUSAN_DATA.get(k, {})
    default = ptn.get("_default", {"mn": 650, "mx": 720})
    return {
        "k": ptn.get("_klaster", 4),
        "mn": default["mn"],
        "mx": default["mx"],
        "lbl": ptn.get("_lbl", "🔸 Klaster 4")
    }

ALTERNATIF_MAP = {
    "Kedokteran":["Keperawatan","Farmasi","Gizi"],
    "Kedokteran Gigi":["Farmasi","Keperawatan","Kesehatan Masyarakat"],
    "Teknik Informatika":["Statistika","Matematika","Teknik Elektro"],
    "Teknik Sipil":["Teknik Industri","Teknik Mesin","Fisika"],
    "Teknik Mesin":["Teknik Industri","Teknik Sipil","Fisika"],
    "Teknik Elektro":["Teknik Informatika","Fisika","Matematika"],
    "Teknik Industri":["Teknik Sipil","Manajemen","Statistika"],
    "Teknik Kimia":["Kimia","Farmasi","Teknik Industri"],
    "Matematika":["Statistika","Aktuaria","Fisika"],
    "Fisika":["Matematika","Teknik Mesin","Teknik Elektro"],
    "Kimia":["Farmasi","Teknik Kimia","Biologi"],
    "Biologi":["Gizi","Keperawatan","Kimia"],
    "Statistika":["Matematika","Aktuaria","Teknik Informatika"],
    "Aktuaria":["Statistika","Matematika","Ekonomi"],
    "Farmasi":["Kimia","Gizi","Kesehatan Masyarakat"],
    "Gizi":["Keperawatan","Farmasi","Kesehatan Masyarakat"],
    "Keperawatan":["Gizi","Kesehatan Masyarakat","Farmasi"],
    "Kesehatan Masyarakat":["Keperawatan","Gizi","Biologi"],
    "Ilmu Hukum":["Administrasi Publik","Ilmu Politik","Sosiologi"],
    "Ekonomi":["Akuntansi","Manajemen","Bisnis"],
    "Manajemen":["Ekonomi","Bisnis","Akuntansi"],
    "Akuntansi":["Manajemen","Ekonomi","Bisnis"],
    "Bisnis":["Manajemen","Ekonomi","Akuntansi"],
    "Psikologi":["Ilmu Komunikasi","Sosiologi","Administrasi Publik"],
    "Ilmu Komunikasi":["Hubungan Internasional","Administrasi Publik","Psikologi"],
    "Hubungan Internasional":["Ilmu Komunikasi","Ilmu Politik","Sejarah"],
    "Administrasi Publik":["Ilmu Politik","Sosiologi","Ilmu Hukum"],
    "Sastra Inggris":["Pendidikan Bahasa Inggris","Hubungan Internasional","Ilmu Komunikasi"],
    "Pendidikan Bahasa Indonesia":["Sastra Inggris","Ilmu Komunikasi","Sosiologi"],
    "Pendidikan Bahasa Inggris":["Sastra Inggris","Hubungan Internasional","Ilmu Komunikasi"],
    "Sosiologi":["Ilmu Politik","Administrasi Publik","Psikologi"],
    "Ilmu Politik":["Sosiologi","Hubungan Internasional","Administrasi Publik"],
    "Sejarah":["Sosiologi","Geografi","Ilmu Politik"],
    "Geografi":["Sejarah","Sosiologi","Kesehatan Masyarakat"],
}

ALTERNATIF_MAP_D3 = {
    "D3 Teknik Sipil":         ["D3 Teknik Mesin","D3 Teknik Elektro","D3 Teknik Mekatronika"],
    "D3 Teknik Mesin":         ["D3 Teknik Sipil","D3 Teknik Elektro","D3 Teknik Mekatronika"],
    "D3 Teknik Elektro":       ["D3 Teknik Komputer","D3 Teknologi Informasi","D3 Teknik Mekatronika"],
    "D3 Teknik Kimia":         ["D3 Teknologi Pangan","D3 Teknik Sipil","D3 Teknik Mesin"],
    "D3 Teknik Komputer":      ["D3 Teknologi Informasi","D3 Teknik Elektro","D3 Animasi"],
    "D3 Teknologi Informasi":  ["D3 Teknik Komputer","D3 Animasi","D3 Desain Grafis"],
    "D3 Teknik Mekatronika":   ["D3 Teknik Mesin","D3 Teknik Elektro","D3 Teknik Komputer"],
    "D3 Manajemen":            ["D3 Administrasi Bisnis","D3 Manajemen Pemasaran","D3 Akuntansi"],
    "D3 Akuntansi":            ["D3 Perpajakan","D3 Perbankan & Keuangan","D3 Manajemen"],
    "D3 Administrasi Bisnis":  ["D3 Manajemen","D3 Manajemen Pemasaran","D3 Akuntansi"],
    "D3 Perbankan & Keuangan": ["D3 Akuntansi","D3 Perpajakan","D3 Manajemen"],
    "D3 Manajemen Pemasaran":  ["D3 Administrasi Bisnis","D3 Komunikasi","D3 Manajemen"],
    "D3 Perpajakan":           ["D3 Akuntansi","D3 Perbankan & Keuangan","D3 Manajemen"],
    "D3 Keperawatan":          ["D3 Kebidanan","D3 Gizi","D3 Farmasi"],
    "D3 Kebidanan":            ["D3 Keperawatan","D3 Gizi","D3 Analis Kesehatan"],
    "D3 Farmasi":              ["D3 Analis Kesehatan","D3 Keperawatan","D3 Gizi"],
    "D3 Gizi":                 ["D3 Keperawatan","D3 Farmasi","D3 Analis Kesehatan"],
    "D3 Analis Kesehatan":     ["D3 Farmasi","D3 Radiologi","D3 Rekam Medis"],
    "D3 Rekam Medis":          ["D3 Administrasi Bisnis","D3 Analis Kesehatan","D3 Keperawatan"],
    "D3 Fisioterapi":          ["D3 Keperawatan","D3 Gizi","D3 Kebidanan"],
    "D3 Radiologi":            ["D3 Analis Kesehatan","D3 Rekam Medis","D3 Farmasi"],
    "D3 Komunikasi":           ["D3 Hubungan Masyarakat","D3 Manajemen Pemasaran","D3 Pariwisata"],
    "D3 Hubungan Masyarakat":  ["D3 Komunikasi","D3 Manajemen Pemasaran","D3 Administrasi Bisnis"],
    "D3 Desain Grafis":        ["D3 Animasi","D3 Komunikasi","D3 Teknologi Informasi"],
    "D3 Animasi":              ["D3 Desain Grafis","D3 Teknologi Informasi","D3 Komunikasi"],
    "D3 Pariwisata":           ["D3 Perhotelan","D3 Komunikasi","D3 Manajemen"],
    "D3 Perhotelan":           ["D3 Pariwisata","D3 Manajemen","D3 Komunikasi"],
    "D3 Bahasa Inggris":       ["D3 Komunikasi","D3 Hubungan Masyarakat","D3 Pariwisata"],
    "D3 Agribisnis":           ["D3 Teknologi Pangan","D3 Manajemen","D3 Administrasi Bisnis"],
    "D3 Teknologi Pangan":     ["D3 Agribisnis","D3 Analis Kesehatan","D3 Gizi"],
}

LABEL_STRATEGI = ["Intensif & Terstruktur","Penguatan Mental","Optimasi & Review","Pertahankan & Tingkatkan"]
DESC_STRATEGI = {
    "Intensif & Terstruktur":{"icon":"🔴","desc":"Kebiasaan belajar dan kondisi psikologis perlu ditingkatkan secara bersamaan.",
        "tips":["Buat jadwal belajar harian yang ketat","Mulai 2 jam/hari, tingkatkan bertahap","Metode Pomodoro 25+5 menit","Cari kelompok belajar","Konsultasi guru/mentor"]},
    "Penguatan Mental":{"icon":"🟠","desc":"Kebiasaan belajar sudah baik, namun kondisi psikologis perlu diperkuat.",
        "tips":["Mindfulness 10 mnt sebelum belajar","Target kecil harian","Kurangi perbandingan diri","Rutinitas tidur teratur","Tryout rutin untuk adaptasi"]},
    "Optimasi & Review":{"icon":"🟡","desc":"Kebiasaan & mental sudah baik, tingkatkan kualitas review dan evaluasi.",
        "tips":["Review soal yang pernah salah","Analisis pola kesalahan per subtes","Tryout min. 2x/bulan","Catatan ringkasan materi","Fokus efisiensi waktu"]},
    "Pertahankan & Tingkatkan":{"icon":"🟢","desc":"Kebiasaan belajar dan kondisi psikologis sudah sangat baik!",
        "tips":["Pertahankan konsistensi","Tingkatkan target tryout bertahap","Manajemen waktu ujian","Bantu teman belajar","Jaga kesehatan fisik"]},
}


# ══════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    for f in ["lgbm_model_2_.pkl","lgbm_model.pkl","model_skor_utbk_asli.pkl"]:
        if os.path.exists(f):
            try:
                with open(f,"rb") as fp: return pickle.load(fp), f
            except: pass
    return None, None

lgbm_model, lgbm_fname = load_model()


# ══════════════════════════════════════════════════════════
# KALKULASI
# ══════════════════════════════════════════════════════════
def hitung_tw(skor, bobot): return sum(skor[k]*bobot[k] for k in SUBTES)

def hitung_peluang(sw, kampus, jurusan=None, jenjang="S1 (Sarjana)"):
    if jurusan:
        info = get_ptn_info(kampus, jurusan, jenjang)
    else:
        info = get_ptn(kampus)
    mn, mx = info["mn"], info["mx"]
    g = sw - mn
    if sw >= mx:      return "Sangat Aman","#1a8a4a", min(93.,76+(sw-mx)/max(mx,1)*12)
    elif sw >= mn:    return "Aman","#1a8a4a",        62+(sw-mn)/max(mx-mn,1)*13
    elif sw >= mn-70: return "Kompetitif","#d4620a",  32+(70+g)/70*25
    elif sw >= mn-140:return "Berisiko","#c0392b",    16.
    else:             return "Perlu Peningkatan","#c0392b", 8.

def predict_lgbm(model, inp):
    try:
        feat = pd.DataFrame([{
            "Jam_Belajar":inp["jam"],"Hari_Belajar":inp["hari"],
            "Latihan_Soal":inp["latihan"],"Frekuensi_Tryout":inp["tryout"],
            "Review_Soal":inp["review"],"Fokus":inp["fokus"],
            "Percaya_Diri":inp["pede"],
            "Kecemasan_Rev":6-inp["cemas"],"Distraksi_Rev":6-inp["distrak"],
        }])
        if hasattr(model,"feature_name_"):     feat = feat.reindex(columns=model.feature_name_,fill_value=0)
        elif hasattr(model,"feature_names_in_"):feat = feat.reindex(columns=model.feature_names_in_,fill_value=0)
        kode  = int(model.predict(feat)[0])
        label = LABEL_STRATEGI[kode] if kode < len(LABEL_STRATEGI) else LABEL_STRATEGI[-1]
        kpct  = None
        if hasattr(model,"predict_proba"): kpct = float(model.predict_proba(feat)[0][kode])*100
        return {"ok":True,"kode":kode,"strategi":label,"kpct":kpct,"detail":DESC_STRATEGI.get(label,{})}
    except Exception as e:
        return {"ok":False,"err":str(e)}

def compute(d):
    skor  = {k: d[k] for k in SUBTES}
    bobot = get_bobot(d["jurusan"])
    sw    = hitung_tw(skor, bobot)
    rata  = float(np.mean([skor[k] for k in SUBTES]))
    jenjang = d.get("jenjang", "S1 (Sarjana)")
    pl,pc,ppct = hitung_peluang(sw, d["kampus"], d["jurusan"], jenjang)
    info  = get_ptn_info(d["kampus"], d["jurusan"], jenjang)
    gap   = sw - info["mn"]

    psiko = (d["fokus"]*1.5 + d["pede"]*1.5 + (6-d["cemas"]) + (6-d["distrak"])) / 20 * 100
    konsist = min(100, (d["jam"]*2 + d["hari"]*2.2 + d["latihan"]*1.8 + d["tryout"]*1.5 + d["review"]*1.5)*2)
    pos = (d["fokus"]*1.5 + d["pede"]*1.5)*10
    neg = (d["cemas"]*1.2 + d["distrak"]*1.2)*8
    stab = max(0, min(100, pos - neg + 50))
    rgb  = stab*0.6 + konsist*0.4
    if rgb >= 75: risk=("Rendah","✅","Kemungkinan perform sesuai/di atas kemampuan")
    elif rgb >= 60: risk=("Sedang","⚠️","Ada potensi fluktuasi, jaga konsistensi")
    else: risk=("Tinggi","🔴","Risiko perform di bawah kemampuan, perlu perbaikan")

    lgbm_r = predict_lgbm(lgbm_model, d) if lgbm_model else None
    aman   = pl in ("Sangat Aman","Aman")
    jenjang = d.get("jenjang","S1 (Sarjana)")
    if "D3" in jenjang or d["jurusan"].startswith("D3"):
        alt = ALTERNATIF_MAP_D3.get(d["jurusan"],[])
    else:
        alt = ALTERNATIF_MAP.get(d["jurusan"],[])

    return {**d,"skor":skor,"bobot":bobot,"sw":sw,"rata":rata,
            "pl":pl,"pc":pc,"ppct":ppct,"info":info,"gap":gap,
            "psiko":psiko,"konsist":konsist,"stab":stab,"risk":risk,
            "lgbm_r":lgbm_r,"aman":aman,"jenjang":jenjang,
            "alternatif":alt}

# ══════════════════════════════════════════════════════════
# RENCANA BELAJAR MINGGUAN
# ══════════════════════════════════════════════════════════
def buat_rencana_mingguan(r, n_minggu=8):
    skor  = r["skor"]
    bobot = r["bobot"]
    gap   = r["gap"]
    sw    = r["sw"]
    mn    = r["info"]["mn"]
    mx    = r["info"]["mx"]

    ranked = sorted(SUBTES, key=lambda k: skor[k])
    terlemah3 = ranked[:3]
    sedang2   = ranked[3:5]
    terkuat2  = ranked[5:]

    if gap < 0:
        target_per_minggu = abs(gap) / n_minggu + 10
    else:
        target_per_minggu = (mx - sw) / n_minggu + 5 if sw < mx else 5

    rencana = []
    for w in range(1, n_minggu+1):
        fase = "Fondasi" if w <= 2 else "Intensif" if w <= 5 else "Pemantapan" if w <= 7 else "Final"
        target_sw = min(mx+20, sw + target_per_minggu * w)

        if fase == "Fondasi":
            tasks = [
                f"Review konsep dasar {SUBTES_FULL[terlemah3[0]]} (skor {skor[terlemah3[0]]} → target +30)",
                f"50 soal latihan {SUBTES_FULL[terlemah3[1]]} dengan timer",
                f"Pelajari pola soal {SUBTES_FULL[terlemah3[2]]}",
                "Buat catatan kesalahan (error log)",
                "Tryout mini: 30 soal campuran + analisis",
            ]
            jam = "2–3 jam/hari"
        elif fase == "Intensif":
            subtes_minggu = terlemah3 + sedang2
            subtes_ini = subtes_minggu[(w-3) % len(subtes_minggu)] if subtes_minggu else "PU"
            tasks = [
                f"100 soal latihan {SUBTES_FULL[subtes_ini]} + timer ketat",
                "Review error log minggu sebelumnya",
                f"Mini tryout {SUBTES_FULL[sedang2[0] if sedang2 else 'PU']} (50 soal, 45 mnt)",
                "Simulasi 1 paket soal lengkap (90 mnt)",
                "Analisis & rekap kesalahan pola berulang",
            ]
            jam = "3–4 jam/hari"
        elif fase == "Pemantapan":
            tasks = [
                "Full tryout 1 paket lengkap + evaluasi",
                f"Review intensif {SUBTES_FULL[terlemah3[0]]} (subtes fokus utama)",
                "Latihan manajemen waktu (simulasi kondisi ujian)",
                "Review catatan penting semua subtes",
                "Rest day: hanya review ringan 1 jam",
            ]
            jam = "3–4 jam/hari (1 hari libur)"
        else:
            tasks = [
                "Full tryout final + review mendalam",
                "Revisi soal-soal sulit yang pernah salah",
                "Persiapan mental: teknik relaksasi & tidur cukup",
                "Cek strategi manajemen waktu ujian",
                "Istirahat — jaga kondisi fisik & mental",
            ]
            jam = "2 jam/hari + istirahat cukup"

        rencana.append({
            "minggu": w, "fase": fase,
            "target_skor": f"{target_sw:.0f}",
            "jam": jam, "fokus": SUBTES_FULL.get(terlemah3[0],"TPS") if terlemah3 else "TPS",
            "tasks": tasks,
        })
    return rencana


# ══════════════════════════════════════════════════════════
# CHART THEME — Light
# ══════════════════════════════════════════════════════════
CTH = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#3a4a65'),
    margin=dict(l=10, r=10, t=45, b=10)
)

def ch_radar(skor, bobot, jurusan, key=None):
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal, theta=cats, fill='toself', name='Profil Ideal Jurusan',
        fillcolor='rgba(200,137,10,.08)', line=dict(color='#c8890a', dash='dot', width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,  theta=cats, fill='toself', name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)', line=dict(color='#3b6cb7', width=2.5)))
    fig.update_layout(**CTH, polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS], gridcolor='#dde3ec', linecolor='#dde3ec',
                        tickfont=dict(size=9, color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec', linecolor='#dde3ec', tickfont=dict(size=9.5, color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)', orientation='h', x=.5, xanchor='center', y=-.15,
                    font=dict(color='#3a4a65')),
        title=dict(text=f"Radar TPS — {jurusan}", font=dict(size=13, color='#1a2540')), height=400)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("radar"))

def ch_bar_subtes(skor, bobot, info, key=None):
    lbl  = [SUBTES_FULL[k] for k in SUBTES]
    vals = [skor[k] for k in SUBTES]
    tgt  = [min(SKOR_MAX_TPS,(info["mn"]+info["mx"])/2*bobot[k]*7) for k in SUBTES]
    clrs = [SUBTES_CLR[k] for k in SUBTES]
    fig  = go.Figure()
    fig.add_trace(go.Bar(name='Skor Kamu', x=lbl, y=vals, marker_color=clrs, marker_line_width=0,
        text=[str(v) for v in vals], textposition='outside', textfont=dict(size=10, color='#1a2540')))
    fig.add_trace(go.Scatter(name='Target Kampus', x=lbl, y=tgt, mode='markers+lines',
        marker=dict(symbol='diamond', size=9, color='#c8890a'),
        line=dict(color='#c8890a', dash='dot', width=1.5)))
    fig.update_layout(**CTH, barmode='group',
        xaxis=dict(tickfont=dict(size=9, color='#3a4a65'), gridcolor='#dde3ec'),
        yaxis=dict(range=[0, SKOR_MAX_TPS*1.07], gridcolor='#eef1f5', tickfont=dict(size=9, color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)', orientation='h', x=.5, xanchor='center', y=-.2, font=dict(color='#3a4a65')),
        title=dict(text="Skor Per Subtes vs Target Kampus", font=dict(size=13, color='#1a2540')), height=370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("bar"))

def ch_pipeline(skor, bobot, info, jurusan, key=None):
    lbl    = [SUBTES_FULL[k] for k in SUBTES]
    aktual = [skor[k]*bobot[k] for k in SUBTES]
    ideal  = [info["mn"]*bobot[k] for k in SUBTES]
    clrs   = [SUBTES_CLR[k] for k in SUBTES]
    fig    = go.Figure()
    fig.add_trace(go.Bar(name='Target Min Kampus', y=lbl, x=ideal, orientation='h',
        marker_color=['rgba(200,137,10,.12)']*7,
        marker_line_color='#c8890a', marker_line_width=1.5))
    fig.add_trace(go.Bar(name='Kontribusi Aktual', y=lbl, x=aktual, orientation='h',
        marker_color=clrs, text=[f"{v:.1f}" for v in aktual],
        textposition='inside', textfont=dict(size=10, color='#fff')))
    fig.update_layout(**CTH, barmode='overlay',
        xaxis=dict(title="Kontribusi ke Skor Total", gridcolor='#eef1f5',
                   title_font=dict(color='#6a7a95'), tickfont=dict(size=9, color='#3a4a65')),
        yaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=10, color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)', orientation='h', x=.5, xanchor='center', y=-.13, font=dict(color='#3a4a65')),
        title=dict(text=f"Pipeline Kontribusi Subtes — {jurusan}", font=dict(size=13, color='#1a2540')), height=380)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("pipe"))

def ch_bobot(jurusan, key=None):
    bobot = get_bobot(jurusan)
    lbl   = [SUBTES_FULL[k] for k in SUBTES]
    vals  = [bobot[k]*100 for k in SUBTES]
    clrs  = [SUBTES_CLR[k] for k in SUBTES]
    fig   = go.Figure(go.Bar(x=lbl, y=vals, marker_color=clrs, marker_line_width=0,
        text=[f"{v:.0f}%" for v in vals], textposition='outside', textfont=dict(size=10, color='#1a2540')))
    fig.update_layout(**CTH,
        xaxis=dict(tickfont=dict(size=9, color='#3a4a65'), gridcolor='#dde3ec'),
        yaxis=dict(range=[0,55], ticksuffix="%", gridcolor='#eef1f5',
                   title="Bobot (%)", title_font=dict(color='#6a7a95'), tickfont=dict(size=9, color='#3a4a65')),
        title=dict(text=f"Distribusi Bobot Subtes — {jurusan}", font=dict(size=13, color='#1a2540')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("bobot"))

def ch_klaster(sw, key=None):
    kl = [("Klaster 1\nTop Tier",880,970,"#c0392b"),
          ("Klaster 2\nMng Atas",730,870,"#d4620a"),
          ("Klaster 3\nMenengah",600,730,"#1a8a4a"),
          ("Klaster 4\nRegional",555,660,"#3b6cb7")]
    fig = go.Figure()
    for lbl,mn,mx,clr in kl:
        r_,g_,b_ = int(clr[1:3],16),int(clr[3:5],16),int(clr[5:7],16)
        fig.add_trace(go.Bar(x=[lbl], y=[mx-mn], base=[mn], showlegend=False,
            marker_color=f"rgba({r_},{g_},{b_},.12)", marker_line_color=clr, marker_line_width=2,
            text=[f"{mn}–{mx}"], textposition='inside', textfont=dict(size=10,color=clr)))
    fig.add_hline(y=sw, line_dash="dash", line_color="#7048c8", line_width=2.5,
        annotation_text=f"  Skor kamu: {sw:.0f}", annotation_font_color="#7048c8", annotation_font_size=11)
    fig.update_layout(**CTH, barmode='overlay',
        xaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=10,color='#3a4a65')),
        yaxis=dict(range=[450,SKOR_MAX_TPS], gridcolor='#eef1f5',
                   title="Rentang Skor Aman", title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        title=dict(text="Posisi Skor vs Klaster PTN", font=dict(size=13,color='#1a2540')), height=370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("klaster"))

def ch_ptn(sw, klaster_no, jurusan, jenjang="S1 (Sarjana)", key=None):
    if "D3" in jenjang:
        ptn_k = {k:v for k,v in PTN_D3_DATA.items() if v.get("_klaster")==klaster_no}
    else:
        ptn_k = {k:v for k,v in PTN_JURUSAN_DATA.items() if v.get("_klaster")==klaster_no}
    fig = go.Figure()
    for nm,d in ptn_k.items():
        short = nm.split("(")[0].strip()[:24]
        jd = d.get(jurusan, d.get("_default", {"mn":500,"mx":600}))
        mn_j, mx_j = jd["mn"], jd["mx"]
        fig.add_trace(go.Bar(x=[short], y=[mx_j-mn_j], base=[mn_j], showlegend=False,
            marker_color='rgba(59,108,183,.12)', marker_line_color='#3b6cb7', marker_line_width=1.5,
            text=[f"{mn_j}–{mx_j}"], textposition='inside', textfont=dict(size=9,color='#1a2540')))
    fig.add_hline(y=sw, line_dash="dash", line_color="#c8890a", line_width=2,
        annotation_text=f"  Skor kamu: {sw:.0f}", annotation_font_color="#c8890a", annotation_font_size=11)
    y_min = 350 if "D3" in jenjang else 450
    jenjang_lbl2 = "D3" if "D3" in jenjang else "S1"
    fig.update_layout(**CTH, barmode='overlay',
        yaxis=dict(range=[y_min,SKOR_MAX_TPS], gridcolor='#eef1f5',
                   title="Rentang Skor", title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        xaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=9,color='#3a4a65')),
        title=dict(text=f"PTN Klaster {klaster_no} ({jenjang_lbl2}) — {jurusan}", font=dict(size=13,color='#1a2540')), height=320)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("ptn"))

def ch_psiko(psiko, konsist, stab, key=None):
    cats = ["Kesiapan Mental","Konsistensi Belajar","Stabilitas Mental"]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=cats, y=[psiko,konsist,stab],
        marker_color=["#3b6cb7","#1a8a4a","#7048c8"], marker_line_width=0,
        text=[f"{v:.0f}%" for v in [psiko,konsist,stab]],
        textposition='outside', textfont=dict(size=11,color='#1a2540')))
    fig.add_hline(y=80, line_dash="dot", line_color="#c8890a", line_width=1.5,
        annotation_text="  Target 80%", annotation_font_color="#c8890a", annotation_font_size=10)
    fig.update_layout(**CTH,
        yaxis=dict(range=[0,115], ticksuffix="%", gridcolor='#eef1f5', tickfont=dict(size=9,color='#3a4a65')),
        xaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=10,color='#3a4a65')),
        title=dict(text="Indikator Psikologis & Konsistensi", font=dict(size=13,color='#1a2540')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("psiko"))

def ch_progress(r, key=None):
    sw   = r["sw"]; mn = r["info"]["mn"]; mx = r["info"]["mx"]
    gap  = abs(r["gap"]) if r["gap"] < 0 else 0
    ppm  = gap/8 + 8
    weeks = list(range(0, 9))
    preds = [min(mx+30, sw + ppm*w) for w in weeks]
    fig = go.Figure()
    fig.add_hrect(y0=mn, y1=mx, fillcolor="rgba(26,138,74,.07)", layer="below",
                  line_width=0, annotation_text="  Zona Aman", annotation_position="top right",
                  annotation_font=dict(color="#1a8a4a", size=10))
    fig.add_trace(go.Scatter(x=weeks, y=preds, mode='lines+markers+text',
        line=dict(color='#3b6cb7', width=2.5),
        marker=dict(size=8, color='#3b6cb7', line=dict(color='#ffffff', width=1.5)),
        text=[f"{v:.0f}" for v in preds], textposition='top center',
        textfont=dict(size=9,color='#3a4a65'), name='Proyeksi Skor'))
    fig.add_trace(go.Scatter(x=[0], y=[sw], mode='markers',
        marker=dict(size=12, color='#c8890a', symbol='star'),
        name=f'Skor Sekarang ({sw:.0f})'))
    fig.add_hline(y=mn, line_dash="dash", line_color="#d4620a", line_width=1.5,
        annotation_text=f"  Minimum ({mn})", annotation_font_color="#d4620a", annotation_font_size=10)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#3a4a65'),
        margin=dict(l=10, r=10, t=45, b=30),
        xaxis=dict(title="Minggu ke-", tickvals=weeks, gridcolor='#eef1f5',
                   title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(range=[max(400,sw-100), min(1000,mx+60)], gridcolor='#eef1f5',
                   title="Proyeksi Skor", title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)', font=dict(color='#3a4a65')),
        title=dict(text="Proyeksi Skor 8 Minggu ke Depan", font=dict(size=13,color='#1a2540')),
        height=340
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("prog"))


# ══════════════════════════════════════════════════════════
# PDF EXPORT
# ══════════════════════════════════════════════════════════
def generate_pdf(r):
    now  = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    nama = r.get("nama","—")
    jenjang_lbl = r.get("jenjang","S1 (Sarjana)")
    bobot_rows = "".join(
        f"<tr><td>{SUBTES_FULL[k]}</td><td>{int(r['bobot'][k]*100)}%</td>"
        f"<td>{r['skor'][k]}</td><td>{r['skor'][k]*r['bobot'][k]:.1f}</td></tr>"
        for k in SUBTES)
    alt_list = ", ".join(r["alternatif"]) if r["alternatif"] else "—"
    lgbm_txt = ""
    if r.get("lgbm_r") and r["lgbm_r"].get("ok"):
        h = r["lgbm_r"]
        kp = f"{h['kpct']:.1f}%" if h.get("kpct") else "—"
        lgbm_txt = f"<p><strong>Rekomendasi Strategi SKORIA AI:</strong> {h['strategi']} (kepercayaan: {kp})</p>"
    rencana = buat_rencana_mingguan(r, 8)
    minggu_html = "".join(f"""
    <div style="margin-bottom:12px;padding:10px 14px;background:#f8fafc;border-radius:8px;border-left:3px solid #3b6cb7">
      <div style="font-size:9pt;color:#3b6cb7;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px">
        Minggu {m['minggu']} — {m['fase']}
      </div>
      <div style="font-size:9.5pt;font-weight:600;color:#1e293b;margin-bottom:4px">
        Target skor: {m['target_skor']} | {m['jam']}
      </div>
      <ul style="margin:0;padding-left:1.1rem;font-size:9pt;color:#374151;line-height:1.7">
        {"".join(f"<li>{t}</li>" for t in m['tasks'])}
      </ul>
    </div>""" for m in rencana)
    gc = "green" if r["gap"]>=0 else "red"
    pc = "green" if r["ppct"]>=65 else "orange" if r["ppct"]>=35 else "red"
    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8">
<title>Laporan SKORIA — {nama}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Sora:wght@700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;font-size:11pt;color:#1e293b;background:#fff;padding:1.2cm 1.8cm}}
h1{{font-family:'Sora',sans-serif;font-size:18pt;font-weight:800;color:#0f172a}}
h2{{font-family:'Sora',sans-serif;font-size:11pt;font-weight:700;color:#0f172a;margin:16px 0 7px;
    border-bottom:2px solid #3b6cb7;padding-bottom:3px}}
p{{font-size:10pt;line-height:1.65;color:#374151;margin-bottom:5px}}
.hdr{{background:linear-gradient(135deg,#2a4a8c,#3b6cb7);color:#fff;padding:1.1cm 1.4cm;
      border-radius:12px;margin-bottom:.9cm}}
.brand{{font-family:'Sora',sans-serif;font-size:12pt;font-weight:800;color:#ffd166;margin-bottom:3px}}
.hdr .sub{{color:rgba(255,255,255,.75);font-size:9pt;margin-top:3px}}
.kpi-row{{display:flex;gap:10px;margin-bottom:10px}}
.kpi{{flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center}}
.kpi .val{{font-size:18pt;font-weight:800;font-family:'Sora',sans-serif}}
.kpi .lbl{{font-size:7.5pt;color:#64748b;text-transform:uppercase;letter-spacing:.05em}}
.green{{color:#16a34a}}.orange{{color:#ca8a04}}.red{{color:#dc2626}}.blue{{color:#1d4ed8}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:9px}}
th{{background:#eef3fc;text-align:left;padding:5px 9px;font-weight:600;border:1px solid #dde3ec;color:#1e293b}}
td{{padding:5px 9px;border:1px solid #dde3ec;color:#374151}}
tr:nth-child(even) td{{background:#f7f9fc}}
.footer{{margin-top:.8cm;font-size:8pt;color:#94a3b8;text-align:center;border-top:1px solid #e2e8f0;padding-top:7px}}
@media print{{body{{padding:.8cm 1cm}}.no-print{{display:none}}}}
</style></head><body>
<div class="hdr">
  <div class="brand">🎯 SKORIA</div>
  <h1>AI UTBK Readiness Report</h1>
  <div class="sub">Laporan Kesiapan UTBK · {now}</div>
</div>
<h2>👤 Profil Siswa</h2>
<table><tr><th>Nama</th><td>{nama}</td><th>Jenjang</th><td>{jenjang_lbl}</td></tr>
<tr><th>Jurusan / Prodi</th><td>{r['jurusan']}</td><th>Kampus Target</th><td>{r['kampus']}</td></tr>
<tr><th>Klaster</th><td colspan="3">{r['info']['lbl']}</td></tr></table>
<h2>📊 Ringkasan Hasil (Skor skala 1000)</h2>
<div class="kpi-row">
<div class="kpi"><div class="lbl">Skor Tertimbang</div><div class="val {gc}">{r['sw']:.0f}</div><div class="lbl">dari 1000</div></div>
<div class="kpi"><div class="lbl">Rata-rata Subtes</div><div class="val blue">{r['rata']:.0f}</div></div>
<div class="kpi"><div class="lbl">Peluang Lolos</div><div class="val {pc}">{r['ppct']:.0f}%</div><div class="lbl">{r['pl']}</div></div>
<div class="kpi"><div class="lbl">Gap vs Minimum</div><div class="val {gc}">{r['gap']:+.0f}</div><div class="lbl">Min {r['info']['mn']}</div></div>
</div>
{lgbm_txt}
<h2>📋 Bobot & Skor Subtes</h2>
<table><tr><th>Subtes</th><th>Bobot ({r['jurusan']})</th><th>Skor (maks 1000)</th><th>Kontribusi</th></tr>
{bobot_rows}
<tr style="background:#eef3fc"><th colspan="2">Total Skor Tertimbang</th><th colspan="2"><strong>{r['sw']:.1f}</strong></th></tr></table>
<h2>🧠 Indikator Psikologis & Kebiasaan</h2>
<table>
<tr><th>Fokus</th><td>{r['fokus']}/5</td><th>Percaya Diri</th><td>{r['pede']}/5</td></tr>
<tr><th>Kecemasan</th><td>{r['cemas']}/5</td><th>Distraksi</th><td>{r['distrak']}/5</td></tr>
<tr><th>Kesiapan Mental</th><td>{r['psiko']:.0f}/100</td><th>Konsistensi</th><td>{r['konsist']:.0f}/100</td></tr>
<tr><th>Stabilitas Mental</th><td>{r['stab']:.0f}/100</td><th>Risiko Underperform</th><td>{r['risk'][0]} {r['risk'][1]}</td></tr></table>
<h2>🎓 Jurusan Alternatif</h2><p>{alt_list}</p>
<h2>📅 Rencana Belajar Mingguan (8 Minggu)</h2>
{minggu_html}
<div class="footer">🎯 SKORIA — AI UTBK Intelligence · Data SNPMB/BPPP Kemdikbud & media pendidikan 2025/2026 · Skor skala 200–1000</div>
<div class="no-print" style="margin-top:16px;text-align:center">
<button onclick="window.print()" style="padding:8px 20px;background:#3b6cb7;border:none;border-radius:8px;
  font-weight:700;cursor:pointer;font-size:11pt;font-family:'Sora',sans-serif;color:#ffffff">
  🖨️ Print / Save as PDF</button></div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════════
def render_nav():
    p = st.session_state.page
    s1 = "done" if p in ["survey","result"] else "active" if p=="home" else ""
    s2 = "done" if p=="result" else "active" if p=="survey" else ""
    s3 = "active" if p=="result" else ""
    st.markdown(f"""<div class="topbar">
      <div class="topbar-brand">🎯 SKORIA <span class="topbar-tag">AI UTBK Intelligence</span></div>
      <div class="step-pill {s1}">{'✓' if p in ['survey','result'] else '①'} Beranda</div>
      <div class="step-pill {s2}">{'✓' if p=='result' else '②'} Input Data</div>
      <div class="step-pill {s3}">③ Hasil Analisis</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def prog_bar(label, val, color):
    st.markdown(f"""<div class="prog-wrap">
      <div class="prog-lbl"><span>{label}</span>
        <span style="color:{color};font-weight:700">{val:.0f}/100</span></div>
      <div class="prog-bg">
        <div class="prog-fill" style="width:{val:.0f}%;background:{color}"></div>
      </div>
    </div>""", unsafe_allow_html=True)

def bobot_chips(jurusan):
    b = get_bobot(jurusan)
    chips = "".join(
        f'<div class="bobot-chip"><span class="sk">{k}</span><span class="bv">{int(b[k]*100)}%</span></div>'
        for k in SUBTES)
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:3px;margin:.4rem 0">{chips}</div>',
                unsafe_allow_html=True)

def step_bar(cur):
    steps = ["👤 Profil, Jenjang & Target","📊 Skor TPS","🧠 Psikologis","📚 Kebiasaan Belajar"]
    html  = '<div class="step-row">'
    for i,s in enumerate(steps,1):
        cls = "active" if i==cur else "done" if i<cur else ""
        mk  = "✓" if i<cur else str(i)
        html += f'<div class="step-item {cls}"><span class="step-num">{mk}</span>{s}</div>'
    st.markdown(html+"</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════
def page_home():
    st.markdown("""<div class="hero">
      <h1>SKORIA — Analisis Kesiapan<br><span>UTBK</span> Berbasis AI</h1>
      <p>Platform kecerdasan buatan untuk memahami peluang, gap skor, dan strategi belajar<br>
         yang dipersonalisasi. Data skor berbasis UTBK 2023/2024 per jurusan dan PTN.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    feats = [
        ("📡","Radar Chart TPS","Visualisasi 7 subtes vs profil ideal jurusan"),
        ("🎓","S1 & D3 Support","Data skor aman per jenjang, jurusan, & PTN berbasis SNPMB 2025/2026"),
        ("📅","Rencana Mingguan","Jadwal belajar 8 minggu terstruktur"),
        ("📄","Export PDF","Laporan lengkap dengan rencana belajar"),
    ]
    for col,(ico,ttl,desc) in zip([c1,c2,c3,c4],feats):
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;padding:1.3rem">
              <div style="font-size:1.8rem;margin-bottom:.4rem">{ico}</div>
              <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:.88rem;
                          margin-bottom:.3rem;color:#1a2540">{ttl}</div>
              <div style="font-size:.77rem;color:#6a7a95;line-height:1.55">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">🤖 Tentang SKORIA</div>', unsafe_allow_html=True)
    st.markdown("""<div class="al al-i">
      <h4>SKORIA — Score Intelligence for UTBK</h4>
      Platform SKORIA mengintegrasikan <strong>Model LightGBM</strong> dengan analisis holistik:
      <ul>
        <li>🎓 <strong>Support jenjang S1 (Sarjana) & D3 (Diploma Tiga)</strong> — 30+ prodi D3 dari 18 PTN</li>
        <li>📊 Skor aman per jurusan, jenjang, & PTN berbasis <strong>SNPMB/BPPP Kemdikbud & media pendidikan 2025/2026</strong></li>
        <li>🧠 Evaluasi psikologis: fokus, percaya diri, kecemasan, distraksi</li>
        <li>📡 Radar Chart TPS, Bar Chart, Pipeline Kontribusi, Klaster PTN</li>
        <li>📅 Rencana belajar mingguan 8 minggu dengan target terukur</li>
        <li>📄 Export PDF lengkap termasuk rencana mingguan</li>
        <li>🎯 Gap analysis berbasis klaster PTN — skor maksimal 1000</li>
      </ul>
    </div>""", unsafe_allow_html=True)

    if lgbm_model:
        st.markdown(f'<div class="al al-s"><h4>✅ Model AI Aktif</h4>File: <code>{lgbm_fname}</code> — Prediksi strategi belajar siap digunakan.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="al al-w"><h4>⚠️ Model AI Tidak Ditemukan</h4>Letakkan <code>lgbm_model_2_.pkl</code> di folder yang sama. Kalkulasi manual tetap berjalan.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀  Mulai Analisis UTBK", type="primary"):
        st.session_state.page="survey"; st.session_state.step=1; st.rerun()


# ══════════════════════════════════════════════════════════
# PAGE: SURVEY (4 STEPS)
# ══════════════════════════════════════════════════════════
def step1():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Profil & Target</h3>', unsafe_allow_html=True)
    d = st.session_state.data
    nama    = st.text_input("Nama Lengkap", value=d.get("nama",""), placeholder="Nama kamu...")

    # Jenjang selector
    prev_jenjang = d.get("jenjang", DAFTAR_JENJANG[0])
    jenjang = st.radio(
        "🎓 Jenjang yang Dituju",
        DAFTAR_JENJANG,
        index=DAFTAR_JENJANG.index(prev_jenjang),
        horizontal=True,
        help="S1 = Sarjana (4 tahun) | D3 = Diploma Tiga (3 tahun, program vokasi)"
    )

    # Jurusan dinamis berdasarkan jenjang
    daftar_j = get_daftar_jurusan(jenjang)
    prev_jurusan = d.get("jurusan", daftar_j[0])
    if prev_jurusan not in daftar_j:
        prev_jurusan = daftar_j[0]
    jurusan = st.selectbox(
        "🏫 Target Jurusan / Program Studi",
        daftar_j,
        index=daftar_j.index(prev_jurusan),
        help="Pilih program studi yang kamu tuju"
    )

    kampus  = st.selectbox("🏛️ Target Kampus (PTN)", DAFTAR_PTN,
                           index=DAFTAR_PTN.index(d.get("kampus",DAFTAR_PTN[0])))

    # Info jenjang
    if "D3" in jenjang:
        st.markdown("""<div class="al al-p" style="margin-top:.5rem;padding:.7rem 1rem">
          <h4>📋 Tentang Jenjang D3 (Diploma Tiga)</h4>
          Program vokasi 3 tahun yang menekankan keterampilan praktis & profesional.
          Skor aman D3 umumnya <strong>35–80 poin lebih rendah</strong> dari S1 sejenis,
          namun persaingan tetap ada karena kuota lebih kecil. Data berbasis SNPMB 2025/2026.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="al al-i" style="margin-top:.5rem;padding:.7rem 1rem">
          <h4>📋 Tentang Jenjang S1 (Sarjana)</h4>
          Program akademik 4 tahun. Data skor aman berbasis SNPMB/BPPP Kemdikbud & media pendidikan 2025/2026.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    bobot_chips(jurusan)
    info = get_ptn_info(kampus, jurusan, jenjang)
    jenjang_lbl = "D3" if "D3" in jenjang else "S1"
    st.markdown(f"""<div class="al al-i" style="margin-top:.7rem">
      <h4>{info['lbl']} — {kampus}</h4>
      Skor aman <strong>{jenjang_lbl} {jurusan}</strong>:
      <strong>{info['mn']} – {info['mx']}</strong>
      <br><small style="color:#6a7a95">Berdasarkan data SNPMB/BPPP Kemdikbud & referensi media pendidikan 2025/2026</small>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Lanjut → Skor TPS ▶", type="primary"):
        if not nama.strip(): st.error("Nama harus diisi!"); return
        st.session_state.data.update({"nama":nama,"jenjang":jenjang,"jurusan":jurusan,"kampus":kampus})
        st.session_state.step=2; st.rerun()

def step2():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Skor TPS (Tes Potensi Skolastik)</h3>', unsafe_allow_html=True)
    st.caption(f"Masukkan skor tryout terbaru kamu. Skala: {SKOR_MIN_TPS} – {SKOR_MAX_TPS}")
    d = st.session_state.data
    skor = {}

    # Input angka langsung (bukan slider)
    pairs = [("PU","PPU"),("PBM","PK"),("LBI","LBE"),("PM",None)]
    for pair in pairs:
        cols = st.columns(2)
        for col, k in zip(cols, pair):
            if k is None: continue
            with col:
                val = d.get(k, 550)
                skor[k] = st.number_input(
                    f"{SUBTES_FULL[k]} ({k})",
                    min_value=SKOR_MIN_TPS, max_value=SKOR_MAX_TPS,
                    value=int(val), step=5,
                    key=f"n_{k}",
                    help=f"Masukkan skor {SUBTES_FULL[k]} dari tryout terakhir (200–1000)"
                )

    jurusan = d.get("jurusan", DAFTAR_JURUSAN[0])
    bobot   = get_bobot(jurusan)

    # Live radar preview
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES]+[min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal',
        fillcolor='rgba(200,137,10,.08)',line=dict(color='#c8890a',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)',line=dict(color='#3b6cb7',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9,color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9.5,color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#3a4a65')),
        title=dict(text=f"Preview Radar — {jurusan}",font=dict(size=13,color='#1a2540')),height=380)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key="survey_radar")
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=1; st.rerun()
    with cb:
        if st.button("Lanjut → Psikologis ▶", type="primary"):
            st.session_state.data.update(skor); st.session_state.step=3; st.rerun()

def step3():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>🧠 Kondisi Psikologis</h3>', unsafe_allow_html=True)
    st.caption("1 = Sangat Rendah · 5 = Sangat Tinggi")
    d = st.session_state.data
    ca,cb = st.columns(2)
    with ca:
        fokus = st.slider("🎯 Kemampuan Fokus Belajar",1,5,d.get("fokus",3))
        pede  = st.slider("💪 Percaya Diri",1,5,d.get("pede",3))
    with cb:
        cemas  = st.slider("😰 Tingkat Kecemasan (1=tenang, 5=sangat cemas)",1,5,d.get("cemas",3))
        distrak= st.slider("📱 Mudah Terdistraksi (1=fokus, 5=sangat mudah)",1,5,d.get("distrak",3))
    psiko = (fokus*1.5+pede*1.5+(6-cemas)+(6-distrak))/20*100
    pc = "#1a8a4a" if psiko>=65 else "#c8890a" if psiko>=45 else "#c0392b"
    st.markdown(f"""<div class="card" style="text-align:center;margin-top:.8rem">
      <div class="kpi-lbl">Indeks Kesiapan Mental</div>
      <div class="kpi-val" style="color:{pc}">{psiko:.0f}<span style="font-size:1rem;color:#6a7a95">/100</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=2; st.rerun()
    with cb:
        if st.button("Lanjut → Kebiasaan Belajar ▶", type="primary"):
            st.session_state.data.update({"fokus":fokus,"pede":pede,"cemas":cemas,"distrak":distrak})
            st.session_state.step=4; st.rerun()

def step4():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📚 Kebiasaan Belajar</h3>', unsafe_allow_html=True)
    d = st.session_state.data
    mj = {"< 1 jam":1,"1–2 jam":2,"3–4 jam":3,"5–6 jam":4,"> 6 jam":5}
    mh = {"≤ 1 hari":1,"2 hari":2,"3 hari":3,"4–5 hari":4,"≥ 6 hari":5}
    ca,cb = st.columns(2)
    with ca:
        js = st.selectbox("⏰ Jam belajar/hari",list(mj.keys()),index=d.get("jam",3)-1)
        hs = st.selectbox("📅 Hari belajar/minggu",list(mh.keys()),index=d.get("hari",3)-1)
        lat= st.slider("✏️ Intensitas latihan soal/minggu (1–5)",1,5,d.get("latihan",3))
    with cb:
        try_= st.slider("📝 Frekuensi tryout/bulan (1–5)",1,5,d.get("tryout",2))
        rev = st.slider("🔄 Intensitas review soal salah/minggu (1–5)",1,5,d.get("review",3))
    jb = mj[js]; hb = mh[hs]
    konsist = min(100,(jb*2+hb*2.2+lat*1.8+try_*1.5+rev*1.5)*2)
    kc = "#1a8a4a" if konsist>=65 else "#c8890a" if konsist>=45 else "#c0392b"
    st.markdown(f"""<div class="card" style="text-align:center;margin-top:.8rem">
      <div class="kpi-lbl">Indeks Konsistensi Belajar</div>
      <div class="kpi-val" style="color:{kc}">{konsist:.0f}<span style="font-size:1rem;color:#6a7a95">/100</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=3; st.rerun()
    with cb:
        if st.button("🎯  Lihat Hasil Analisis SKORIA", type="primary"):
            st.session_state.data.update({"jam":jb,"hari":hb,"latihan":lat,"tryout":try_,"review":rev})
            st.session_state.result = compute(st.session_state.data)
            st.session_state.page="result"; st.rerun()

def page_survey():
    step_bar(st.session_state.step)
    {1:step1,2:step2,3:step3,4:step4}[st.session_state.step]()


# ══════════════════════════════════════════════════════════
# PAGE: RESULT
# ══════════════════════════════════════════════════════════
def page_result():
    r = st.session_state.result
    if not r: st.session_state.page="home"; st.rerun()

    nama = r.get("nama","Pejuang UTBK")
    jam  = datetime.datetime.now().hour
    salam= "Selamat pagi" if jam<11 else "Selamat siang" if jam<15 else "Selamat sore" if jam<18 else "Selamat malam"
    jenjang_lbl = r.get("jenjang","S1 (Sarjana)")
    jenjang_badge = "🎓 D3 Vokasi" if "D3" in jenjang_lbl else "🎓 S1 Sarjana"

    st.markdown(f"""<div class="hero" style="padding:1.7rem 2.4rem">
      <h1 style="font-size:1.55rem!important">{salam}, <span>{nama}!</span> 👋</h1>
      <p>Hasil analisis <strong style="color:#ffd166">SKORIA</strong> untuk
         <strong style="color:#ffd166">{jenjang_badge} — {r['jurusan']}</strong> di
         <strong style="color:rgba(255,255,255,.9)">{r['kampus']}</strong> · Skor skala 1000</p>
    </div>""", unsafe_allow_html=True)

    # ── KPI Row ──
    gc = "c-green" if r["gap"]>=0 else "c-red"
    pc = "c-green" if r["ppct"]>=65 else "c-orange" if r["ppct"]>=35 else "c-red"
    kc = "c-green" if r["pl"] in ("Sangat Aman","Aman") else "c-orange" if r["pl"]=="Kompetitif" else "c-red"

    k1,k2,k3,k4,k5 = st.columns(5)
    for col,lbl,val,cls,sub in [
        (k1,"Skor Tertimbang",f"{r['sw']:.0f}",kc,"dari 1000"),
        (k2,"Rata-rata Subtes",f"{r['rata']:.0f}","c-blue","7 subtes"),
        (k3,"Peluang Lolos",f"{r['ppct']:.0f}%",pc,r["pl"]),
        (k4,"Gap vs Minimum",f"{r['gap']:+.0f}",gc,f"Min {r['info']['mn']}"),
        (k5,"Risiko Underperform",r["risk"][0],
             "c-green" if r["risk"][0]=="Rendah" else "c-orange" if r["risk"][0]=="Sedang" else "c-red",
             r["risk"][1]),
    ]:
        with col:
            st.markdown(f"""<div class="card">
              <div class="kpi-lbl">{lbl}</div>
              <div class="kpi-val {cls}">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── LGBM Banner ──
    if r.get("lgbm_r") and r["lgbm_r"].get("ok"):
        h=r["lgbm_r"]; det=h.get("detail",{})
        kpct = f"{h['kpct']:.1f}%" if h.get("kpct") else ""
        tips = "".join(f"<li>{t}</li>" for t in det.get("tips",[]))
        st.markdown(f"""<div class="al al-s">
          <h4>🤖 Rekomendasi Strategi SKORIA AI — {det.get('icon','')} {h['strategi']}
            <span style="font-size:.78rem;font-weight:500;color:#6a7a95"> · Kepercayaan: {kpct}</span></h4>
          <em>{det.get('desc','')}</em>
          <ul style="margin-top:.35rem">{tips}</ul>
        </div>""", unsafe_allow_html=True)

    # ── Status Banner ──
    if r["pl"]=="Sangat Aman":
        st.markdown(f"""<div class="al al-s"><h4>🎯 Status: SANGAT AMAN</h4>
          Skor tertimbang <strong>{r['sw']:.0f}</strong> melampaui batas aman maksimum {r['info']['mx']} untuk {r['jurusan']} di {r['kampus']}.
          Pertahankan performa & jaga kondisi mental.</div>""", unsafe_allow_html=True)
    elif r["pl"]=="Aman":
        st.markdown(f"""<div class="al al-s"><h4>✅ Status: AMAN</h4>
          Skor {r['sw']:.0f} dalam zona aman ({r['info']['mn']}–{r['info']['mx']}).
          Tambah <strong>{r['info']['mx']-r['sw']:.0f} poin</strong> lagi untuk zona sangat aman.</div>""", unsafe_allow_html=True)
    elif r["pl"]=="Kompetitif":
        st.markdown(f"""<div class="al al-w"><h4>⚡ Status: KOMPETITIF</h4>
          Butuh <strong>+{r['info']['mn']-r['sw']:.0f} poin</strong> untuk zona aman di {r['jurusan']} - {r['kampus']}. Intensifkan latihan.</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="al al-d"><h4>🔴 Status: PERLU PENINGKATAN</h4>
          Gap <strong>{abs(r['gap']):.0f} poin</strong> dari minimum untuk {r['jurusan']} di {r['kampus']}. Pertimbangkan bimbingan intensif atau jurusan alternatif.</div>""", unsafe_allow_html=True)

    # ── TABS ──
    t1,t2,t3,t4,t5,t6,t7 = st.tabs([
        "📡 Radar & Skor TPS",
        "📊 Analisis Kampus",
        "🔀 Pipeline & Bobot",
        "🎓 Jurusan",
        "🚀 Strategi",
        "📅 Rencana Mingguan",
        "📄 Export PDF",
    ])

    # ─── TAB 1: RADAR + BAR ───
    with t1:
        st.markdown('<div class="sec">📡 Radar TPS vs Profil Ideal Jurusan</div>', unsafe_allow_html=True)
        ch_radar(r["skor"],r["bobot"],r["jurusan"], key="r_radar_t1")
        st.markdown('<div class="sec">📊 Skor Per Subtes vs Target Kampus</div>', unsafe_allow_html=True)
        ch_bar_subtes(r["skor"],r["bobot"],r["info"], key="r_bar_t1")
        st.markdown('<div class="sec">Detail Skor Subtes</div>', unsafe_allow_html=True)
        df_data = []
        for k in SUBTES:
            sv = r["skor"][k]
            status = "✅ Kuat" if sv>=750 else "⚡ Sedang" if sv>=550 else "🔴 Perlu Fokus"
            df_data.append({
                "Subtes": SUBTES_FULL[k],
                "Bobot (%)": f"{r['bobot'][k]*100:.0f}%",
                "Skor": sv,
                "Kontribusi": f"{sv*r['bobot'][k]:.1f}",
                "Status": status,
            })
        st.dataframe(
            pd.DataFrame(df_data),
            use_container_width=True, hide_index=True,
            column_config={
                "Skor": st.column_config.ProgressColumn("Skor", min_value=200, max_value=1000, format="%d"),
            }
        )

    # ─── TAB 2: ANALISIS KAMPUS ───
    with t2:
        st.markdown('<div class="sec">📊 Posisi Skor vs Klaster PTN</div>', unsafe_allow_html=True)
        ch_klaster(r["sw"], key="r_kl_t2")
        st.markdown(f'<div class="sec">🏛️ PTN Klaster {r["info"]["k"]} — Skor per {r["jurusan"]} ({r.get("jenjang","S1")})</div>', unsafe_allow_html=True)
        ch_ptn(r["sw"], r["info"]["k"], r["jurusan"], r.get("jenjang","S1 (Sarjana)"), key="r_ptn_t2")
        st.markdown('<div class="sec">Ringkasan Peluang per Klaster</div>', unsafe_allow_html=True)
        jenjang_r = r.get("jenjang","S1 (Sarjana)")
        kl_rows = []
        for kno,(mn_k,mx_k,knm) in [(1,(850,950,"⭐ Klaster 1 — Top Tier")),
                                      (2,(700,870,"🔷 Klaster 2 — Menengah Atas")),
                                      (3,(600,720,"🔹 Klaster 3 — Menengah")),
                                      (4,(555,660,"🔸 Klaster 4 — Regional"))]:
            if "D3" in jenjang_r:
                ptn_klaster = [k for k,v in PTN_D3_DATA.items() if v.get("_klaster")==kno]
                data_src = PTN_D3_DATA
            else:
                ptn_klaster = [k for k,v in PTN_JURUSAN_DATA.items() if v.get("_klaster")==kno]
                data_src = PTN_JURUSAN_DATA
            if ptn_klaster:
                info_k = get_ptn_info(ptn_klaster[0], r["jurusan"], jenjang_r)
                mn_k, mx_k = info_k["mn"], info_k["mx"]
            g = r["sw"] - mn_k
            if r["sw"]>=mx_k: st_k,p_k="🎯 Sangat Aman","~87%"
            elif r["sw"]>=mn_k: st_k,p_k="✅ Aman","~72%"
            elif r["sw"]>=mn_k-70: st_k,p_k="⚡ Kompetitif","~42%"
            else: st_k,p_k="🔴 Berisiko","~16%"
            kl_rows.append({
                "Klaster": knm,
                "Rentang Skor": f"{mn_k}–{mx_k}",
                "Skor Kamu": f"{r['sw']:.0f}",
                "Gap": f"{g:+.0f}",
                "Status": st_k,
                "Est. Peluang": p_k
            })
        st.dataframe(pd.DataFrame(kl_rows), use_container_width=True, hide_index=True)
        d1,d2,d3 = st.columns(3)
        with d1: st.metric("Skor Minimum Aman",r["info"]["mn"])
        with d2: st.metric("Skor Sangat Aman",r["info"]["mx"])
        with d3: st.metric("Skor Tertimbang Kamu",f"{r['sw']:.0f}",
                            delta=f"{r['gap']:+.0f} vs minimum",
                            delta_color="normal" if r["gap"]>=0 else "inverse")

    # ─── TAB 3: PIPELINE & BOBOT ───
    with t3:
        st.markdown('<div class="sec">🔀 Pipeline Kontribusi Subtes → Skor Total</div>', unsafe_allow_html=True)
        st.caption("Batang berwarna = kontribusi aktual. Batang transparan = target minimum kampus.")
        ch_pipeline(r["skor"],r["bobot"],r["info"],r["jurusan"], key="r_pipe_t3")
        st.markdown(f'<div class="sec">📐 Distribusi Bobot Subtes — {r["jurusan"]}</div>', unsafe_allow_html=True)
        ch_bobot(r["jurusan"], key="r_bobot_t3")
        st.markdown('<div class="sec">Tabel Bobot & Kontribusi Detail</div>', unsafe_allow_html=True)
        df_b_data = []
        for k in SUBTES:
            df_b_data.append({
                "Subtes": SUBTES_FULL[k],
                "Bobot": f"{r['bobot'][k]*100:.0f}%",
                "Skor": r["skor"][k],
                "Kontribusi Aktual": f"{r['skor'][k]*r['bobot'][k]:.1f}",
                "Target Minimum": f"{r['info']['mn']*r['bobot'][k]:.1f}",
                "Selisih": f"{(r['skor'][k]-r['info']['mn'])*r['bobot'][k]:+.1f}",
            })
        df_b_data.append({
            "Subtes": "TOTAL",
            "Bobot": "100%",
            "Skor": "—",
            "Kontribusi Aktual": f"{r['sw']:.1f}",
            "Target Minimum": f"{r['info']['mn']:.0f}",
            "Selisih": f"{r['gap']:+.1f}",
        })
        st.dataframe(pd.DataFrame(df_b_data), use_container_width=True, hide_index=True)
        with st.expander("📊 Lihat bobot semua jurusan"):
            rows_all = []
            for j,b in BOBOT_MAP.items():
                row={"Jurusan":j}; row.update({f"{k}(%)":f"{b[k]*100:.0f}" for k in SUBTES})
                rows_all.append(row)
            st.dataframe(pd.DataFrame(rows_all), use_container_width=True, hide_index=True)

    # ─── TAB 4: JURUSAN ───
    with t4:
        st.markdown(f'<div class="sec">🎓 Analisis Jurusan — {r["jurusan"]}</div>', unsafe_allow_html=True)
        if r["aman"]:
            st.markdown(f"""<div class="al al-s">
              <h4>🎯 FOKUS KE JURUSAN TARGET: {r['jurusan']}</h4>
              Peluang lolos <strong>{r['pl']}</strong> ({r['ppct']:.0f}%) — tidak perlu berpindah jurusan.
              Pertahankan dan tingkatkan skor menjelang UTBK.
            </div>""", unsafe_allow_html=True)
            bobot_chips(r["jurusan"])
            col_a, col_b = st.columns(2)
            with col_a:
                ch_bobot(r["jurusan"], key="r_bobot_t4_main")
            with col_b:
                st.markdown("<p style='color:#3a4a65;font-weight:600;margin-bottom:.8rem'>📈 Indikator Kesiapan:</p>", unsafe_allow_html=True)
                prog_bar("Kesiapan Mental",r["psiko"],"#3b6cb7")
                prog_bar("Konsistensi Belajar",r["konsist"],"#1a8a4a")
                prog_bar("Stabilitas Mental",r["stab"],"#7048c8")
            bs = sorted(r["bobot"].items(),key=lambda x:x[1],reverse=True)
            st.markdown('<div class="sec">🔑 Subtes Kunci (Bobot Tertinggi)</div>', unsafe_allow_html=True)
            sc = st.columns(3)
            for col,(k,bv) in zip(sc,bs[:3]):
                sv = r["skor"][k]
                kc2 = "c-green" if sv>=750 else "c-gold" if sv>=550 else "c-red"
                with col:
                    st.markdown(f"""<div class="card" style="text-align:center">
                      <div class="kpi-lbl">{SUBTES_FULL[k]}</div>
                      <div class="kpi-val {kc2}">{sv}</div>
                      <div class="kpi-sub">Bobot {int(bv*100)}% {'✅' if sv>=750 else '⚡' if sv>=550 else '🔴'}</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown('<div class="sec">📋 Jurusan Alternatif (Cadangan)</div>', unsafe_allow_html=True)
            st.markdown('<div class="al al-i"><h4>ℹ️ Info</h4>Skor kamu sudah aman. Alternatif ini hanya cadangan formalitas.</div>', unsafe_allow_html=True)
            alt = r["alternatif"]
            if alt:
                ac = st.columns(len(alt))
                for col,j in zip(ac,alt):
                    with col:
                        bj=get_bobot(j); swj=hitung_tw(r["skor"],bj)
                        plj,_,pctj=hitung_peluang(swj,r["kampus"],j,r.get("jenjang","S1 (Sarjana)"))
                        st.markdown(f"""<div class="card" style="text-align:center;opacity:.75">
                          <div style="font-size:.7rem;color:#6a7a95">Alternatif</div>
                          <div style="font-weight:700;font-size:.87rem;margin:.2rem 0;color:#1a2540">{j}</div>
                          <div style="font-size:.75rem;color:#3a4a65">{plj} ({pctj:.0f}%)</div>
                        </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-w">
              <h4>⚡ Skor Belum Zona Aman — {r['jurusan']}</h4>
              Butuh <strong>+{r['info']['mn']-r['sw']:.0f} poin</strong>. Pertimbangkan jurusan alternatif.
            </div>""", unsafe_allow_html=True)
            bobot_chips(r["jurusan"])
            ch_bobot(r["jurusan"], key="r_bobot_t4_alt")
            st.markdown('<div class="sec">🔄 Jurusan Alternatif yang Direkomendasikan</div>', unsafe_allow_html=True)
            for idx,j in enumerate(r["alternatif"]):
                bj = get_bobot(j); swj = hitung_tw(r["skor"],bj)
                plj,_,pctj = hitung_peluang(swj, r["kampus"], j, r.get("jenjang","S1 (Sarjana)"))
                info_j = get_ptn_info(r["kampus"], j, r.get("jenjang","S1 (Sarjana)"))
                with st.expander(f"📚 {j}  —  Skor: {swj:.0f}  |  {plj}  ({pctj:.0f}%)"):
                    ca2,cb2 = st.columns(2)
                    with ca2:
                        st.metric("Skor Tertimbang",f"{swj:.0f}")
                        st.metric("Peluang",f"{pctj:.0f}% ({plj})")
                        st.metric("Skor Aman",f"{info_j['mn']}–{info_j['mx']}")
                        bobot_chips(j)
                    with cb2:
                        ch_bobot(j, key=f"r_bobot_alt_{idx}")

    # ─── TAB 5: STRATEGI ───
    with t5:
        st.markdown('<div class="sec">🚀 Strategi Belajar Personal</div>', unsafe_allow_html=True)
        ch_psiko(r["psiko"],r["konsist"],r["stab"], key="r_psiko_t5")
        prog_bar("Kesiapan Mental",r["psiko"],"#3b6cb7")
        prog_bar("Konsistensi Belajar",r["konsist"],"#1a8a4a")
        prog_bar("Stabilitas Mental",r["stab"],"#7048c8")
        st.markdown('<div class="sec">📌 Prioritas Subtes</div>', unsafe_allow_html=True)
        ss = sorted(r["skor"].items(),key=lambda x:x[1])
        lemah3 = ss[:3]; kuat2 = ss[-2:]
        cp1,cp2 = st.columns(2)
        with cp1:
            il = "".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} → perlu +{max(0,750-v)} poin</li>" for k,v in lemah3)
            st.markdown(f'<div class="al al-d"><h4>🔴 3 Subtes Perlu Fokus</h4><ul>{il}</ul></div>',unsafe_allow_html=True)
        with cp2:
            ik = "".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} ✅</li>" for k,v in kuat2)
            st.markdown(f'<div class="al al-s"><h4>🟢 Kekuatan Akademik</h4><ul>{ik}</ul></div>',unsafe_allow_html=True)
        st.markdown('<div class="sec">📋 Rencana Aksi</div>', unsafe_allow_html=True)
        if r["sw"]>=r["info"]["mx"]:
            st.markdown("""<div class="al al-s"><h4>🏆 Maintenance Mode</h4><ul>
              <li>Tryout 1–2x/minggu untuk menjaga ketajaman</li>
              <li>Review kesalahan kecil yang masih berulang</li>
              <li>Fokus manajemen waktu dan kondisi mental</li>
              <li>Jaga pola tidur 7–8 jam/malam</li></ul></div>""",unsafe_allow_html=True)
        elif r["sw"]>=r["info"]["mn"]:
            st.markdown(f"""<div class="al al-i"><h4>✅ Penguatan & Konsistensi</h4><ul>
              <li>Target +{r['info']['mx']-r['sw']:.0f} poin untuk zona sangat aman</li>
              <li>60% waktu pada {SUBTES_FULL[ss[0][0]]} (terlemah)</li>
              <li>Tryout min. 2x/bulan + review mendalam</li>
              <li>Simulasi 150 soal dalam 2.5 jam/sesi</li></ul></div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-w"><h4>⚡ Intensifikasi Penuh</h4><ul>
              <li>Target +{r['info']['mn']-r['sw']:.0f} poin — bertahap +{min(60,r['info']['mn']-r['sw']):.0f}/bulan</li>
              <li>Belajar 4–5 jam/hari terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Konsultasi tutor untuk subtes berbobot tinggi</li></ul></div>""",unsafe_allow_html=True)
        st.markdown('<div class="sec">🧠 Tips Psikologis</div>', unsafe_allow_html=True)
        tp1,tp2 = st.columns(2)
        with tp1:
            if r.get("fokus",3)<=2:
                st.markdown('<div class="al al-d"><h4>🎯 Fokus Rendah</h4><ul><li>Pomodoro 25+5 mnt</li><li>Matikan notifikasi HP</li><li>Mulai sesi pendek 15 mnt</li></ul></div>',unsafe_allow_html=True)
            if r.get("cemas",3)>=4:
                st.markdown('<div class="al al-d"><h4>😰 Kecemasan Tinggi</h4><ul><li>Pernapasan 4-7-8 tiap pagi</li><li>Fokus proses bukan hasil</li><li>Tidur 7–8 jam/malam</li></ul></div>',unsafe_allow_html=True)
        with tp2:
            if r.get("distrak",3)>=4:
                st.markdown('<div class="al al-d"><h4>📱 Distraksi Tinggi</h4><ul><li>Cold Turkey / Forest app</li><li>HP di ruangan lain</li><li>Reward setelah selesai sesi</li></ul></div>',unsafe_allow_html=True)
            if r.get("review",3)<=2:
                st.markdown('<div class="al al-w"><h4>📝 Review Soal Kurang</h4><ul><li>Review SETIAP soal salah</li><li>Buku catatan soal sulit</li></ul></div>',unsafe_allow_html=True)

    # ─── TAB 6: RENCANA MINGGUAN ───
    with t6:
        st.markdown('<div class="sec">📅 Proyeksi Skor 8 Minggu ke Depan</div>', unsafe_allow_html=True)
        ch_progress(r, key="r_prog_t6")
        st.markdown('<div class="sec">📋 Detail Rencana Per Minggu</div>', unsafe_allow_html=True)
        rencana = buat_rencana_mingguan(r, 8)
        fase_clr = {"Fondasi":"#3b6cb7","Intensif":"#d4620a","Pemantapan":"#1a8a4a","Final":"#c8890a"}
        for m in rencana:
            clr = fase_clr.get(m["fase"],"#7048c8")
            tasks_html = "".join(f'<div style="padding:.1rem 0;color:#3a4a65">• {t}</div>' for t in m["tasks"])
            st.markdown(f"""<div class="week-card">
              <div class="week-num" style="color:{clr}">MINGGU {m['minggu']} — {m['fase'].upper()}</div>
              <div class="week-target">
                🎯 Target skor: <strong style="color:{clr}">{m['target_skor']}</strong> &nbsp;|&nbsp; ⏰ {m['jam']}
              </div>
              <div class="week-tasks">{tasks_html}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">Ringkasan Rencana 8 Minggu</div>', unsafe_allow_html=True)
        df_r = pd.DataFrame([{
            "Minggu": f"Minggu {m['minggu']}",
            "Fase": m["fase"],
            "Target Skor": m["target_skor"],
            "Durasi Belajar": m["jam"],
            "Fokus Utama": m["fokus"]
        } for m in rencana])
        st.dataframe(df_r, use_container_width=True, hide_index=True)

    # ─── TAB 7: PDF ───
    with t7:
        st.markdown('<div class="sec">📄 Export Laporan ke PDF</div>', unsafe_allow_html=True)
        st.markdown("""<div class="al al-i"><h4>Cara Menyimpan sebagai PDF</h4><ol>
          <li>Klik tombol <strong>Generate & Download Laporan HTML</strong> di bawah</li>
          <li>Buka file HTML yang terdownload di browser</li>
          <li>Tekan <strong>Ctrl+P</strong> (Win) atau <strong>Cmd+P</strong> (Mac)</li>
          <li>Pilih <strong>"Save as PDF"</strong> sebagai printer</li>
          <li>Klik <strong>Save</strong></li>
        </ol></div>""", unsafe_allow_html=True)
        if st.button("📄  Generate & Download Laporan HTML", type="primary"):
            html = generate_pdf(r)
            b64  = base64.b64encode(html.encode()).decode()
            fn   = f"skoria_{r.get('nama','').replace(' ','_')}.html"
            st.markdown(f"""<a href="data:text/html;base64,{b64}" download="{fn}"
              style="display:inline-block;background:linear-gradient(135deg,#3b6cb7,#2a4a8c);
                     color:#ffffff;font-weight:700;padding:.6rem 1.4rem;border-radius:8px;
                     text-decoration:none;font-family:'Sora',sans-serif;font-size:.9rem;margin-top:.5rem">
              ⬇️ Download {fn}</a>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">Preview Ringkasan Laporan</div>', unsafe_allow_html=True)
        pp1,pp2 = st.columns(2)
        with pp1:
            st.dataframe(pd.DataFrame([
                {"Info": "Nama", "Detail": r.get("nama","—")},
                {"Info": "Jurusan", "Detail": r["jurusan"]},
                {"Info": "Kampus", "Detail": r["kampus"]},
                {"Info": "Klaster", "Detail": r["info"]["lbl"]},
                {"Info": "Skor Tertimbang", "Detail": f"{r['sw']:.0f} / 1000"},
                {"Info": "Gap vs Minimum", "Detail": f"{r['gap']:+.0f}"},
            ]), use_container_width=True, hide_index=True)
        with pp2:
            st.dataframe(pd.DataFrame([
                {"Indikator": "Peluang Lolos", "Nilai": f"{r['ppct']:.0f}% ({r['pl']})"},
                {"Indikator": "Kesiapan Mental", "Nilai": f"{r['psiko']:.0f}/100"},
                {"Indikator": "Konsistensi", "Nilai": f"{r['konsist']:.0f}/100"},
                {"Indikator": "Stabilitas", "Nilai": f"{r['stab']:.0f}/100"},
                {"Indikator": "Risiko Underperform", "Nilai": f"{r['risk'][0]} {r['risk'][1]}"},
            ]), use_container_width=True, hide_index=True)

    # ── Footer ──
    st.divider()
    nb1,nb2,_ = st.columns([1,1,4])
    with nb1:
        if st.button("◀ Ubah Data"): st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with nb2:
        if st.button("🏠 Beranda"): st.session_state.page="home"; st.rerun()

    st.markdown(f"""<div style="text-align:center;padding:1.4rem;background:var(--surf);
      border-radius:var(--r);border:1px solid var(--border);margin-top:.8rem;
      box-shadow:var(--shadow)">
      <div style="font-family:'Sora',sans-serif;font-size:1.05rem;font-weight:800;color:#1a2540">
        💪 {nama}, kamu pasti bisa!
      </div>
      <div style="color:#6a7a95;font-size:.82rem;margin-top:.3rem">
        Konsistensi + strategi tepat = PTN impianmu pasti bisa diraih 🚀
      </div>
      <div style="color:#b0b8c8;font-size:.7rem;margin-top:.3rem">
        🎯 SKORIA v4.0 — AI UTBK Intelligence · LightGBM + Data SNPMB 2025/2026 · S1 & D3 · Skor skala 200–1000
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    render_nav()
    {"home":page_home,"survey":page_survey,"result":page_result}[st.session_state.page]()

if __name__=="__main__":
    main()
