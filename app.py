"""
SKORIA — AI UTBK Readiness Dashboard v2.0
Platform kecerdasan buatan untuk analisis kesiapan UTBK secara holistik
Skor maksimal: 1000 | Multi-halaman | Charts | PDF Export
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
# GLOBAL CSS — Soft dark navy theme, readable typography
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Fraunces:wght@600;700;800&display=swap');

:root {
  --bg:       #1a1f2e;
  --surf:     #232a3b;
  --surf2:    #2a3347;
  --border:   #3a4560;
  --accent:   #6c9bd2;
  --accent2:  #8bb8e8;
  --gold:     #d4a847;
  --gold2:    #ecc96a;
  --green:    #52c97a;
  --green2:   #7adeA0;
  --red:      #e06c75;
  --orange:   #e09a52;
  --purple:   #9d7be8;
  --teal:     #4ec9b0;
  --text:     #e8edf5;
  --text2:    #b8c4d8;
  --text3:    #8a9ab8;
  --r:        12px;
}

html,body,[class*="css"],.stApp {
  background: var(--bg) !important;
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden }
.stDeployButton { display: none }
.block-container { padding: 1rem 1.5rem !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
  background: linear-gradient(90deg, #1e2540, #252d45);
  border-bottom: 1px solid var(--border);
  padding: .7rem 2rem;
  display: flex; align-items: center; gap: 1.2rem;
  margin: -1rem -1.5rem 1.5rem -1.5rem;
  position: sticky; top: 0; z-index: 999;
}
.topbar-brand {
  font-family: 'Fraunces', serif;
  font-size: 1.15rem; font-weight: 800;
  color: var(--gold) !important;
  display: flex; align-items: center; gap: .5rem;
}
.topbar-tag {
  font-size: .7rem; font-weight: 500;
  color: var(--text3); letter-spacing: .05em;
}
.step-pill {
  font-size: .75rem; font-weight: 600;
  padding: .28rem .8rem; border-radius: 99px;
  color: var(--text3); cursor: default;
}
.step-pill.done  { background: rgba(82,201,122,.12); color: var(--green); }
.step-pill.active{ background: rgba(212,168,71,.14); color: var(--gold); border: 1px solid rgba(212,168,71,.3); }

/* ── HERO ── */
.hero {
  background: linear-gradient(135deg, #1c2338 0%, #222d45 60%, #1e2a40 100%);
  border: 1px solid var(--border);
  border-radius: 16px; padding: 2.5rem 3rem;
  margin-bottom: 1.8rem; position: relative; overflow: hidden;
}
.hero::before {
  content: ''; position: absolute; top: -60px; right: -60px;
  width: 320px; height: 320px; border-radius: 50%;
  background: radial-gradient(circle, rgba(212,168,71,.08) 0%, transparent 65%);
}
.hero::after {
  content: ''; position: absolute; bottom: -80px; left: 5%;
  width: 280px; height: 280px; border-radius: 50%;
  background: radial-gradient(circle, rgba(108,155,210,.06) 0%, transparent 65%);
}
.hero h1 {
  font-family: 'Fraunces', serif !important;
  font-size: 2.1rem !important; font-weight: 800 !important;
  color: #fff !important; margin: 0 0 .6rem !important; line-height: 1.2 !important;
}
.hero h1 span { color: var(--gold); }
.hero p { color: var(--text2) !important; font-size: .95rem; margin: 0; line-height: 1.65; }

/* ── CARDS ── */
.card {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.3rem 1.5rem;
}
.card-dark {
  background: var(--surf2);
  border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.2rem 1.4rem;
}
.kpi-lbl {
  font-size: .68rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .1em; color: var(--text3); margin-bottom: .35rem;
}
.kpi-val {
  font-family: 'Fraunces', serif;
  font-size: 2rem; font-weight: 700; line-height: 1; color: var(--text);
}
.kpi-sub { font-size: .73rem; color: var(--text3); margin-top: .2rem; }

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
  font-family: 'Fraunces', serif; font-size: 1rem; font-weight: 700;
  color: var(--text); margin: 1.6rem 0 .8rem;
  padding-bottom: .35rem; border-bottom: 2px solid var(--border);
}

/* ── ALERTS ── */
.al {
  border-radius: var(--r); padding: 1rem 1.3rem; margin-bottom: .85rem;
  border-left: 4px solid; font-size: .87rem; line-height: 1.7; color: var(--text2);
}
.al h4 { margin: 0 0 .4rem; font-size: .9rem; font-weight: 700; color: var(--text); }
.al ul, .al ol { margin: .35rem 0 0; padding-left: 1.2rem; color: var(--text2); }
.al ul li, .al ol li { margin-bottom: .2rem; }
.al strong { color: var(--text); }
.al code { color: var(--gold2); background: rgba(212,168,71,.1); padding: 1px 5px; border-radius: 4px; }
.al-s { background: rgba(82,201,122,.07); border-color: var(--green); }
.al-s h4 { color: var(--green); }
.al-w { background: rgba(224,154,82,.07); border-color: var(--orange); }
.al-w h4 { color: var(--orange); }
.al-d { background: rgba(224,108,117,.07); border-color: var(--red); }
.al-d h4 { color: var(--red); }
.al-i { background: rgba(108,155,210,.07); border-color: var(--accent); }
.al-i h4 { color: var(--accent2); }
.al-p { background: rgba(157,123,232,.07); border-color: var(--purple); }
.al-p h4 { color: var(--purple); }

/* ── PROGRESS BARS ── */
.prog-wrap { margin-bottom: .8rem; }
.prog-lbl {
  display: flex; justify-content: space-between;
  font-size: .8rem; font-weight: 600; color: var(--text2); margin-bottom: 4px;
}
.prog-bg { background: var(--surf2); border-radius: 99px; height: 8px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 99px; }

/* ── STEP BAR ── */
.step-row {
  display: flex; margin-bottom: 2rem;
  background: var(--surf); border: 1px solid var(--border);
  border-radius: var(--r); overflow: hidden;
}
.step-item {
  flex: 1; padding: .9rem; text-align: center;
  font-size: .76rem; font-weight: 600; color: var(--text3);
  border-right: 1px solid var(--border);
}
.step-item:last-child { border-right: none; }
.step-item.active { background: rgba(212,168,71,.09); color: var(--gold); }
.step-item.done   { background: rgba(82,201,122,.06); color: var(--green); }
.step-num {
  display: block; font-size: 1.2rem;
  font-family: 'Fraunces', serif; font-weight: 800; margin-bottom: 1px;
}

/* ── FORM BOX ── */
.form-box {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.8rem 2rem; margin-bottom: 1.3rem;
}
.form-box h3 {
  font-family: 'Fraunces', serif; font-size: 1rem; font-weight: 700;
  color: var(--gold); margin: 0 0 1.2rem;
}

/* ── BOBOT CHIP ── */
.bobot-chip {
  display: inline-flex; flex-direction: column; align-items: center;
  background: rgba(108,155,210,.08); border: 1px solid rgba(108,155,210,.2);
  border-radius: 9px; padding: .45rem .65rem; margin: .15rem;
}
.bobot-chip .sk { font-size: .65rem; color: var(--text3); margin-bottom: 1px; }
.bobot-chip .bv {
  font-size: 1rem; font-weight: 700; color: var(--accent2);
  font-family: 'Fraunces', serif;
}

/* ── WEEK TABLE ── */
.week-card {
  background: var(--surf2); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: .7rem;
}
.week-num {
  font-family: 'Fraunces', serif; font-size: .75rem; font-weight: 700;
  color: var(--accent); text-transform: uppercase; letter-spacing: .08em;
  margin-bottom: .3rem;
}
.week-target { font-size: .85rem; font-weight: 600; color: var(--text); margin-bottom: .25rem; }
.week-tasks { font-size: .8rem; color: var(--text2); line-height: 1.65; }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stButton"] button[kind="primary"] {
  background: linear-gradient(135deg, var(--gold), #c9962e) !important;
  color: #1a1f2e !important; font-weight: 700 !important;
  font-family: 'Fraunces', serif !important;
  border: none !important; border-radius: 10px !important;
  font-size: .9rem !important; letter-spacing: .02em !important;
}
div[data-testid="stButton"] button {
  background: var(--surf2) !important; color: var(--text2) !important;
  border: 1px solid var(--border) !important; border-radius: 10px !important;
  font-weight: 600 !important;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
  font-family: 'Fraunces', serif !important; font-weight: 600 !important;
  font-size: .82rem !important; color: var(--text3) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--gold) !important; border-bottom-color: var(--gold) !important;
}
div[data-testid="stMetric"] {
  background: var(--surf) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important; padding: 1rem 1.2rem !important;
}
div[data-testid="stMetric"] label {
  color: var(--text3) !important; font-size: .72rem !important;
  font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: .07em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: var(--text) !important; font-family: 'Fraunces', serif !important;
}
div[data-testid="stExpander"] {
  background: var(--surf) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
}
div[data-testid="stExpander"] summary { color: var(--text2) !important; font-weight: 600 !important; }
/* Labels */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stRadio"] label {
  color: var(--text2) !important; font-weight: 600 !important; font-size: .85rem !important;
}
div[data-testid="stTextInput"] input {
  background: var(--surf2) !important; color: var(--text) !important;
  border-color: var(--border) !important;
}
.stCaption, [data-testid="stCaptionContainer"], .stCaption p {
  color: var(--text3) !important; font-size: .78rem !important;
}
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
/* Selectbox dropdown text */
div[data-baseweb="select"] { background: var(--surf2) !important; }
div[data-baseweb="select"] * { color: var(--text) !important; }
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
    "PU": "#d4a847", "PPU": "#6c9bd2", "PBM": "#9d7be8",
    "PK": "#e06c75", "LBI": "#52c97a", "LBE": "#4ec9b0", "PM": "#e09a52",
}

DAFTAR_JURUSAN = [
    "Kedokteran","Kedokteran Gigi",
    "Teknik Sipil","Teknik Mesin","Teknik Elektro","Teknik Industri","Teknik Kimia","Teknik Informatika",
    "Matematika","Fisika","Kimia","Biologi","Statistika","Aktuaria",
    "Farmasi","Gizi","Keperawatan","Kesehatan Masyarakat",
    "Ilmu Hukum","Ekonomi","Manajemen","Akuntansi","Bisnis",
    "Psikologi","Ilmu Komunikasi","Hubungan Internasional","Administrasi Publik",
    "Sastra Inggris","Pendidikan Bahasa Indonesia","Pendidikan Bahasa Inggris",
    "Sosiologi","Ilmu Politik","Sejarah","Geografi"
]

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

# PTN data — skor aman naik 100 poin dari sebelumnya (skala 1000)
PTN_DATA = {
    "Universitas Indonesia (UI)":                {"k":1,"mn":880,"mx":960,"lbl":"⭐ Klaster 1 — Top Tier"},
    "Universitas Gadjah Mada (UGM)":             {"k":1,"mn":880,"mx":960,"lbl":"⭐ Klaster 1 — Top Tier"},
    "Institut Teknologi Bandung (ITB)":          {"k":1,"mn":890,"mx":970,"lbl":"⭐ Klaster 1 — Top Tier"},
    "Universitas Padjadjaran (Unpad)":           {"k":1,"mn":860,"mx":940,"lbl":"⭐ Klaster 1 — Top Tier"},
    "Institut Pertanian Bogor (IPB)":            {"k":1,"mn":850,"mx":930,"lbl":"⭐ Klaster 1 — Top Tier"},
    "Universitas Diponegoro (Undip)":            {"k":2,"mn":800,"mx":870,"lbl":"🔷 Klaster 2 — Menengah Atas"},
    "Universitas Airlangga (Unair)":             {"k":2,"mn":810,"mx":880,"lbl":"🔷 Klaster 2 — Menengah Atas"},
    "Universitas Brawijaya (UB)":                {"k":2,"mn":780,"mx":855,"lbl":"🔷 Klaster 2 — Menengah Atas"},
    "Institut Teknologi Sepuluh Nopember (ITS)": {"k":2,"mn":810,"mx":885,"lbl":"🔷 Klaster 2 — Menengah Atas"},
    "Universitas Sebelas Maret (UNS)":           {"k":2,"mn":760,"mx":840,"lbl":"🔷 Klaster 2 — Menengah Atas"},
    "Universitas Hasanuddin (Unhas)":            {"k":2,"mn":760,"mx":840,"lbl":"🔷 Klaster 2 — Menengah Atas"},
    "Universitas Negeri Yogyakarta (UNY)":       {"k":3,"mn":710,"mx":790,"lbl":"🔹 Klaster 3 — Menengah"},
    "Universitas Negeri Semarang (UNNES)":       {"k":3,"mn":700,"mx":780,"lbl":"🔹 Klaster 3 — Menengah"},
    "Universitas Negeri Malang (UM)":            {"k":3,"mn":700,"mx":780,"lbl":"🔹 Klaster 3 — Menengah"},
    "Universitas Andalas (Unand)":               {"k":3,"mn":700,"mx":780,"lbl":"🔹 Klaster 3 — Menengah"},
    "Universitas Sumatera Utara (USU)":          {"k":3,"mn":690,"mx":770,"lbl":"🔹 Klaster 3 — Menengah"},
    "Universitas Sriwijaya (Unsri)":             {"k":4,"mn":650,"mx":730,"lbl":"🔸 Klaster 4 — Regional"},
    "Universitas Lampung (Unila)":               {"k":4,"mn":640,"mx":720,"lbl":"🔸 Klaster 4 — Regional"},
    "Universitas Jember (Unej)":                 {"k":4,"mn":635,"mx":715,"lbl":"🔸 Klaster 4 — Regional"},
    "Universitas Riau (Unri)":                   {"k":4,"mn":630,"mx":710,"lbl":"🔸 Klaster 4 — Regional"},
}
DAFTAR_PTN = list(PTN_DATA.keys())

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
def get_bobot(j): return BOBOT_MAP.get(j, DEFAULT_BOBOT)

def hitung_tw(skor, bobot): return sum(skor[k]*bobot[k] for k in SUBTES)

def get_ptn(k): return PTN_DATA.get(k, {"k":4,"mn":630,"mx":710,"lbl":"🔸 Klaster 4"})

def hitung_peluang(sw, kampus):
    d = get_ptn(kampus); mn,mx = d["mn"], d["mx"]
    g = sw - mn
    if sw >= mx:      return "Sangat Aman","#52c97a", min(93.,76+(sw-mx)/mx*12)
    elif sw >= mn:    return "Aman","#52c97a",        62+(sw-mn)/(mx-mn)*13
    elif sw >= mn-70: return "Kompetitif","#e09a52",  32+(70+g)/70*25
    elif sw >= mn-140:return "Berisiko","#e06c75",    16.
    else:             return "Perlu Peningkatan","#e06c75", 8.

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
    pl,pc,ppct = hitung_peluang(sw, d["kampus"])
    info  = get_ptn(d["kampus"])
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

    return {**d,"skor":skor,"bobot":bobot,"sw":sw,"rata":rata,
            "pl":pl,"pc":pc,"ppct":ppct,"info":info,"gap":gap,
            "psiko":psiko,"konsist":konsist,"stab":stab,"risk":risk,
            "lgbm_r":lgbm_r,"aman":aman,
            "alternatif":ALTERNATIF_MAP.get(d["jurusan"],[])}


# ══════════════════════════════════════════════════════════
# RENCANA BELAJAR MINGGUAN
# ══════════════════════════════════════════════════════════
def buat_rencana_mingguan(r, n_minggu=8):
    """Generate rencana belajar mingguan berdasarkan profil siswa"""
    skor  = r["skor"]
    bobot = r["bobot"]
    gap   = r["gap"]
    sw    = r["sw"]
    mn    = r["info"]["mn"]
    mx    = r["info"]["mx"]

    # Urutkan subtes dari terlemah
    ranked = sorted(SUBTES, key=lambda k: skor[k])
    terlemah3 = ranked[:3]
    sedang2   = ranked[3:5]
    terkuat2  = ranked[5:]

    # Target kenaikan per minggu
    if gap < 0:
        target_per_minggu = abs(gap) / n_minggu + 10
    else:
        target_per_minggu = (mx - sw) / n_minggu + 5 if sw < mx else 5

    rencana = []
    for w in range(1, n_minggu+1):
        fase = "Fondasi" if w <= 2 else "Intensif" if w <= 5 else "Pemantapan" if w <= 7 else "Final"
        target_sw = min(mx+20, sw + target_per_minggu * w)

        if fase == "Fondasi":
            fokus_subtes = terlemah3[0] if terlemah3 else "PU"
            tasks = [
                f"Review konsep dasar {SUBTES_FULL[terlemah3[0]]} ({skor[terlemah3[0]]} → target +30)",
                f"50 soal latihan {SUBTES_FULL[terlemah3[1]]} dengan timer",
                f"Pelajari pola soal {SUBTES_FULL[terlemah3[2]]}",
                "Buat catatan kesalahan (error log)",
                "Tryout mini: 30 soal campuran + analisis",
            ]
            jam = "2–3 jam/hari"
        elif fase == "Intensif":
            fokus_subtes = terlemah3[w-3] if w-3 < len(terlemah3) else sedang2[0]
            subtes_minggu = terlemah3 + sedang2
            subtes_ini = subtes_minggu[(w-3) % len(subtes_minggu)] if subtes_minggu else "PU"
            tasks = [
                f"100 soal latihan {SUBTES_FULL[subtes_ini]} + timer ketat",
                f"Review error log minggu sebelumnya",
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
        else:  # Final
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
# CHART THEME
# ══════════════════════════════════════════════════════════
CTH = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#b8c4d8'),
    margin=dict(l=10, r=10, t=45, b=10)
)

def ch_radar(skor, bobot, jurusan, key=None):
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal, theta=cats, fill='toself', name='Profil Ideal Jurusan',
        fillcolor='rgba(212,168,71,.06)', line=dict(color='#d4a847', dash='dot', width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,  theta=cats, fill='toself', name='Skor Kamu',
        fillcolor='rgba(108,155,210,.15)', line=dict(color='#6c9bd2', width=2.5)))
    fig.update_layout(**CTH, polar=dict(
        bgcolor='rgba(35,42,59,.85)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS], gridcolor='#3a4560', linecolor='#3a4560',
                        tickfont=dict(size=9, color='#8a9ab8')),
        angularaxis=dict(gridcolor='#3a4560', linecolor='#3a4560', tickfont=dict(size=9.5, color='#b8c4d8'))),
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', x=.5, xanchor='center', y=-.15,
                    font=dict(color='#b8c4d8')),
        title=dict(text=f"Radar TPS — {jurusan}", font=dict(size=13, color='#e8edf5')), height=400)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("radar"))

def ch_bar_subtes(skor, bobot, info, key=None):
    lbl  = [SUBTES_FULL[k] for k in SUBTES]
    vals = [skor[k] for k in SUBTES]
    tgt  = [min(SKOR_MAX_TPS,(info["mn"]+info["mx"])/2*bobot[k]*7) for k in SUBTES]
    clrs = [SUBTES_CLR[k] for k in SUBTES]
    fig  = go.Figure()
    fig.add_trace(go.Bar(name='Skor Kamu', x=lbl, y=vals, marker_color=clrs, marker_line_width=0,
        text=[str(v) for v in vals], textposition='outside', textfont=dict(size=10, color='#e8edf5')))
    fig.add_trace(go.Scatter(name='Target Kampus', x=lbl, y=tgt, mode='markers+lines',
        marker=dict(symbol='diamond', size=9, color='#d4a847'),
        line=dict(color='#d4a847', dash='dot', width=1.5)))
    fig.update_layout(**CTH, barmode='group',
        xaxis=dict(tickfont=dict(size=9, color='#b8c4d8'), gridcolor='#3a4560'),
        yaxis=dict(range=[0, SKOR_MAX_TPS*1.07], gridcolor='#2a3347', tickfont=dict(size=9, color='#b8c4d8')),
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', x=.5, xanchor='center', y=-.2, font=dict(color='#b8c4d8')),
        title=dict(text="Skor Per Subtes vs Target Kampus", font=dict(size=13, color='#e8edf5')), height=370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("bar"))

def ch_pipeline(skor, bobot, info, jurusan, key=None):
    lbl    = [SUBTES_FULL[k] for k in SUBTES]
    aktual = [skor[k]*bobot[k] for k in SUBTES]
    ideal  = [info["mn"]*bobot[k] for k in SUBTES]
    clrs   = [SUBTES_CLR[k] for k in SUBTES]
    fig    = go.Figure()
    fig.add_trace(go.Bar(name='Target Min Kampus', y=lbl, x=ideal, orientation='h',
        marker_color=['rgba(212,168,71,.14)']*7,
        marker_line_color='#d4a847', marker_line_width=1.5))
    fig.add_trace(go.Bar(name='Kontribusi Aktual', y=lbl, x=aktual, orientation='h',
        marker_color=clrs, text=[f"{v:.1f}" for v in aktual],
        textposition='inside', textfont=dict(size=10, color='#fff')))
    fig.update_layout(**CTH, barmode='overlay',
        xaxis=dict(title="Kontribusi ke Skor Total", gridcolor='#2a3347',
                   title_font=dict(color='#8a9ab8'), tickfont=dict(size=9, color='#b8c4d8')),
        yaxis=dict(gridcolor='#3a4560', tickfont=dict(size=10, color='#b8c4d8')),
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', x=.5, xanchor='center', y=-.13, font=dict(color='#b8c4d8')),
        title=dict(text=f"Pipeline Kontribusi Subtes — {jurusan}", font=dict(size=13, color='#e8edf5')), height=380)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("pipe"))

def ch_bobot(jurusan, key=None):
    bobot = get_bobot(jurusan)
    lbl   = [SUBTES_FULL[k] for k in SUBTES]
    vals  = [bobot[k]*100 for k in SUBTES]
    clrs  = [SUBTES_CLR[k] for k in SUBTES]
    fig   = go.Figure(go.Bar(x=lbl, y=vals, marker_color=clrs, marker_line_width=0,
        text=[f"{v:.0f}%" for v in vals], textposition='outside', textfont=dict(size=10, color='#e8edf5')))
    fig.update_layout(**CTH,
        xaxis=dict(tickfont=dict(size=9, color='#b8c4d8'), gridcolor='#3a4560'),
        yaxis=dict(range=[0,55], ticksuffix="%", gridcolor='#2a3347',
                   title="Bobot (%)", title_font=dict(color='#8a9ab8'), tickfont=dict(size=9, color='#b8c4d8')),
        title=dict(text=f"Distribusi Bobot Subtes — {jurusan}", font=dict(size=13, color='#e8edf5')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("bobot"))

def ch_klaster(sw, key=None):
    kl = [("Klaster 1\nTop Tier",880,970,"#e06c75"),
          ("Klaster 2\nMng Atas",780,885,"#e09a52"),
          ("Klaster 3\nMenengah",700,790,"#52c97a"),
          ("Klaster 4\nRegional",630,730,"#6c9bd2")]
    fig = go.Figure()
    for lbl,mn,mx,clr in kl:
        r,g,b = int(clr[1:3],16),int(clr[3:5],16),int(clr[5:7],16)
        fig.add_trace(go.Bar(x=[lbl], y=[mx-mn], base=[mn], showlegend=False,
            marker_color=f"rgba({r},{g},{b},.18)", marker_line_color=clr, marker_line_width=2,
            text=[f"{mn}–{mx}"], textposition='inside', textfont=dict(size=10,color=clr)))
    fig.add_hline(y=sw, line_dash="dash", line_color="#9d7be8", line_width=2.5,
        annotation_text=f"  Skor kamu: {sw:.0f}", annotation_font_color="#9d7be8", annotation_font_size=11)
    fig.update_layout(**CTH, barmode='overlay',
        xaxis=dict(gridcolor='#3a4560', tickfont=dict(size=10,color='#b8c4d8')),
        yaxis=dict(range=[500,SKOR_MAX_TPS], gridcolor='#2a3347',
                   title="Rentang Skor Aman", title_font=dict(color='#8a9ab8'), tickfont=dict(size=9,color='#b8c4d8')),
        title=dict(text="Posisi Skor vs Klaster PTN", font=dict(size=13,color='#e8edf5')), height=370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("klaster"))

def ch_ptn(sw, klaster_no, key=None):
    ptn_k = {k:v for k,v in PTN_DATA.items() if v["k"]==klaster_no}
    fig = go.Figure()
    for nm,d in ptn_k.items():
        short = nm.split("(")[0].strip()[:24]
        fig.add_trace(go.Bar(x=[short], y=[d['mx']-d['mn']], base=[d['mn']], showlegend=False,
            marker_color='rgba(108,155,210,.18)', marker_line_color='#6c9bd2', marker_line_width=1.5,
            text=[f"{d['mn']}–{d['mx']}"], textposition='inside', textfont=dict(size=9,color='#e8edf5')))
    fig.add_hline(y=sw, line_dash="dash", line_color="#d4a847", line_width=2,
        annotation_text=f"  Skor kamu: {sw:.0f}", annotation_font_color="#d4a847", annotation_font_size=11)
    fig.update_layout(**CTH, barmode='overlay',
        yaxis=dict(range=[500,SKOR_MAX_TPS], gridcolor='#2a3347',
                   title="Rentang Skor", title_font=dict(color='#8a9ab8'), tickfont=dict(size=9,color='#b8c4d8')),
        xaxis=dict(gridcolor='#3a4560', tickfont=dict(size=9,color='#b8c4d8')),
        title=dict(text=f"PTN Klaster {klaster_no}", font=dict(size=13,color='#e8edf5')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("ptn"))

def ch_psiko(psiko, konsist, stab, key=None):
    cats = ["Kesiapan<br>Mental","Konsistensi<br>Belajar","Stabilitas<br>Mental","Target<br>Ideal"]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=cats[:3], y=[psiko,konsist,stab],
        marker_color=["#6c9bd2","#52c97a","#9d7be8"], marker_line_width=0,
        text=[f"{v:.0f}%" for v in [psiko,konsist,stab]],
        textposition='outside', textfont=dict(size=11,color='#e8edf5')))
    fig.add_hline(y=80, line_dash="dot", line_color="#d4a847", line_width=1.5,
        annotation_text="  Target 80%", annotation_font_color="#d4a847", annotation_font_size=10)
    fig.update_layout(**CTH,
        yaxis=dict(range=[0,110], ticksuffix="%", gridcolor='#2a3347', tickfont=dict(size=9,color='#b8c4d8')),
        xaxis=dict(gridcolor='#3a4560', tickfont=dict(size=10,color='#b8c4d8')),
        title=dict(text="Indikator Psikologis & Konsistensi", font=dict(size=13,color='#e8edf5')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("psiko"))

def ch_progress(r, key=None):
    """Chart progress minggu ke depan"""
    sw   = r["sw"]; mn = r["info"]["mn"]; mx = r["info"]["mx"]
    gap  = abs(r["gap"]) if r["gap"] < 0 else 0
    ppm  = gap/8 + 8
    weeks = list(range(0, 9))
    preds = [min(mx+30, sw + ppm*w) for w in weeks]
    fig = go.Figure()
    fig.add_hrect(y0=mn, y1=mx, fillcolor="rgba(82,201,122,.07)", layer="below",
                  line_width=0, annotation_text="  Zona Aman", annotation_position="top right",
                  annotation_font=dict(color="#52c97a", size=10))
    fig.add_trace(go.Scatter(x=weeks, y=preds, mode='lines+markers+text',
        line=dict(color='#6c9bd2', width=2.5),
        marker=dict(size=8, color='#6c9bd2', line=dict(color='#e8edf5', width=1.5)),
        text=[f"{v:.0f}" for v in preds], textposition='top center',
        textfont=dict(size=9,color='#b8c4d8'), name='Proyeksi Skor'))
    fig.add_trace(go.Scatter(x=[0], y=[sw], mode='markers',
        marker=dict(size=12, color='#d4a847', symbol='star'),
        name=f'Skor Sekarang ({sw:.0f})'))
    fig.add_hline(y=mn, line_dash="dash", line_color="#e09a52", line_width=1.5,
        annotation_text=f"  Minimum ({mn})", annotation_font_color="#e09a52", annotation_font_size=10)
    fig.update_layout(**CTH, margin=dict(l=10,r=10,t=45,b=30),
        xaxis=dict(title="Minggu ke-", tickvals=weeks, gridcolor='#2a3347',
                   title_font=dict(color='#8a9ab8'), tickfont=dict(size=9,color='#b8c4d8')),
        yaxis=dict(range=[max(400,sw-100), min(1000,mx+60)], gridcolor='#2a3347',
                   title="Proyeksi Skor", title_font=dict(color='#8a9ab8'), tickfont=dict(size=9,color='#b8c4d8')),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#b8c4d8')),
        title=dict(text="Proyeksi Skor 8 Minggu ke Depan", font=dict(size=13,color='#e8edf5')), height=340)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("prog"))


# ══════════════════════════════════════════════════════════
# PDF EXPORT
# ══════════════════════════════════════════════════════════
def generate_pdf(r):
    now  = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    nama = r.get("nama","—")
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
    <div style="margin-bottom:12px;padding:10px 14px;background:#f8fafc;border-radius:8px;border-left:3px solid #6c9bd2">
      <div style="font-size:9pt;color:#6c9bd2;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px">
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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Fraunces:wght@700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'DM Sans',sans-serif;font-size:11pt;color:#1e293b;background:#fff;padding:1.2cm 1.8cm}}
h1{{font-family:'Fraunces',serif;font-size:19pt;font-weight:800;color:#0f172a}}
h2{{font-family:'Fraunces',serif;font-size:11.5pt;font-weight:700;color:#0f172a;margin:16px 0 7px;
    border-bottom:2px solid #d4a847;padding-bottom:3px}}
p{{font-size:10pt;line-height:1.65;color:#374151;margin-bottom:5px}}
.hdr{{background:linear-gradient(135deg,#1a1f2e,#1e2a45);color:#fff;padding:1.1cm 1.4cm;
      border-radius:12px;margin-bottom:.9cm}}
.brand{{font-family:'Fraunces',serif;font-size:13pt;font-weight:800;color:#d4a847;margin-bottom:3px}}
.hdr .sub{{color:#8a9ab8;font-size:9pt;margin-top:3px}}
.kpi-row{{display:flex;gap:10px;margin-bottom:10px}}
.kpi{{flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center}}
.kpi .val{{font-size:18pt;font-weight:800;font-family:'Fraunces',serif}}
.kpi .lbl{{font-size:7.5pt;color:#64748b;text-transform:uppercase;letter-spacing:.05em}}
.green{{color:#16a34a}}.orange{{color:#ca8a04}}.red{{color:#dc2626}}.blue{{color:#1d4ed8}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:9px}}
th{{background:#f1f5f9;text-align:left;padding:5px 9px;font-weight:600;border:1px solid #e2e8f0;color:#1e293b}}
td{{padding:5px 9px;border:1px solid #e2e8f0;color:#374151}}
tr:nth-child(even) td{{background:#f8fafc}}
.footer{{margin-top:.8cm;font-size:8pt;color:#94a3b8;text-align:center;border-top:1px solid #e2e8f0;padding-top:7px}}
@media print{{body{{padding:.8cm 1cm}}.no-print{{display:none}}}}
</style></head><body>
<div class="hdr">
  <div class="brand">🎯 SKORIA</div>
  <h1>AI UTBK Readiness Report</h1>
  <div class="sub">Laporan Kesiapan UTBK · {now}</div>
</div>
<h2>👤 Profil Siswa</h2>
<table><tr><th>Nama</th><td>{nama}</td><th>Jurusan Target</th><td>{r['jurusan']}</td></tr>
<tr><th>Kampus Target</th><td>{r['kampus']}</td><th>Klaster</th><td>{r['info']['lbl']}</td></tr></table>
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
<tr><th colspan="2">Total Skor Tertimbang</th><th colspan="2"><strong>{r['sw']:.1f}</strong></th></tr></table>
<h2>🧠 Indikator Psikologis & Kebiasaan</h2>
<table>
<tr><th>Fokus</th><td>{r['fokus']}/5</td><th>Percaya Diri</th><td>{r['pede']}/5</td></tr>
<tr><th>Kecemasan</th><td>{r['cemas']}/5</td><th>Distraksi</th><td>{r['distrak']}/5</td></tr>
<tr><th>Kesiapan Mental</th><td>{r['psiko']:.0f}/100</td><th>Konsistensi</th><td>{r['konsist']:.0f}/100</td></tr>
<tr><th>Stabilitas Mental</th><td>{r['stab']:.0f}/100</td><th>Risiko Underperform</th><td>{r['risk'][0]} {r['risk'][1]}</td></tr></table>
<h2>🎓 Jurusan Alternatif (Formalitas)</h2><p>{alt_list}</p>
<h2>📅 Rencana Belajar Mingguan (8 Minggu)</h2>
{minggu_html}
<div class="footer">🎯 SKORIA — AI UTBK Intelligence · Estimasi berdasarkan data yang diinput · Skor skala 200–1000</div>
<div class="no-print" style="margin-top:16px;text-align:center">
<button onclick="window.print()" style="padding:8px 20px;background:#d4a847;border:none;border-radius:8px;
  font-weight:700;cursor:pointer;font-size:11pt;font-family:'Fraunces',serif;color:#1a1f2e">
  🖨️ Print / Save as PDF</button></div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════════
def render_nav():
    p = st.session_state.page
    def sp(label, pages, step_p=None):
        cls = "done" if (p in pages and p != pages[-1]) else "active" if (p in pages) else ""
        ic  = "✓" if (cls=="done") else ""
        return f'<div class="step-pill {cls}">{ic} {label}</div>'
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
    steps = ["👤 Profil & Target","📊 Skor TPS","🧠 Psikologis","📚 Kebiasaan Belajar"]
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
         yang dipersonalisasi sesuai profil akademik & psikologis kamu. Skor skala 1000.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    feats = [
        ("📡","Radar Chart TPS","Visualisasi 7 subtes vs profil ideal jurusan"),
        ("📊","Bar & Pipeline Chart","Skor subtes + kontribusi tertimbang vs target"),
        ("📅","Rencana Mingguan","Jadwal belajar 8 minggu + target per subtes"),
        ("📄","Export PDF","Laporan lengkap dengan rencana belajar"),
    ]
    for col,(ico,ttl,desc) in zip([c1,c2,c3,c4],feats):
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;padding:1.4rem">
              <div style="font-size:2rem;margin-bottom:.5rem">{ico}</div>
              <div style="font-family:'Fraunces',serif;font-weight:700;font-size:.9rem;
                          margin-bottom:.35rem;color:#e8edf5">{ttl}</div>
              <div style="font-size:.77rem;color:#8a9ab8;line-height:1.55">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">🤖 Tentang SKORIA</div>', unsafe_allow_html=True)
    st.markdown("""<div class="al al-i">
      <h4>SKORIA — Score Intelligence for UTBK</h4>
      Platform SKORIA mengintegrasikan <strong>Model LightGBM</strong> dengan analisis holistik:
      <ul>
        <li>📊 Analisis tertimbang sesuai bobot setiap jurusan target</li>
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
    jurusan = st.selectbox("Target Jurusan", DAFTAR_JURUSAN,
                           index=DAFTAR_JURUSAN.index(d.get("jurusan",DAFTAR_JURUSAN[0])))
    kampus  = st.selectbox("Target Kampus (PTN)", DAFTAR_PTN,
                           index=DAFTAR_PTN.index(d.get("kampus",DAFTAR_PTN[0])))
    st.markdown("---")
    st.markdown(f"<p style='color:#b8c4d8;font-weight:600;font-size:.87rem'>📋 Bobot Subtes untuk <strong style='color:#d4a847'>{jurusan}</strong>:</p>", unsafe_allow_html=True)
    bobot_chips(jurusan)
    info = get_ptn(kampus)
    st.markdown(f"""<div class="al al-i" style="margin-top:.7rem">
      <h4>{info['lbl']} — {kampus}</h4>
      Skor aman: <strong>{info['mn']} – {info['mx']}</strong> (skala 1000, naik +100 dari sebelumnya)
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Lanjut → Skor TPS ▶", type="primary"):
        if not nama.strip(): st.error("Nama harus diisi!"); return
        st.session_state.data.update({"nama":nama,"jurusan":jurusan,"kampus":kampus})
        st.session_state.step=2; st.rerun()

def step2():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Skor TPS (Tes Potensi Skolastik)</h3>', unsafe_allow_html=True)
    st.caption(f"Skala skor: {SKOR_MIN_TPS} – {SKOR_MAX_TPS} · Masukkan skor tryout terbaru")
    d = st.session_state.data
    skor = {}
    pairs = [("PU","PPU"),("PBM","PK"),("LBI","LBE"),("PM",None)]
    for pair in pairs:
        cols = st.columns(2)
        for col, k in zip(cols, pair):
            if k is None: continue
            with col:
                skor[k] = st.slider(f"{SUBTES_FULL[k]} ({k})", SKOR_MIN_TPS, SKOR_MAX_TPS,
                                    d.get(k, 550), step=5, key=f"s_{k}")
    jurusan = d.get("jurusan", DAFTAR_JURUSAN[0])
    bobot   = get_bobot(jurusan)
    # Live radar preview
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES]+[min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal',
        fillcolor='rgba(212,168,71,.06)',line=dict(color='#d4a847',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(108,155,210,.15)',line=dict(color='#6c9bd2',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(35,42,59,.85)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#3a4560',linecolor='#3a4560',tickfont=dict(size=9,color='#8a9ab8')),
        angularaxis=dict(gridcolor='#3a4560',linecolor='#3a4560',tickfont=dict(size=9.5,color='#b8c4d8'))),
        legend=dict(bgcolor='rgba(0,0,0,0)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#b8c4d8')),
        title=dict(text=f"Preview Radar — {jurusan}",font=dict(size=13,color='#e8edf5')),height=380)
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
    pc = "#52c97a" if psiko>=65 else "#d4a847" if psiko>=45 else "#e06c75"
    st.markdown(f"""<div class="card" style="text-align:center;margin-top:.8rem">
      <div class="kpi-lbl">Indeks Kesiapan Mental</div>
      <div class="kpi-val" style="color:{pc}">{psiko:.0f}<span style="font-size:1rem;color:#8a9ab8">/100</span></div>
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
        lat= st.slider("✏️ Latihan soal/minggu (1–5)",1,5,d.get("latihan",3))
    with cb:
        try_= st.slider("📝 Tryout/bulan (1–5)",1,5,d.get("tryout",2))
        rev = st.slider("🔄 Review soal salah/minggu (1–5)",1,5,d.get("review",3))
    jb = mj[js]; hb = mh[hs]
    konsist = min(100,(jb*2+hb*2.2+lat*1.8+try_*1.5+rev*1.5)*2)
    kc = "#52c97a" if konsist>=65 else "#d4a847" if konsist>=45 else "#e06c75"
    st.markdown(f"""<div class="card" style="text-align:center;margin-top:.8rem">
      <div class="kpi-lbl">Indeks Konsistensi Belajar</div>
      <div class="kpi-val" style="color:{kc}">{konsist:.0f}<span style="font-size:1rem;color:#8a9ab8">/100</span></div>
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

    st.markdown(f"""<div class="hero" style="padding:1.8rem 2.5rem">
      <h1 style="font-size:1.6rem!important">{salam}, <span>{nama}!</span> 👋</h1>
      <p>Hasil analisis <strong style="color:#d4a847">SKORIA</strong> untuk 
         <strong style="color:#d4a847">{r['jurusan']}</strong> di 
         <strong style="color:#8bb8e8">{r['kampus']}</strong> · Skor skala 1000</p>
    </div>""", unsafe_allow_html=True)

    # ── KPI Row ──
    gc = "c-green" if r["gap"]>=0 else "c-red"
    pc = "c-green" if r["ppct"]>=65 else "c-orange" if r["ppct"]>=35 else "c-red"
    kc = "c-green" if r["pl"] in ("Sangat Aman","Aman") else "c-orange" if r["pl"]=="Kompetitif" else "c-red"

    k1,k2,k3,k4,k5 = st.columns(5)
    for col,lbl,val,cls,sub in [
        (k1,"Skor Tertimbang",f"{r['sw']:.0f}",kc,f"dari 1000"),
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
            <span style="font-size:.78rem;font-weight:500;color:#8a9ab8"> · Kepercayaan: {kpct}</span></h4>
          <em>{det.get('desc','')}</em>
          <ul style="margin-top:.35rem">{tips}</ul>
        </div>""", unsafe_allow_html=True)

    # ── Status Banner ──
    if r["pl"]=="Sangat Aman":
        st.markdown(f"""<div class="al al-s"><h4>🎯 Status: SANGAT AMAN</h4>
          Skor tertimbang <strong>{r['sw']:.0f}</strong> melampaui batas aman maksimum {r['info']['mx']}.
          Pertahankan performa & jaga kondisi mental.</div>""", unsafe_allow_html=True)
    elif r["pl"]=="Aman":
        st.markdown(f"""<div class="al al-s"><h4>✅ Status: AMAN</h4>
          Skor {r['sw']:.0f} dalam zona aman ({r['info']['mn']}–{r['info']['mx']}).
          Tambah <strong>{r['info']['mx']-r['sw']:.0f} poin</strong> lagi untuk zona sangat aman.</div>""", unsafe_allow_html=True)
    elif r["pl"]=="Kompetitif":
        st.markdown(f"""<div class="al al-w"><h4>⚡ Status: KOMPETITIF</h4>
          Butuh <strong>+{r['info']['mn']-r['sw']:.0f} poin</strong> untuk zona aman. Intensifkan latihan.</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="al al-d"><h4>🔴 Status: PERLU PENINGKATAN</h4>
          Gap <strong>{abs(r['gap']):.0f} poin</strong> dari minimum. Pertimbangkan bimbingan intensif.</div>""", unsafe_allow_html=True)

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
        st.markdown('<div class="sec">📊 Bar Chart Skor Per Subtes vs Target Kampus</div>', unsafe_allow_html=True)
        ch_bar_subtes(r["skor"],r["bobot"],r["info"], key="r_bar_t1")
        st.markdown('<div class="sec">📋 Tabel Detail Subtes</div>', unsafe_allow_html=True)
        df = pd.DataFrame([{
            "Subtes":SUBTES_FULL[k],"Bobot":f"{r['bobot'][k]*100:.0f}%",
            "Skor":r["skor"][k],
            "Kontribusi":f"{r['skor'][k]*r['bobot'][k]:.1f}",
            "Gap vs Target":f"{r['skor'][k]-(r['info']['mn']+r['info']['mx'])/2*r['bobot'][k]*7:+.0f}",
            "Status":"✅ Kuat" if r["skor"][k]>=750 else "⚡ Sedang" if r["skor"][k]>=550 else "🔴 Lemah",
        } for k in SUBTES])
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ─── TAB 2: ANALISIS KAMPUS ───
    with t2:
        st.markdown('<div class="sec">📊 Posisi Skor vs Klaster PTN</div>', unsafe_allow_html=True)
        ch_klaster(r["sw"], key="r_kl_t2")
        st.markdown(f'<div class="sec">🏛️ PTN Klaster {r["info"]["k"]} — Detail</div>', unsafe_allow_html=True)
        ch_ptn(r["sw"], r["info"]["k"], key="r_ptn_t2")
        st.markdown('<div class="sec">📋 Perbandingan Semua Klaster</div>', unsafe_allow_html=True)
        kl_rows = []
        for kno,(mn,mx,knm) in [(1,(880,970,"⭐ Klaster 1 — Top Tier")),
                                  (2,(780,885,"🔷 Klaster 2 — Menengah Atas")),
                                  (3,(700,790,"🔹 Klaster 3 — Menengah")),
                                  (4,(630,730,"🔸 Klaster 4 — Regional"))]:
            g=r["sw"]-mn
            if r["sw"]>=mx: st_k,p_k="🎯 Sangat Aman","~87%"
            elif r["sw"]>=mn: st_k,p_k="✅ Aman","~72%"
            elif r["sw"]>=mn-70: st_k,p_k="⚡ Kompetitif","~42%"
            else: st_k,p_k="🔴 Berisiko","~16%"
            kl_rows.append({"Klaster":knm,"Rentang Skor":f"{mn}–{mx}",
                             "Skor Kamu":f"{r['sw']:.0f}","Gap":f"{g:+.0f}",
                             "Status":st_k,"Est. Peluang":p_k})
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
        st.markdown(f'<div class="sec">📐 Distribusi Bobot — {r["jurusan"]}</div>', unsafe_allow_html=True)
        ch_bobot(r["jurusan"], key="r_bobot_t3")
        st.markdown('<div class="sec">📋 Tabel Bobot & Kontribusi</div>', unsafe_allow_html=True)
        df_b = pd.DataFrame([{
            "Subtes":SUBTES_FULL[k],"Bobot":f"{r['bobot'][k]*100:.0f}%","Skor":r["skor"][k],
            "Kontribusi Aktual":f"{r['skor'][k]*r['bobot'][k]:.1f}",
            "Target Minimum":f"{r['info']['mn']*r['bobot'][k]:.1f}",
            "Selisih":f"{(r['skor'][k]-r['info']['mn'])*r['bobot'][k]:+.1f}",
        } for k in SUBTES]+[{"Subtes":"TOTAL","Bobot":"100%","Skor":"—",
            "Kontribusi Aktual":f"{r['sw']:.1f}","Target Minimum":f"{r['info']['mn']:.0f}",
            "Selisih":f"{r['gap']:+.1f}"}])
        st.dataframe(df_b, use_container_width=True, hide_index=True)
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
            # Skor aman → fokus ke jurusan target
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
                st.markdown("<p style='color:#b8c4d8;font-weight:600;margin-bottom:.8rem'>📈 Indikator Kesiapan:</p>", unsafe_allow_html=True)
                prog_bar("Kesiapan Mental",r["psiko"],"#6c9bd2")
                prog_bar("Konsistensi Belajar",r["konsist"],"#52c97a")
                prog_bar("Stabilitas Mental",r["stab"],"#9d7be8")
            # Subtes kunci
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
            # Alternatif hanya formalitas
            st.markdown('<div class="sec">📋 Jurusan Alternatif (Hanya Formalitas)</div>', unsafe_allow_html=True)
            st.markdown('<div class="al al-i"><h4>ℹ️ Info</h4>Skor kamu sudah aman. Alternatif ini hanya cadangan formalitas.</div>', unsafe_allow_html=True)
            alt = r["alternatif"]
            if alt:
                ac = st.columns(len(alt))
                for col,j in zip(ac,alt):
                    with col:
                        st.markdown(f"""<div class="card" style="text-align:center;opacity:.55">
                          <div style="font-size:.7rem;color:#8a9ab8">Formalitas</div>
                          <div style="font-weight:700;font-size:.87rem;margin:.25rem 0;color:#b8c4d8">{j}</div>
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
                plj,_,pctj = hitung_peluang(swj, r["kampus"])
                with st.expander(f"📚 {j}  —  Skor: {swj:.0f}  |  {plj}"):
                    ca2,cb2 = st.columns(2)
                    with ca2:
                        st.metric("Skor Tertimbang",f"{swj:.0f}")
                        st.metric("Peluang",f"{pctj:.0f}% ({plj})")
                        bobot_chips(j)
                    with cb2:
                        ch_bobot(j, key=f"r_bobot_alt_{idx}")

    # ─── TAB 5: STRATEGI ───
    with t5:
        st.markdown('<div class="sec">🚀 Strategi Belajar Personal</div>', unsafe_allow_html=True)
        ch_psiko(r["psiko"],r["konsist"],r["stab"], key="r_psiko_t5")
        prog_bar("Kesiapan Mental",r["psiko"],"#6c9bd2")
        prog_bar("Konsistensi Belajar",r["konsist"],"#52c97a")
        prog_bar("Stabilitas Mental",r["stab"],"#9d7be8")
        st.markdown('<div class="sec">📌 Prioritas Subtes</div>', unsafe_allow_html=True)
        ss = sorted(r["skor"].items(),key=lambda x:x[1])
        lemah3 = ss[:3]; kuat2 = ss[-2:]
        cp1,cp2 = st.columns(2)
        with cp1:
            il = "".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} → +{max(0,750-v)} poin dibutuhkan</li>" for k,v in lemah3)
            st.markdown(f'<div class="al al-d"><h4>🔴 3 Subtes Terlemah (Prioritas)</h4><ul>{il}</ul></div>',unsafe_allow_html=True)
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
        st.markdown('<div class="sec">📅 Proyeksi & Rencana Belajar 8 Minggu</div>', unsafe_allow_html=True)
        ch_progress(r, key="r_prog_t6")
        st.markdown('<div class="sec">📋 Detail Rencana Per Minggu</div>', unsafe_allow_html=True)
        rencana = buat_rencana_mingguan(r, 8)
        fase_clr = {"Fondasi":"#6c9bd2","Intensif":"#e09a52","Pemantapan":"#52c97a","Final":"#d4a847"}
        for m in rencana:
            clr = fase_clr.get(m["fase"],"#9d7be8")
            tasks_html = "".join(f'<div style="padding:.1rem 0;color:#b8c4d8">• {t}</div>' for t in m["tasks"])
            st.markdown(f"""<div class="week-card">
              <div class="week-num" style="color:{clr}">MINGGU {m['minggu']} — {m['fase'].upper()}</div>
              <div class="week-target" style="color:#e8edf5">
                🎯 Target skor: <strong style="color:{clr}">{m['target_skor']}</strong> &nbsp;|&nbsp; ⏰ {m['jam']}
              </div>
              <div class="week-tasks">{tasks_html}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">📊 Tabel Ringkasan Rencana</div>', unsafe_allow_html=True)
        df_r = pd.DataFrame([{"Minggu":m["minggu"],"Fase":m["fase"],
                               "Target Skor":m["target_skor"],"Durasi":m["jam"],
                               "Fokus Utama":m["fokus"]} for m in rencana])
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
              style="display:inline-block;background:linear-gradient(135deg,#d4a847,#c9962e);
                     color:#1a1f2e;font-weight:700;padding:.6rem 1.4rem;border-radius:10px;
                     text-decoration:none;font-family:'Fraunces',serif;font-size:.9rem;margin-top:.5rem">
              ⬇️ Download {fn}</a>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">👁️ Preview Ringkasan</div>', unsafe_allow_html=True)
        pp1,pp2 = st.columns(2)
        with pp1:
            st.markdown(f"""| Info | Detail |
|---|---|
| Nama | {r.get('nama','—')} |
| Jurusan | {r['jurusan']} |
| Kampus | {r['kampus']} |
| Klaster | {r['info']['lbl']} |
| Skor Tertimbang | {r['sw']:.0f} / 1000 |
| Gap | {r['gap']:+.0f} |""")
        with pp2:
            st.markdown(f"""| Indikator | Nilai |
|---|---|
| Peluang Lolos | {r['ppct']:.0f}% ({r['pl']}) |
| Kesiapan Mental | {r['psiko']:.0f}/100 |
| Konsistensi | {r['konsist']:.0f}/100 |
| Stabilitas | {r['stab']:.0f}/100 |
| Risiko | {r['risk'][0]} {r['risk'][1]} |""")

    # ── Footer ──
    st.divider()
    nb1,nb2,_ = st.columns([1,1,4])
    with nb1:
        if st.button("◀ Ubah Data"): st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with nb2:
        if st.button("🏠 Beranda"): st.session_state.page="home"; st.rerun()

    st.markdown(f"""<div style="text-align:center;padding:1.4rem;background:var(--surf);
      border-radius:var(--r);border:1px solid var(--border);margin-top:.8rem">
      <div style="font-family:'Fraunces',serif;font-size:1.1rem;font-weight:800;color:#fff">
        💪 {nama}, kamu pasti bisa!
      </div>
      <div style="color:#8a9ab8;font-size:.82rem;margin-top:.3rem">
        Konsistensi + strategi tepat = PTN impianmu pasti bisa diraih 🚀
      </div>
      <div style="color:#3a4560;font-size:.7rem;margin-top:.35rem">
        🎯 SKORIA — AI UTBK Intelligence · LightGBM + Analisis Holistik · Skor skala 200–1000
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
