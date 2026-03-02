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
    page_title="Skoolnow AI — AI UTBK",
    page_icon="data:image/png;base64,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",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════
# GLOBAL CSS — Animated Design System v4.2
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');

:root {
  --bg:      #f0f4fa;
  --surf:    #ffffff;
  --surf2:   #f7f9fd;
  --border:  #e0e8f4;
  --accent:  #3464c8;
  --a2:      #5080e0;
  --gold:    #d4900a;
  --green:   #148a42;
  --red:     #c0392b;
  --orange:  #d4620a;
  --purple:  #6b3fca;
  --teal:    #0d8a80;
  --text:    #12203f;
  --text2:   #334466;
  --text3:   #6a7a9a;
  --r:       12px;
  --sh:      0 2px 12px rgba(30,60,140,.08);
  --sh2:     0 8px 32px rgba(30,60,140,.15);
}

@keyframes fadeSlideUp {
  from { opacity:0; transform:translateY(30px) scale(.97); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes fadeSlideLeft {
  from { opacity:0; transform:translateX(-24px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes fadeSlideRight {
  from { opacity:0; transform:translateX(24px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes popIn {
  0%   { opacity:0; transform:scale(.5) rotate(-8deg); }
  65%  { opacity:1; transform:scale(1.1) rotate(3deg); }
  85%  { transform:scale(.96) rotate(-1deg); }
  100% { transform:scale(1) rotate(0); }
}
@keyframes pulseRing {
  0%,100% { box-shadow: 0 0 0 0 rgba(52,100,200,.35); }
  50%      { box-shadow: 0 0 0 10px rgba(52,100,200,0); }
}
@keyframes orb {
  0%,100% { transform:scale(1) translate(0,0); opacity:.08; }
  40%      { transform:scale(1.18) translate(15px,-12px); opacity:.14; }
  70%      { transform:scale(.88) translate(-10px,14px); opacity:.04; }
}
@keyframes float {
  0%,100% { transform:translateY(0px); }
  50%      { transform:translateY(-8px); }
}
@keyframes shimmer {
  from { background-position:-600px 0; }
  to   { background-position:600px 0; }
}
@keyframes progressGrow {
  from { width:0 !important; opacity:.4; }
}
@keyframes gradientFlow {
  0%,100% { background-position:0% 50%; }
  50%      { background-position:100% 50%; }
}
@keyframes ticker {
  from { transform:translateX(0); }
  to   { transform:translateX(-50%); }
}
@keyframes countUp {
  from { opacity:0; transform:translateY(14px) scale(.8); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes borderTrail {
  0%   { clip-path:inset(0 100% 0 0); }
  100% { clip-path:inset(0 0% 0 0); }
}
@keyframes starSpin {
  0%   { opacity:0; transform:rotate(-30deg) scale(0); }
  60%  { opacity:1; transform:rotate(10deg) scale(1.2); }
  100% { opacity:1; transform:rotate(0) scale(1); }
}
@keyframes typeBar { from { width:0; } }

html,body,[class*="css"],.stApp {
  background: var(--bg) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: var(--text) !important;
}
#MainMenu, footer, header { visibility:hidden }
.stDeployButton { display:none }
.block-container { padding:1rem 1.5rem !important; max-width:100% !important; }
.main .block-container { animation: fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both; }

.topbar {
  background:#fff; border-bottom:2px solid var(--border);
  padding:.6rem 2rem; display:flex; align-items:center; gap:1.2rem;
  margin:-1rem -1.5rem 1.5rem -1.5rem;
  position:sticky; top:0; z-index:999;
  box-shadow:0 2px 12px rgba(30,60,140,.07);
  animation:fadeSlideLeft .4s ease both;
}
.topbar-brand {
  font-family:'Space Grotesk',sans-serif;
  font-size:1.1rem; font-weight:800; color:var(--accent) !important;
  display:flex; align-items:center; gap:.5rem;
  animation:float 4s ease-in-out infinite;
}
.topbar-tag { font-size:.68rem; color:var(--text3); letter-spacing:.04em; }
.step-pill {
  font-size:.72rem; font-weight:600; padding:.26rem .8rem; border-radius:99px;
  color:var(--text3); background:var(--surf2); border:1px solid var(--border);
  transition:all .3s ease;
}
.step-pill.done  { background:#e6f5ee; color:var(--green); border-color:#9adbb8; animation:popIn .5s ease both; }
.step-pill.active{ background:#eef2fc; color:var(--accent); border-color:#aac0f0; animation:pulseRing 2.5s ease-in-out infinite; }

.hero {
  background:linear-gradient(135deg,#1a3470 0%,#3464c8 55%,#2a50a8 100%);
  border-radius:16px; padding:2.4rem 3rem; margin-bottom:1.8rem;
  position:relative; overflow:hidden;
  box-shadow:0 6px 32px rgba(30,60,180,.22);
  animation:fadeSlideUp .65s cubic-bezier(.22,.68,0,1.2) both;
}
.hero::before {
  content:''; position:absolute; top:-70px; right:-70px;
  width:320px; height:320px; border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.12) 0%,transparent 65%);
  animation:orb 7s ease-in-out infinite;
}
.hero::after {
  content:''; position:absolute; bottom:-90px; left:8%;
  width:240px; height:240px; border-radius:50%;
  background:radial-gradient(circle,rgba(255,209,102,.09) 0%,transparent 65%);
  animation:orb 9s ease-in-out infinite reverse;
}
.hero h1 {
  font-family:'Space Grotesk',sans-serif !important;
  font-size:2rem !important; font-weight:800 !important;
  color:#fff !important; margin:0 0 .6rem !important;
  animation:fadeSlideLeft .7s cubic-bezier(.22,.68,0,1.2) .1s both;
}
.hero h1 span { color:#ffd166; }
.hero p {
  color:rgba(255,255,255,.82) !important; font-size:.95rem; margin:0; line-height:1.7;
  animation:fadeSlideUp .7s ease .2s both;
}
.hero-badge {
  display:inline-flex; align-items:center; gap:.4rem;
  background:rgba(255,255,255,.12); backdrop-filter:blur(4px);
  border:1px solid rgba(255,255,255,.2);
  padding:.3rem .85rem; border-radius:99px;
  font-size:.72rem; font-weight:600; color:rgba(255,255,255,.9);
  margin-bottom:1rem; animation:fadeSlideLeft .5s ease .05s both;
}

.anim-div {
  height:2px; border-radius:99px; margin:1.2rem 0;
  background:linear-gradient(90deg,var(--accent),var(--purple),var(--teal),var(--gold),var(--accent));
  background-size:300% auto; animation:gradientFlow 4s linear infinite;
}

.ticker-wrap {
  overflow:hidden; white-space:nowrap;
  background:linear-gradient(90deg,#eef2fc,#f2eeff,#eef6fc);
  background-size:200% auto; animation:gradientFlow 6s linear infinite;
  border:1px solid var(--border); border-radius:10px;
  padding:.5rem 0; margin-bottom:1.3rem;
}
.ticker-inner { display:inline-block; animation:ticker 28s linear infinite; }
.ticker-item { display:inline-block; padding:0 2.8rem; font-size:.8rem; font-weight:600; color:var(--text2); }
.ticker-item span { color:var(--accent); font-family:'Space Grotesk',sans-serif; font-weight:700; }

.feat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.4rem; }
.feat-card {
  background:var(--surf); border:1px solid var(--border); border-radius:14px;
  padding:1.6rem 1.2rem; text-align:center; box-shadow:var(--sh);
  transition:all .32s cubic-bezier(.22,.68,0,1.2);
  position:relative; overflow:hidden; animation:fadeSlideUp .5s ease both;
}
.feat-card:hover { transform:translateY(-8px) scale(1.02); box-shadow:var(--sh2); }
.feat-icon { font-size:2.2rem; margin-bottom:.6rem; display:block; animation:float 3.2s ease-in-out infinite; }
.feat-card:nth-child(2) .feat-icon { animation-delay:.3s; }
.feat-card:nth-child(3) .feat-icon { animation-delay:.6s; }
.feat-card:nth-child(4) .feat-icon { animation-delay:.9s; }
.feat-title { font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:.9rem; color:var(--text); margin-bottom:.35rem; }
.feat-desc { font-size:.76rem; color:var(--text3); line-height:1.6; }

.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.8rem; margin-bottom:1.4rem; }
.stat-box {
  background:linear-gradient(135deg,var(--accent),var(--purple));
  border-radius:12px; padding:1.1rem 1rem; text-align:center;
  box-shadow:0 4px 16px rgba(52,100,200,.25); animation:popIn .6s ease both;
}
.stat-box:nth-child(2) { background:linear-gradient(135deg,var(--purple),var(--teal)); animation-delay:.1s; }
.stat-box:nth-child(3) { background:linear-gradient(135deg,var(--teal),var(--green)); animation-delay:.2s; }
.stat-box:nth-child(4) { background:linear-gradient(135deg,var(--gold),var(--orange)); animation-delay:.3s; }
.stat-num { font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:800; color:#fff; animation:countUp .8s cubic-bezier(.22,.68,0,1.2) .4s both; }
.stat-lbl { font-size:.72rem; color:rgba(255,255,255,.82); font-weight:600; margin-top:.15rem; }

.step-row {
  display:flex; margin-bottom:1.8rem; background:var(--surf); border:1px solid var(--border);
  border-radius:var(--r); overflow:hidden; box-shadow:var(--sh); animation:fadeSlideUp .45s ease .05s both;
}
.step-item {
  flex:1; padding:.9rem; text-align:center; font-size:.73rem; font-weight:600; color:var(--text3);
  border-right:1px solid var(--border); transition:background .4s ease, color .3s ease;
}
.step-item:last-child { border-right:none; }
.step-item.active { background:linear-gradient(135deg,#eef2fc,#e8f0ff); color:var(--accent); animation:pulseRing 2.5s ease-in-out infinite; }
.step-item.done { background:#e8f5ee; color:var(--green); }
.step-item.done .step-num { animation:starSpin .5s ease both; }
.step-num { display:block; font-size:1.15rem; font-family:'Space Grotesk',sans-serif; font-weight:800; margin-bottom:1px; }

.form-box {
  background:var(--surf); border:1px solid var(--border); border-radius:var(--r);
  padding:1.8rem 2rem; margin-bottom:1.2rem; box-shadow:var(--sh);
  animation:fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both;
  transition:border-color .3s ease, box-shadow .3s ease;
  position:relative; overflow:hidden;
}
.form-box::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg,var(--accent),var(--purple));
  animation:borderTrail .8s ease .2s both;
}
.form-box:focus-within { border-color:var(--a2); box-shadow:0 4px 20px rgba(52,100,200,.12); }
.form-box h3 { font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:700; color:var(--accent); margin:0 0 1.2rem; animation:fadeSlideLeft .5s ease both; }

.sec {
  font-family:'Space Grotesk',sans-serif; font-size:.94rem; font-weight:700; color:var(--text);
  margin:1.6rem 0 .75rem; padding-bottom:.35rem; border-bottom:2px solid var(--border);
  animation:fadeSlideLeft .4s ease both; position:relative;
}
.sec::after {
  content:''; position:absolute; bottom:-2px; left:0; height:2px;
  background:linear-gradient(90deg,var(--accent),var(--a2)); animation:typeBar .7s ease .2s both;
}

.card {
  background:var(--surf); border:1px solid var(--border); border-radius:var(--r);
  padding:1.2rem 1.4rem; box-shadow:var(--sh);
  transition:transform .28s ease, box-shadow .28s ease; animation:fadeSlideUp .5s ease both;
}
.card:hover { transform:translateY(-4px); box-shadow:var(--sh2); }
.kpi-lbl { font-size:.67rem; font-weight:700; text-transform:uppercase; letter-spacing:.1em; color:var(--text3); margin-bottom:.3rem; }
.kpi-val { font-family:'Space Grotesk',sans-serif; font-size:1.9rem; font-weight:800; line-height:1; animation:countUp .6s cubic-bezier(.22,.68,0,1.2) .2s both; }
.kpi-sub { font-size:.71rem; color:var(--text3); margin-top:.2rem; }

.c-gold   { color:var(--gold)!important; }
.c-green  { color:var(--green)!important; }
.c-red    { color:var(--red)!important; }
.c-orange { color:var(--orange)!important; }
.c-blue   { color:var(--a2)!important; }
.c-purple { color:var(--purple)!important; }
.c-teal   { color:var(--teal)!important; }

.al {
  border-radius:var(--r); padding:1rem 1.3rem; margin-bottom:.9rem;
  border-left:4px solid; font-size:.86rem; line-height:1.75; color:var(--text2);
  box-shadow:var(--sh); animation:fadeSlideRight .45s cubic-bezier(.22,.68,0,1.2) both;
  transition:transform .22s ease, box-shadow .22s ease;
}
.al:hover { transform:translateX(5px); box-shadow:var(--sh2); }
.al h4 { margin:0 0 .4rem; font-size:.9rem; font-weight:700; }
.al ul { margin:.35rem 0 0; padding-left:1.3rem; }
.al li { margin-bottom:.22rem; }
.al strong { color:var(--text); }
.al-s  { background:#edfbf3; border-color:var(--green); }  .al-s h4 { color:var(--green); }
.al-w  { background:#fff7ee; border-color:var(--orange); } .al-w h4 { color:var(--orange); }
.al-d  { background:#fff0f0; border-color:var(--red); }    .al-d h4 { color:var(--red); }
.al-i  { background:#eef2fc; border-color:var(--accent); } .al-i h4 { color:var(--accent); }
.al-p  { background:#f3eeff; border-color:var(--purple); } .al-p h4 { color:var(--purple); }
.al-na { background:#ffe8e8; border-color:#c0392b; }       .al-na h4 { color:#c0392b; }
.al-br { background:#fff3e0; border-color:#e67e22; }       .al-br h4 { color:#e67e22; }

/* ── 4 STATUS KATEGORI BADGE ── */
.badge-sa  { background:#e6f5ee; color:#148a42; border:1.5px solid #9adbb8; }
.badge-a   { background:#edf6ff; color:#1a5fa0; border:1.5px solid #90c0f0; }
.badge-br  { background:#fff4e6; color:#d4620a; border:1.5px solid #f4c08a; }
.badge-na  { background:#fff0f0; color:#c0392b; border:1.5px solid #f4a0a0; }

.prog-wrap { margin-bottom:.75rem; }
.prog-lbl { display:flex; justify-content:space-between; font-size:.79rem; font-weight:600; color:var(--text2); margin-bottom:5px; }
.prog-bg { background:var(--surf2); border-radius:99px; height:10px; overflow:hidden; border:1px solid var(--border); }
.prog-fill { height:100%; border-radius:99px; animation:progressGrow .9s cubic-bezier(.22,.68,0,1.2) .3s both; position:relative; overflow:hidden; }
.prog-fill::after {
  content:''; position:absolute; inset:0;
  background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.45) 50%,transparent 100%);
  background-size:200% 100%; animation:shimmer 2s ease 1.4s infinite;
}

.bobot-chip {
  display:inline-flex; flex-direction:column; align-items:center;
  background:#eef2fc; border:1px solid #b8cff0; border-radius:8px; padding:.4rem .65rem; margin:.12rem;
  transition:transform .22s ease, background .22s ease; animation:popIn .5s ease both;
}
.bobot-chip:hover { transform:scale(1.12) translateY(-2px); background:#dde8f8; }
.bobot-chip .sk { font-size:.62rem; color:var(--text3); margin-bottom:2px; }
.bobot-chip .bv { font-size:.96rem; font-weight:800; color:var(--accent); font-family:'Space Grotesk',sans-serif; }

.week-card {
  background:var(--surf); border:1px solid var(--border); border-radius:12px;
  padding:1rem 1.2rem; margin-bottom:.65rem; box-shadow:var(--sh);
  transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease;
  animation:fadeSlideUp .5s ease both; border-left:4px solid transparent;
}
.week-card:hover { transform:translateX(8px); border-left-color:var(--accent); box-shadow:var(--sh2); }
.week-num { font-family:'Space Grotesk',sans-serif; font-size:.72rem; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:.1em; margin-bottom:.28rem; }
.week-target { font-size:.84rem; font-weight:700; color:var(--text); margin-bottom:.24rem; }
.week-tasks { font-size:.79rem; color:var(--text2); line-height:1.68; }

.status-badge { display:inline-flex; align-items:center; gap:.45rem; padding:.42rem 1.1rem; border-radius:99px; font-size:.78rem; font-weight:700; animation:popIn .6s ease both; }

.score-ring-wrap { display:flex; justify-content:center; padding:1rem 0; }
.score-ring {
  width:148px; height:148px; border-radius:50%;
  background:conic-gradient(var(--accent) var(--pct,0%), #e8eef8 var(--pct,0%));
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  position:relative; animation:popIn .8s cubic-bezier(.22,.68,0,1.2) .1s both;
  box-shadow:0 4px 24px rgba(52,100,200,.2);
}
.score-ring::before { content:''; position:absolute; inset:13px; border-radius:50%; background:var(--surf); box-shadow:inset 0 2px 10px rgba(52,100,200,.08); }
.score-ring-val { position:relative; z-index:1; font-family:'Space Grotesk',sans-serif; font-size:1.65rem; font-weight:800; color:var(--accent); animation:countUp .9s ease .5s both; }
.score-ring-sub { position:relative; z-index:1; font-size:.62rem; color:var(--text3); }

/* 4-level skor gauge */
.skor-legend {
  display:flex; gap:.5rem; flex-wrap:wrap; margin:.6rem 0;
}
.skor-legend-item {
  display:inline-flex; align-items:center; gap:.35rem;
  padding:.25rem .65rem; border-radius:99px; font-size:.72rem; font-weight:700;
}
.sl-na  { background:#fff0f0; color:#c0392b; border:1.5px solid #f4a0a0; }
.sl-br  { background:#fff4e6; color:#e67e22; border:1.5px solid #f4c08a; }
.sl-a   { background:#edf6ff; color:#1a5fa0; border:1.5px solid #90c0f0; }
.sl-sa  { background:#e6f5ee; color:#148a42; border:1.5px solid #9adbb8; }

/* ── FITUR PANEL ── */
.fitur-panel {
  background:var(--surf); border:1.5px solid var(--border); border-radius:16px;
  padding:1.8rem 2rem; margin-bottom:1.6rem; box-shadow:var(--sh);
  animation:fadeSlideUp .6s ease both;
  position:relative; overflow:hidden;
}
.fitur-panel::before {
  content:''; position:absolute; top:0; left:0; right:0; height:4px;
  background:linear-gradient(90deg,var(--accent),var(--purple),var(--teal));
  animation:gradientFlow 4s linear infinite; background-size:300% auto;
}
.fitur-panel-title {
  font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:800;
  color:var(--text); margin-bottom:1.1rem; display:flex; align-items:center; gap:.5rem;
}
.fitur-grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:.9rem; }
.fitur-item {
  background:var(--surf2); border:1px solid var(--border); border-radius:12px;
  padding:1rem 1.1rem; transition:all .25s ease; animation:fadeSlideUp .5s ease both;
}
.fitur-item:hover { background:#eef2fc; border-color:var(--a2); transform:translateY(-3px); box-shadow:var(--sh2); }
.fitur-item-icon { font-size:1.6rem; margin-bottom:.4rem; display:block; }
.fitur-item-title { font-family:'Space Grotesk',sans-serif; font-size:.82rem; font-weight:700; color:var(--text); margin-bottom:.3rem; }
.fitur-item-desc { font-size:.73rem; color:var(--text3); line-height:1.6; }

div[data-testid="stButton"] button[kind="primary"] {
  background:linear-gradient(135deg,var(--accent),#1a3470) !important;
  color:#fff !important; font-weight:700 !important; font-family:'Space Grotesk',sans-serif !important;
  border:none !important; border-radius:10px !important; font-size:.89rem !important;
  letter-spacing:.02em !important; transition:all .28s cubic-bezier(.22,.68,0,1.2) !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
  transform:translateY(-3px) scale(1.02) !important;
  box-shadow:0 8px 28px rgba(52,100,200,.4) !important;
}
div[data-testid="stButton"] button {
  background:var(--surf) !important; color:var(--text2) !important;
  border:1px solid var(--border) !important; border-radius:10px !important;
  font-weight:600 !important; transition:all .22s ease !important;
}
div[data-testid="stButton"] button:hover {
  border-color:var(--a2) !important; color:var(--accent) !important;
  transform:translateY(-2px) !important; box-shadow:0 4px 14px rgba(52,100,200,.15) !important;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] { font-family:'Space Grotesk',sans-serif !important; font-weight:700 !important; font-size:.79rem !important; color:var(--text3) !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:var(--accent) !important; border-bottom-color:var(--accent) !important; }
div[data-testid="stMetric"] { background:var(--surf) !important; border:1px solid var(--border) !important; border-radius:var(--r) !important; padding:1.1rem 1.3rem !important; box-shadow:var(--sh) !important; }
div[data-testid="stMetric"]:hover { transform:translateY(-4px) !important; box-shadow:var(--sh2) !important; }
div[data-testid="stMetric"] label { color:var(--text3) !important; font-size:.7rem !important; font-weight:700 !important; text-transform:uppercase !important; letter-spacing:.08em !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:var(--text) !important; font-family:'Space Grotesk',sans-serif !important; }
div[data-testid="stExpander"] { background:var(--surf) !important; border:1px solid var(--border) !important; border-radius:var(--r) !important; box-shadow:var(--sh) !important; }
div[data-testid="stExpander"]:hover { border-color:var(--a2) !important; }
div[data-testid="stExpander"] summary { color:var(--text2) !important; font-weight:700 !important; }
div[data-testid="stNumberInput"] label,div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,div[data-testid="stRadio"] label { color:var(--text2) !important; font-weight:700 !important; font-size:.83rem !important; }
div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input { background:var(--surf) !important; color:var(--text) !important; border-color:var(--border) !important; font-size:.9rem !important; border-radius:8px !important; }
div[data-testid="stNumberInput"] input:focus,div[data-testid="stTextInput"] input:focus { border-color:var(--a2) !important; box-shadow:0 0 0 3px rgba(52,100,200,.14) !important; }
div[data-baseweb="select"] { background:var(--surf) !important; }
div[data-baseweb="select"] * { color:var(--text) !important; }
hr { border-color:var(--border) !important; margin:1.2rem 0 !important; }
div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; box-shadow:var(--sh); }
table { border-collapse:collapse; width:100%; font-size:.84rem; }
th { background:#eef2fc; color:var(--text); padding:.55rem .9rem; border:1px solid var(--border); font-weight:700; text-align:left; }
td { padding:.5rem .9rem; border:1px solid var(--border); color:var(--text2); }
tr:nth-child(even) td { background:#f8faff; }
tr:hover td { background:#eef2fc !important; }

.d1{animation-delay:.05s!important} .d2{animation-delay:.10s!important}
.d3{animation-delay:.15s!important} .d4{animation-delay:.20s!important}
.d5{animation-delay:.25s!important} .d6{animation-delay:.30s!important}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
DEFAULTS = {'page':'home','step':1,'data':{},'result':None,'_cid':0}
for k,v in DEFAULTS.items():
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

SUBTES = ["PU","PPU","PBM","PK","LBI","LBE","PM"]
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
    "PU":"#c8890a","PPU":"#3b6cb7","PBM":"#7048c8",
    "PK":"#c0392b","LBI":"#1a8a4a","LBE":"#0d8a80","PM":"#d4620a",
}

DAFTAR_JENJANG = ["S1 (Sarjana)", "D4 (Sarjana Terapan)", "D3 (Diploma Tiga)"]

# ══════════════════════════════════════════════════════════
# LOAD DATA DARI XLSX
# ══════════════════════════════════════════════════════════
URL_S1  = "https://raw.githubusercontent.com/Skoriaid/skoria-data/main/UTBK_SNBT_Estimasi_30PTN.xlsx"
URL_D34 = "https://raw.githubusercontent.com/Skoriaid/skoria-data/main/UTBK_SNBT_D3_D4_SaintekSoshum_30PTN.xlsx"
LOCAL_S1  = "UTBK_SNBT_Estimasi_30PTN.xlsx"
LOCAL_D34 = "UTBK_SNBT_D3_D4_SaintekSoshum_30PTN.xlsx"

def parse_rentang(r):
    for sep in ['–', '-']:
        try:
            parts = str(r).split(sep)
            if len(parts) == 2:
                mn = int(parts[0].strip())
                mx = int(parts[1].strip())
                return mn, mx
        except:
            pass
    return None, None

# ── FILTER: hanya PTN (Perguruan Tinggi Negeri) ──
_PTN_KEYWORDS_POSITIF = [
    "negeri", "institut teknologi", "institut pertanian",
    "universitas indonesia", "universitas gadjah mada",
    "universitas airlangga", "universitas padjadjaran",
    "universitas diponegoro", "universitas brawijaya",
    "universitas sebelas maret", "universitas hasanuddin",
    "universitas sumatera utara", "universitas andalas",
    "universitas sriwijaya", "universitas udayana",
    "universitas riau", "universitas jember",
    "universitas mulawarman", "universitas syiah kuala",
    "universitas sam ratulangi", "universitas lampung",
    "politeknik negeri", "politeknik elektronika negeri",
    "politeknik perkapalan negeri", "politeknik manufaktur negeri",
]
_PTS_KEYWORDS_NEGATIF = [
    "swasta", "amikom", "bina nusantara", "mercu buana",
    "trisakti", "pelita harapan", "atma jaya", "unika",
    "unpas", "untar", "unisba", "ums ", "umy ", "unissula",
    "uib ", "uii ", "umm ", "umsu", "prasetiya mulya",
    "ciputra", "widyatama", "stmik", "stikes", "sekolah tinggi",
    "akademi ", "itb-stei",
]

def is_ptn(nama: str) -> bool:
    """Kembalikan True jika nama kampus terindikasi PTN (bukan PTS)."""
    n = nama.lower().strip()
    # Jika ada kata kunci PTS → langsung tolak
    for kw in _PTS_KEYWORDS_NEGATIF:
        if kw in n:
            return False
    # Jika ada kata kunci PTN → terima
    for kw in _PTN_KEYWORDS_POSITIF:
        if kw in n:
            return True
    # Default: tolak jika tidak cocok keyword PTN
    return False

# ══════════════════════════════════════════════════════════
# DATABASE PRODI D3 DAN D4 AKURAT PER KAMPUS
# Sumber: website resmi masing-masing PTN & SNPMB 2022-2024
# ══════════════════════════════════════════════════════════

PTN_PRODI_D3 = {
    # ── POLITEKNIK ──
    "Politeknik Negeri Bandung": {
        "D3 Teknik Sipil": {"mn": 530, "mx": 600},
        "D3 Teknik Geodesi": {"mn": 520, "mx": 590},
        "D3 Teknik Mesin": {"mn": 520, "mx": 590},
        "D3 Teknik Refrigerasi dan Tata Udara": {"mn": 510, "mx": 580},
        "D3 Teknik Otomotif": {"mn": 510, "mx": 580},
        "D3 Teknik Elektronika": {"mn": 530, "mx": 600},
        "D3 Teknik Elektro": {"mn": 535, "mx": 605},
        "D3 Teknik Informatika": {"mn": 560, "mx": 630},
        "D3 Teknik Kimia": {"mn": 510, "mx": 580},
        "D3 Analisis Kimia": {"mn": 510, "mx": 580},
        "D3 Teknik Lingkungan": {"mn": 500, "mx": 570},
        "D3 Akuntansi": {"mn": 520, "mx": 590},
        "D3 Keuangan dan Perbankan": {"mn": 510, "mx": 580},
        "D3 Manajemen Pemasaran": {"mn": 500, "mx": 570},
        "D3 Administrasi Bisnis": {"mn": 500, "mx": 570},
        "D3 Manajemen Informatika": {"mn": 530, "mx": 600},
        "D3 Komputerisasi Akuntansi": {"mn": 520, "mx": 590},
        "D3 Usaha Perjalanan Wisata": {"mn": 490, "mx": 560},
        "D3 Manajemen Aset": {"mn": 490, "mx": 560},
    },
    "Politeknik Negeri Jakarta": {
        "D3 Teknik Sipil": {"mn": 520, "mx": 590},
        "D3 Teknik Mesin": {"mn": 515, "mx": 585},
        "D3 Teknik Elektro": {"mn": 530, "mx": 600},
        "D3 Teknik Elektronika": {"mn": 525, "mx": 595},
        "D3 Teknik Informatika": {"mn": 550, "mx": 620},
        "D3 Teknik Kimia": {"mn": 505, "mx": 575},
        "D3 Akuntansi": {"mn": 515, "mx": 585},
        "D3 Keuangan dan Perbankan": {"mn": 505, "mx": 575},
        "D3 Manajemen Pemasaran": {"mn": 495, "mx": 565},
        "D3 Administrasi Bisnis": {"mn": 495, "mx": 565},
        "D3 Manajemen Informatika": {"mn": 525, "mx": 595},
        "D3 Komputerisasi Akuntansi": {"mn": 515, "mx": 585},
        "D3 Perbankan Syariah": {"mn": 495, "mx": 565},
        "D3 Teknik Grafika dan Penerbitan": {"mn": 490, "mx": 560},
    },
    "Politeknik Negeri Semarang": {
        "D3 Teknik Sipil": {"mn": 510, "mx": 580},
        "D3 Teknik Mesin": {"mn": 505, "mx": 575},
        "D3 Teknik Elektro": {"mn": 520, "mx": 590},
        "D3 Teknik Elektronika": {"mn": 515, "mx": 585},
        "D3 Teknik Informatika": {"mn": 540, "mx": 610},
        "D3 Teknik Kimia": {"mn": 500, "mx": 570},
        "D3 Teknik Telekomunikasi": {"mn": 515, "mx": 585},
        "D3 Akuntansi": {"mn": 510, "mx": 580},
        "D3 Keuangan dan Perbankan": {"mn": 500, "mx": 570},
        "D3 Manajemen Pemasaran": {"mn": 490, "mx": 560},
        "D3 Administrasi Bisnis": {"mn": 490, "mx": 560},
        "D3 Manajemen Informatika": {"mn": 520, "mx": 590},
        "D3 Komputerisasi Akuntansi": {"mn": 510, "mx": 580},
        "D3 Teknik Konstruksi Gedung": {"mn": 495, "mx": 565},
    },
    "Politeknik Negeri Malang": {
        "D3 Teknik Sipil": {"mn": 505, "mx": 575},
        "D3 Teknik Mesin": {"mn": 500, "mx": 570},
        "D3 Teknik Elektro": {"mn": 515, "mx": 585},
        "D3 Teknik Elektronika": {"mn": 510, "mx": 580},
        "D3 Teknik Informatika": {"mn": 535, "mx": 605},
        "D3 Teknik Kimia": {"mn": 495, "mx": 565},
        "D3 Teknik Listrik": {"mn": 500, "mx": 570},
        "D3 Akuntansi": {"mn": 505, "mx": 575},
        "D3 Keuangan dan Perbankan": {"mn": 495, "mx": 565},
        "D3 Manajemen Pemasaran": {"mn": 485, "mx": 555},
        "D3 Administrasi Bisnis": {"mn": 485, "mx": 555},
        "D3 Manajemen Informatika": {"mn": 515, "mx": 585},
        "D3 Komputerisasi Akuntansi": {"mn": 505, "mx": 575},
        "D3 Teknik Otomotif Elektronik": {"mn": 495, "mx": 565},
    },
    "Politeknik Negeri Medan": {
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Mesin": {"mn": 485, "mx": 555},
        "D3 Teknik Elektro": {"mn": 500, "mx": 570},
        "D3 Teknik Elektronika": {"mn": 495, "mx": 565},
        "D3 Teknik Informatika": {"mn": 515, "mx": 585},
        "D3 Teknik Kimia": {"mn": 480, "mx": 550},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Keuangan dan Perbankan": {"mn": 480, "mx": 550},
        "D3 Manajemen Pemasaran": {"mn": 470, "mx": 540},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 500, "mx": 570},
        "D3 Komputerisasi Akuntansi": {"mn": 490, "mx": 560},
        "D3 Teknik Konstruksi Gedung": {"mn": 475, "mx": 545},
    },
    "Politeknik Negeri Ujung Pandang": {
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Mesin": {"mn": 485, "mx": 555},
        "D3 Teknik Elektro": {"mn": 500, "mx": 570},
        "D3 Teknik Elektronika": {"mn": 495, "mx": 565},
        "D3 Teknik Informatika": {"mn": 515, "mx": 585},
        "D3 Teknik Kimia": {"mn": 480, "mx": 550},
        "D3 Teknik Refrigerasi dan Tata Udara": {"mn": 480, "mx": 550},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 500, "mx": 570},
        "D3 Pariwisata": {"mn": 460, "mx": 530},
        "D3 Teknik Konstruksi Gedung": {"mn": 475, "mx": 545},
        "D3 Teknik Pertambangan": {"mn": 470, "mx": 540},
    },
    "Politeknik Negeri Bali": {
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Mesin": {"mn": 485, "mx": 555},
        "D3 Teknik Elektro": {"mn": 495, "mx": 565},
        "D3 Teknik Elektronika": {"mn": 490, "mx": 560},
        "D3 Teknik Informatika": {"mn": 510, "mx": 580},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Keuangan dan Perbankan": {"mn": 480, "mx": 550},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 500, "mx": 570},
        "D3 Pariwisata": {"mn": 490, "mx": 560},
        "D3 Usaha Perjalanan Wisata": {"mn": 480, "mx": 550},
        "D3 Perhotelan": {"mn": 475, "mx": 545},
        "D3 Manajemen Proyek": {"mn": 470, "mx": 540},
    },
    "Politeknik Elektronika Negeri Surabaya": {
        "D3 Teknik Elektronika": {"mn": 545, "mx": 615},
        "D3 Teknik Informatika": {"mn": 555, "mx": 625},
        "D3 Teknik Telekomunikasi": {"mn": 535, "mx": 605},
        "D3 Teknik Komputer": {"mn": 540, "mx": 610},
        "D3 Teknik Listrik": {"mn": 520, "mx": 590},
        "D3 Sistem Kelistrikan": {"mn": 515, "mx": 585},
        "D3 Manajemen Informatika": {"mn": 530, "mx": 600},
        "D3 Teknik Mekatronika": {"mn": 535, "mx": 605},
    },
    "Politeknik Manufaktur Negeri Bandung": {
        "D3 Teknik Mesin": {"mn": 530, "mx": 600},
        "D3 Teknik Manufaktur": {"mn": 525, "mx": 595},
        "D3 Teknik Otomasi Industri": {"mn": 530, "mx": 600},
        "D3 Teknik Perancangan dan Konstruksi Mesin": {"mn": 520, "mx": 590},
        "D3 Teknik Pemeliharaan Mesin": {"mn": 515, "mx": 585},
        "D3 Teknik Pengecoran Logam": {"mn": 505, "mx": 575},
    },
    "Politeknik Perkapalan Negeri Surabaya": {
        "D3 Teknik Perkapalan": {"mn": 530, "mx": 600},
        "D3 Teknik Permesinan Kapal": {"mn": 520, "mx": 590},
        "D3 Teknik Kelistrikan Kapal": {"mn": 515, "mx": 585},
        "D3 Teknik Bangunan Kapal": {"mn": 525, "mx": 595},
        "D3 Teknik Desain dan Manufaktur": {"mn": 515, "mx": 585},
        "D3 Teknik Keselamatan dan Kesehatan Kerja": {"mn": 510, "mx": 580},
    },

    # ── UNIVERSITAS (D3 yang benar-benar ada) ──
    "Universitas Indonesia": {
        "D3 Fisioterapi": {"mn": 560, "mx": 630},
        "D3 Okupasi Terapi": {"mn": 540, "mx": 610},
        "D3 Administrasi Perkantoran": {"mn": 510, "mx": 580},
        "D3 Akuntansi": {"mn": 540, "mx": 610},
        "D3 Perpajakan": {"mn": 530, "mx": 600},
        "D3 Manajemen Informasi": {"mn": 510, "mx": 580},
        "D3 Hubungan Masyarakat": {"mn": 510, "mx": 580},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 530, "mx": 600},
        "D3 Teknik Komputer": {"mn": 560, "mx": 630},
        "D3 Kebidanan": {"mn": 530, "mx": 600},
    },
    "Institut Teknologi Bandung": {
        "D3 Teknik Sipil": {"mn": 590, "mx": 660},
        "D3 Teknik Mesin": {"mn": 585, "mx": 655},
        "D3 Teknik Elektro": {"mn": 595, "mx": 665},
        "D3 Teknik Kimia": {"mn": 575, "mx": 645},
        "D3 Teknik Informatika": {"mn": 615, "mx": 685},
        "D3 Manajemen Informatika": {"mn": 580, "mx": 650},
        "D3 Analisis Kimia": {"mn": 560, "mx": 630},
        "D3 Teknik Geodesi": {"mn": 565, "mx": 635},
        "D3 Teknik Lingkungan": {"mn": 555, "mx": 625},
        "D3 Manajemen Pemasaran": {"mn": 545, "mx": 615},
        "D3 Akuntansi": {"mn": 555, "mx": 625},
    },
    "Institut Teknologi Sepuluh Nopember": {
        "D3 Teknik Sipil": {"mn": 560, "mx": 630},
        "D3 Teknik Mesin": {"mn": 555, "mx": 625},
        "D3 Teknik Elektro": {"mn": 570, "mx": 640},
        "D3 Teknik Kimia": {"mn": 545, "mx": 615},
        "D3 Teknik Informatika": {"mn": 590, "mx": 660},
        "D3 Teknik Perkapalan": {"mn": 545, "mx": 615},
        "D3 Teknik Permesinan Kapal": {"mn": 535, "mx": 605},
        "D3 Instrumentasi": {"mn": 540, "mx": 610},
        "D3 Statistika Bisnis": {"mn": 545, "mx": 615},
        "D3 Manajemen Bisnis": {"mn": 545, "mx": 615},
    },
    "Institut Pertanian Bogor": {
        "D3 Analisis Kimia": {"mn": 530, "mx": 600},
        "D3 Teknologi Pangan": {"mn": 540, "mx": 610},
        "D3 Ekowisata": {"mn": 490, "mx": 560},
        "D3 Manajemen Informatika": {"mn": 515, "mx": 585},
        "D3 Akuntansi": {"mn": 510, "mx": 580},
        "D3 Teknik Komputer": {"mn": 525, "mx": 595},
        "D3 Komunikasi": {"mn": 495, "mx": 565},
        "D3 Pengelolaan Perkebunan": {"mn": 465, "mx": 535},
        "D3 Manajemen Agribisnis": {"mn": 475, "mx": 545},
        "D3 Supervisor Jaminan Mutu Pangan": {"mn": 480, "mx": 550},
        "D3 Manajemen Sumber Daya Lahan": {"mn": 460, "mx": 530},
        "D3 Teknik dan Manajemen Lingkungan": {"mn": 470, "mx": 540},
    },
    "Universitas Gadjah Mada": {
        "D3 Bahasa Inggris": {"mn": 530, "mx": 600},
        "D3 Bahasa Jepang": {"mn": 510, "mx": 580},
        "D3 Bahasa Prancis": {"mn": 500, "mx": 570},
        "D3 Bahasa Korea": {"mn": 505, "mx": 575},
        "D3 Akuntansi": {"mn": 550, "mx": 620},
        "D3 Manajemen": {"mn": 545, "mx": 615},
        "D3 Perpajakan": {"mn": 530, "mx": 600},
        "D3 Keuangan dan Perbankan": {"mn": 520, "mx": 590},
        "D3 Ekonomika Terapan": {"mn": 520, "mx": 590},
        "D3 Rekam Medis": {"mn": 530, "mx": 600},
        "D3 Kesehatan Hewan": {"mn": 490, "mx": 560},
        "D3 Komputer dan Sistem Informasi": {"mn": 545, "mx": 615},
        "D3 Elektronika dan Instrumentasi": {"mn": 530, "mx": 600},
        "D3 Teknik Elektro": {"mn": 530, "mx": 600},
        "D3 Teknik Mesin": {"mn": 520, "mx": 590},
        "D3 Teknik Sipil": {"mn": 525, "mx": 595},
        "D3 Teknik Kimia": {"mn": 510, "mx": 580},
        "D3 Teknik Geomatika": {"mn": 510, "mx": 580},
        "D3 Pariwisata": {"mn": 510, "mx": 580},
        "D3 Manajemen dan Penilaian Properti": {"mn": 505, "mx": 575},
    },
    "Universitas Airlangga": {
        "D3 Analis Kesehatan / TLM": {"mn": 540, "mx": 610},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 520, "mx": 590},
        "D3 Fisioterapi": {"mn": 530, "mx": 600},
        "D3 Radiologi": {"mn": 525, "mx": 595},
        "D3 Gizi": {"mn": 520, "mx": 590},
        "D3 Keperawatan": {"mn": 515, "mx": 585},
        "D3 Kebidanan": {"mn": 510, "mx": 580},
        "D3 Farmasi": {"mn": 540, "mx": 610},
        "D3 Akuntansi": {"mn": 520, "mx": 590},
        "D3 Perpajakan": {"mn": 510, "mx": 580},
        "D3 Manajemen Pemasaran": {"mn": 500, "mx": 570},
        "D3 Keuangan dan Perbankan": {"mn": 505, "mx": 575},
        "D3 Administrasi Bisnis": {"mn": 495, "mx": 565},
        "D3 Bahasa Inggris": {"mn": 500, "mx": 570},
        "D3 Bahasa Jepang": {"mn": 480, "mx": 550},
        "D3 Teknik Informatika": {"mn": 530, "mx": 600},
        "D3 Manajemen Informasi Kesehatan": {"mn": 515, "mx": 585},
        "D3 Hubungan Masyarakat": {"mn": 490, "mx": 560},
    },
    "Universitas Padjadjaran": {
        "D3 Analis Kesehatan / TLM": {"mn": 530, "mx": 600},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 510, "mx": 580},
        "D3 Fisioterapi": {"mn": 520, "mx": 590},
        "D3 Radiologi": {"mn": 515, "mx": 585},
        "D3 Gizi": {"mn": 510, "mx": 580},
        "D3 Keperawatan": {"mn": 505, "mx": 575},
        "D3 Kebidanan": {"mn": 500, "mx": 570},
        "D3 Farmasi": {"mn": 525, "mx": 595},
        "D3 Akuntansi": {"mn": 515, "mx": 585},
        "D3 Perpajakan": {"mn": 505, "mx": 575},
        "D3 Manajemen Pemasaran": {"mn": 495, "mx": 565},
        "D3 Keuangan dan Perbankan": {"mn": 495, "mx": 565},
        "D3 Administrasi Bisnis": {"mn": 485, "mx": 555},
        "D3 Bahasa Inggris": {"mn": 490, "mx": 560},
        "D3 Bahasa Jepang": {"mn": 470, "mx": 540},
        "D3 Hubungan Masyarakat": {"mn": 485, "mx": 555},
        "D3 Kehumasan": {"mn": 480, "mx": 550},
    },
    "Universitas Diponegoro": {
        "D3 Analis Kesehatan / TLM": {"mn": 510, "mx": 580},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 490, "mx": 560},
        "D3 Gizi": {"mn": 495, "mx": 565},
        "D3 Keperawatan": {"mn": 485, "mx": 555},
        "D3 Farmasi": {"mn": 505, "mx": 575},
        "D3 Akuntansi": {"mn": 500, "mx": 570},
        "D3 Perpajakan": {"mn": 490, "mx": 560},
        "D3 Manajemen Pemasaran": {"mn": 475, "mx": 545},
        "D3 Keuangan dan Perbankan": {"mn": 480, "mx": 550},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Bahasa Inggris": {"mn": 475, "mx": 545},
        "D3 Hubungan Masyarakat": {"mn": 470, "mx": 540},
        "D3 Teknik Informatika": {"mn": 510, "mx": 580},
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Elektro": {"mn": 490, "mx": 560},
        "D3 Teknik Kimia": {"mn": 480, "mx": 550},
        "D3 Teknik Geomatika": {"mn": 475, "mx": 545},
    },
    "Universitas Brawijaya": {
        "D3 Analis Kesehatan / TLM": {"mn": 500, "mx": 570},
        "D3 Keperawatan": {"mn": 475, "mx": 545},
        "D3 Kebidanan": {"mn": 470, "mx": 540},
        "D3 Gizi": {"mn": 480, "mx": 550},
        "D3 Farmasi": {"mn": 490, "mx": 560},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Perpajakan": {"mn": 480, "mx": 550},
        "D3 Manajemen Pemasaran": {"mn": 465, "mx": 535},
        "D3 Keuangan dan Perbankan": {"mn": 470, "mx": 540},
        "D3 Administrasi Bisnis": {"mn": 460, "mx": 530},
        "D3 Bahasa Inggris": {"mn": 465, "mx": 535},
        "D3 Teknik Informatika": {"mn": 495, "mx": 565},
        "D3 Manajemen Informatika": {"mn": 480, "mx": 550},
        "D3 Teknik Sipil": {"mn": 470, "mx": 540},
        "D3 Teknik Pengairan": {"mn": 455, "mx": 525},
        "D3 Statistika": {"mn": 470, "mx": 540},
    },
    "Universitas Sebelas Maret": {
        "D3 Rekam Medis": {"mn": 490, "mx": 560},
        "D3 Analis Kesehatan / TLM": {"mn": 495, "mx": 565},
        "D3 Keperawatan": {"mn": 470, "mx": 540},
        "D3 Kebidanan": {"mn": 465, "mx": 535},
        "D3 Farmasi": {"mn": 480, "mx": 550},
        "D3 Akuntansi": {"mn": 480, "mx": 550},
        "D3 Perpajakan": {"mn": 470, "mx": 540},
        "D3 Keuangan dan Perbankan": {"mn": 460, "mx": 530},
        "D3 Manajemen Pemasaran": {"mn": 450, "mx": 520},
        "D3 Manajemen Administrasi": {"mn": 450, "mx": 520},
        "D3 Usaha Perjalanan Wisata": {"mn": 445, "mx": 515},
        "D3 Komunikasi Terapan": {"mn": 450, "mx": 520},
        "D3 Bahasa Inggris": {"mn": 455, "mx": 525},
        "D3 Bahasa Mandarin": {"mn": 445, "mx": 515},
        "D3 Bahasa Jepang": {"mn": 440, "mx": 510},
        "D3 Teknik Informatika": {"mn": 480, "mx": 550},
        "D3 Teknik Sipil": {"mn": 455, "mx": 525},
        "D3 Teknik Kimia": {"mn": 445, "mx": 515},
        "D3 Teknik Mesin": {"mn": 445, "mx": 515},
        "D3 Statistika": {"mn": 455, "mx": 525},
        "D3 Desain Komunikasi Visual": {"mn": 430, "mx": 500},
    },
    "Universitas Hasanuddin": {
        "D3 Rekam Medis": {"mn": 480, "mx": 550},
        "D3 Analis Kesehatan / TLM": {"mn": 480, "mx": 550},
        "D3 Keperawatan": {"mn": 455, "mx": 525},
        "D3 Kebidanan": {"mn": 450, "mx": 520},
        "D3 Farmasi": {"mn": 465, "mx": 535},
        "D3 Akuntansi": {"mn": 465, "mx": 535},
        "D3 Perpajakan": {"mn": 455, "mx": 525},
        "D3 Manajemen Pemasaran": {"mn": 445, "mx": 515},
        "D3 Administrasi Bisnis": {"mn": 440, "mx": 510},
        "D3 Teknik Informatika": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 455, "mx": 525},
        "D3 Teknik Sipil": {"mn": 450, "mx": 520},
        "D3 Teknik Elektro": {"mn": 455, "mx": 525},
        "D3 Teknik Mesin": {"mn": 445, "mx": 515},
        "D3 Statistika": {"mn": 450, "mx": 520},
    },
    "Universitas Sumatera Utara": {
        "D3 Rekam Medis": {"mn": 460, "mx": 530},
        "D3 Analis Kesehatan / TLM": {"mn": 465, "mx": 535},
        "D3 Keperawatan": {"mn": 440, "mx": 510},
        "D3 Kebidanan": {"mn": 435, "mx": 505},
        "D3 Farmasi": {"mn": 450, "mx": 520},
        "D3 Fisioterapi": {"mn": 445, "mx": 515},
        "D3 Akuntansi": {"mn": 450, "mx": 520},
        "D3 Perpajakan": {"mn": 440, "mx": 510},
        "D3 Keuangan dan Perbankan": {"mn": 435, "mx": 505},
        "D3 Manajemen Pemasaran": {"mn": 425, "mx": 495},
        "D3 Administrasi Bisnis": {"mn": 420, "mx": 490},
        "D3 Bahasa Inggris": {"mn": 435, "mx": 505},
        "D3 Bahasa Jepang": {"mn": 420, "mx": 490},
        "D3 Bahasa Mandarin": {"mn": 415, "mx": 485},
        "D3 Teknik Informatika": {"mn": 460, "mx": 530},
        "D3 Manajemen Informatika": {"mn": 445, "mx": 515},
        "D3 Teknik Sipil": {"mn": 435, "mx": 505},
        "D3 Teknik Elektro": {"mn": 435, "mx": 505},
        "D3 Teknik Kimia": {"mn": 425, "mx": 495},
        "D3 Statistika": {"mn": 435, "mx": 505},
    },
    "Universitas Andalas": {
        "D3 Rekam Medis": {"mn": 450, "mx": 520},
        "D3 Analis Kesehatan / TLM": {"mn": 455, "mx": 525},
        "D3 Keperawatan": {"mn": 430, "mx": 500},
        "D3 Kebidanan": {"mn": 425, "mx": 495},
        "D3 Farmasi": {"mn": 445, "mx": 515},
        "D3 Akuntansi": {"mn": 445, "mx": 515},
        "D3 Perpajakan": {"mn": 435, "mx": 505},
        "D3 Keuangan dan Perbankan": {"mn": 430, "mx": 500},
        "D3 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D3 Teknik Informatika": {"mn": 455, "mx": 525},
        "D3 Teknik Sipil": {"mn": 430, "mx": 500},
        "D3 Teknik Elektro": {"mn": 430, "mx": 500},
        "D3 Teknik Mesin": {"mn": 420, "mx": 490},
    },
    "Universitas Sriwijaya": {
        "D3 Keperawatan": {"mn": 415, "mx": 485},
        "D3 Kebidanan": {"mn": 410, "mx": 480},
        "D3 Akuntansi": {"mn": 430, "mx": 500},
        "D3 Perpajakan": {"mn": 420, "mx": 490},
        "D3 Keuangan dan Perbankan": {"mn": 415, "mx": 485},
        "D3 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D3 Administrasi Bisnis": {"mn": 400, "mx": 470},
        "D3 Teknik Informatika": {"mn": 440, "mx": 510},
        "D3 Teknik Sipil": {"mn": 415, "mx": 485},
        "D3 Teknik Elektro": {"mn": 415, "mx": 485},
        "D3 Teknik Mesin": {"mn": 405, "mx": 475},
        "D3 Teknik Kimia": {"mn": 405, "mx": 475},
    },
    "Universitas Udayana": {
        "D3 Rekam Medis": {"mn": 450, "mx": 520},
        "D3 Analis Kesehatan / TLM": {"mn": 455, "mx": 525},
        "D3 Keperawatan": {"mn": 430, "mx": 500},
        "D3 Kebidanan": {"mn": 425, "mx": 495},
        "D3 Farmasi": {"mn": 445, "mx": 515},
        "D3 Fisioterapi": {"mn": 440, "mx": 510},
        "D3 Akuntansi": {"mn": 445, "mx": 515},
        "D3 Perpajakan": {"mn": 435, "mx": 505},
        "D3 Keuangan dan Perbankan": {"mn": 430, "mx": 500},
        "D3 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D3 Administrasi Bisnis": {"mn": 415, "mx": 485},
        "D3 Teknik Informatika": {"mn": 455, "mx": 525},
        "D3 Teknik Sipil": {"mn": 430, "mx": 500},
        "D3 Pariwisata": {"mn": 450, "mx": 520},
        "D3 Bahasa Inggris": {"mn": 430, "mx": 500},
    },
    "Universitas Jember": {
        "D3 Rekam Medis": {"mn": 435, "mx": 505},
        "D3 Analis Kesehatan / TLM": {"mn": 440, "mx": 510},
        "D3 Keperawatan": {"mn": 415, "mx": 485},
        "D3 Kebidanan": {"mn": 410, "mx": 480},
        "D3 Farmasi": {"mn": 430, "mx": 500},
        "D3 Akuntansi": {"mn": 430, "mx": 500},
        "D3 Perpajakan": {"mn": 420, "mx": 490},
        "D3 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D3 Manajemen Agribisnis": {"mn": 400, "mx": 470},
        "D3 Teknik Informatika": {"mn": 440, "mx": 510},
        "D3 Manajemen Perusahaan": {"mn": 405, "mx": 475},
        "D3 Usaha Perjalanan Wisata": {"mn": 400, "mx": 470},
    },
    "Universitas Lampung": {
        "D3 Keperawatan": {"mn": 405, "mx": 475},
        "D3 Kebidanan": {"mn": 400, "mx": 470},
        "D3 Akuntansi": {"mn": 415, "mx": 485},
        "D3 Perpajakan": {"mn": 405, "mx": 475},
        "D3 Manajemen Pemasaran": {"mn": 415, "mx": 485},
        "D3 Administrasi Bisnis": {"mn": 415, "mx": 485},
        "D3 Teknik Informatika": {"mn": 425, "mx": 495},
        "D3 Manajemen Informatika": {"mn": 410, "mx": 480},
        "D3 Teknik Sipil": {"mn": 400, "mx": 470},
        "D3 Teknik Elektro": {"mn": 400, "mx": 470},
    },
    "Universitas Negeri Yogyakarta": {
        "D3 Teknik Elektro": {"mn": 450, "mx": 520},
        "D3 Teknik Mesin": {"mn": 445, "mx": 515},
        "D3 Teknik Sipil dan Perencanaan": {"mn": 445, "mx": 515},
        "D3 Teknik Elektronika": {"mn": 445, "mx": 515},
        "D3 Tata Boga": {"mn": 415, "mx": 485},
        "D3 Tata Busana": {"mn": 405, "mx": 475},
        "D3 Tata Rias dan Kecantikan": {"mn": 405, "mx": 475},
        "D3 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D3 Akuntansi": {"mn": 430, "mx": 500},
        "D3 Teknik Informatika": {"mn": 455, "mx": 525},
    },
    "Universitas Negeri Malang": {
        "D3 Teknik Elektro": {"mn": 440, "mx": 510},
        "D3 Teknik Mesin": {"mn": 435, "mx": 505},
        "D3 Teknik Sipil": {"mn": 435, "mx": 505},
        "D3 Manajemen Pemasaran": {"mn": 410, "mx": 480},
        "D3 Akuntansi": {"mn": 420, "mx": 490},
        "D3 Teknik Informatika": {"mn": 445, "mx": 515},
        "D3 Desain Komunikasi Visual": {"mn": 405, "mx": 475},
    },
    "Universitas Negeri Semarang": {
        "D3 Teknik Elektro": {"mn": 430, "mx": 500},
        "D3 Teknik Mesin": {"mn": 425, "mx": 495},
        "D3 Teknik Sipil": {"mn": 425, "mx": 495},
        "D3 Teknik Kimia": {"mn": 415, "mx": 485},
        "D3 Manajemen Pemasaran": {"mn": 400, "mx": 470},
        "D3 Akuntansi": {"mn": 410, "mx": 480},
        "D3 Teknik Informatika": {"mn": 435, "mx": 505},
        "D3 Desain Komunikasi Visual": {"mn": 400, "mx": 470},
        "D3 Tata Boga": {"mn": 400, "mx": 470},
    },
    "Universitas Pendidikan Indonesia": {
        "D3 Teknik Elektro": {"mn": 445, "mx": 515},
        "D3 Teknik Mesin": {"mn": 435, "mx": 505},
        "D3 Teknik Sipil": {"mn": 435, "mx": 505},
        "D3 Manajemen Pemasaran": {"mn": 410, "mx": 480},
        "D3 Akuntansi": {"mn": 420, "mx": 490},
        "D3 Teknik Informatika": {"mn": 450, "mx": 520},
        "D3 Bahasa Inggris": {"mn": 430, "mx": 500},
        "D3 Desain Komunikasi Visual": {"mn": 410, "mx": 480},
        "D3 Tata Boga": {"mn": 405, "mx": 475},
        "D3 Tata Busana": {"mn": 400, "mx": 470},
    },
}

PTN_PRODI_D4 = {
    # ── POLITEKNIK ──
    "Politeknik Negeri Bandung": {
        "D4 Teknik Informatika": {"mn": 580, "mx": 650},
        "D4 Teknik Komputer": {"mn": 565, "mx": 635},
        "D4 Teknik Telekomunikasi": {"mn": 555, "mx": 625},
        "D4 Teknik Elektro": {"mn": 555, "mx": 625},
        "D4 Teknik Mesin": {"mn": 545, "mx": 615},
        "D4 Teknik Otomasi": {"mn": 555, "mx": 625},
        "D4 Teknik Sipil": {"mn": 545, "mx": 615},
        "D4 Teknik Kimia": {"mn": 535, "mx": 605},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 530, "mx": 600},
        "D4 Akuntansi Sektor Publik": {"mn": 545, "mx": 615},
        "D4 Keuangan dan Perbankan": {"mn": 535, "mx": 605},
        "D4 Manajemen Pemasaran": {"mn": 525, "mx": 595},
        "D4 Administrasi Bisnis": {"mn": 525, "mx": 595},
        "D4 Manajemen Penilaian Properti": {"mn": 520, "mx": 590},
        "D4 Manajemen Pariwisata": {"mn": 510, "mx": 580},
        "D4 Logistik": {"mn": 525, "mx": 595},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 540, "mx": 610},
        "D4 Teknik Mekatronika": {"mn": 550, "mx": 620},
        "D4 Teknik Geomatika": {"mn": 530, "mx": 600},
        "D4 Bahasa Inggris Terapan": {"mn": 510, "mx": 580},
    },
    "Politeknik Negeri Jakarta": {
        "D4 Teknik Informatika": {"mn": 560, "mx": 630},
        "D4 Teknik Komputer": {"mn": 545, "mx": 615},
        "D4 Teknik Elektro": {"mn": 545, "mx": 615},
        "D4 Teknik Mesin": {"mn": 535, "mx": 605},
        "D4 Teknik Sipil": {"mn": 535, "mx": 605},
        "D4 Teknik Kimia": {"mn": 520, "mx": 590},
        "D4 Akuntansi Sektor Publik": {"mn": 525, "mx": 595},
        "D4 Keuangan dan Perbankan": {"mn": 515, "mx": 585},
        "D4 Manajemen Pemasaran": {"mn": 505, "mx": 575},
        "D4 Administrasi Bisnis": {"mn": 505, "mx": 575},
        "D4 Teknik Mekatronika": {"mn": 530, "mx": 600},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 520, "mx": 590},
        "D4 Manajemen Logistik": {"mn": 505, "mx": 575},
        "D4 Perbankan Syariah": {"mn": 500, "mx": 570},
        "D4 Teknologi Rekayasa Konstruksi Bangunan Gedung": {"mn": 510, "mx": 580},
    },
    "Politeknik Negeri Semarang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 555, "mx": 625},
        "D4 Teknik Informatika": {"mn": 560, "mx": 630},
        "D4 Teknik Elektro": {"mn": 540, "mx": 610},
        "D4 Teknik Telekomunikasi": {"mn": 535, "mx": 605},
        "D4 Teknik Mesin": {"mn": 530, "mx": 600},
        "D4 Teknik Sipil": {"mn": 530, "mx": 600},
        "D4 Teknik Kimia": {"mn": 520, "mx": 590},
        "D4 Akuntansi Sektor Publik": {"mn": 525, "mx": 595},
        "D4 Keuangan dan Perbankan": {"mn": 515, "mx": 585},
        "D4 Manajemen Pemasaran": {"mn": 505, "mx": 575},
        "D4 Administrasi Bisnis": {"mn": 500, "mx": 570},
        "D4 Teknik Otomasi": {"mn": 530, "mx": 600},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 520, "mx": 590},
        "D4 Logistik Bisnis": {"mn": 505, "mx": 575},
    },
    "Politeknik Negeri Malang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 545, "mx": 615},
        "D4 Teknik Informatika": {"mn": 550, "mx": 620},
        "D4 Teknik Elektro": {"mn": 530, "mx": 600},
        "D4 Teknik Mesin": {"mn": 520, "mx": 590},
        "D4 Teknik Sipil": {"mn": 520, "mx": 590},
        "D4 Teknik Kimia": {"mn": 510, "mx": 580},
        "D4 Akuntansi Sektor Publik": {"mn": 515, "mx": 585},
        "D4 Keuangan dan Perbankan": {"mn": 505, "mx": 575},
        "D4 Manajemen Pemasaran": {"mn": 495, "mx": 565},
        "D4 Administrasi Bisnis": {"mn": 490, "mx": 560},
        "D4 Teknik Otomasi": {"mn": 520, "mx": 590},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 510, "mx": 580},
        "D4 Manajemen Energi": {"mn": 495, "mx": 565},
        "D4 Teknologi Rekayasa Kimia": {"mn": 505, "mx": 575},
    },
    "Politeknik Negeri Medan": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 520, "mx": 590},
        "D4 Teknik Informatika": {"mn": 525, "mx": 595},
        "D4 Teknik Elektro": {"mn": 510, "mx": 580},
        "D4 Teknik Mesin": {"mn": 500, "mx": 570},
        "D4 Teknik Sipil": {"mn": 500, "mx": 570},
        "D4 Teknik Kimia": {"mn": 490, "mx": 560},
        "D4 Akuntansi Sektor Publik": {"mn": 495, "mx": 565},
        "D4 Keuangan dan Perbankan": {"mn": 485, "mx": 555},
        "D4 Manajemen Pemasaran": {"mn": 475, "mx": 545},
        "D4 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D4 Teknik Otomasi": {"mn": 500, "mx": 570},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 490, "mx": 560},
        "D4 Teknologi Rekayasa Konstruksi Gedung": {"mn": 485, "mx": 555},
    },
    "Politeknik Negeri Ujung Pandang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 515, "mx": 585},
        "D4 Teknik Informatika": {"mn": 520, "mx": 590},
        "D4 Teknik Elektro": {"mn": 505, "mx": 575},
        "D4 Teknik Mesin": {"mn": 495, "mx": 565},
        "D4 Teknik Sipil": {"mn": 495, "mx": 565},
        "D4 Teknik Kimia": {"mn": 485, "mx": 555},
        "D4 Akuntansi Sektor Publik": {"mn": 490, "mx": 560},
        "D4 Administrasi Bisnis": {"mn": 465, "mx": 535},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 485, "mx": 555},
        "D4 Manajemen Pariwisata": {"mn": 465, "mx": 535},
        "D4 Teknologi Rekayasa Pertambangan": {"mn": 470, "mx": 540},
    },
    "Politeknik Negeri Bali": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 510, "mx": 580},
        "D4 Teknik Informatika": {"mn": 515, "mx": 585},
        "D4 Teknik Elektro": {"mn": 500, "mx": 570},
        "D4 Teknik Mesin": {"mn": 490, "mx": 560},
        "D4 Teknik Sipil": {"mn": 490, "mx": 560},
        "D4 Akuntansi Sektor Publik": {"mn": 485, "mx": 555},
        "D4 Administrasi Bisnis": {"mn": 460, "mx": 530},
        "D4 Manajemen Pariwisata": {"mn": 480, "mx": 550},
        "D4 Perhotelan": {"mn": 470, "mx": 540},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 480, "mx": 550},
    },
    "Politeknik Elektronika Negeri Surabaya": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 580, "mx": 650},
        "D4 Teknik Informatika": {"mn": 585, "mx": 655},
        "D4 Teknik Komputer": {"mn": 570, "mx": 640},
        "D4 Teknik Telekomunikasi": {"mn": 560, "mx": 630},
        "D4 Teknik Mekatronika": {"mn": 565, "mx": 635},
        "D4 Teknologi Informasi": {"mn": 575, "mx": 645},
        "D4 Teknik Elektro Industri": {"mn": 555, "mx": 625},
        "D4 Teknologi Rekayasa Komputer": {"mn": 570, "mx": 640},
    },
    "Politeknik Manufaktur Negeri Bandung": {
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 560, "mx": 630},
        "D4 Teknik Otomasi Industri": {"mn": 555, "mx": 625},
        "D4 Teknik Perancangan dan Konstruksi Mesin": {"mn": 545, "mx": 615},
        "D4 Manajemen Produksi": {"mn": 530, "mx": 600},
        "D4 Teknik Kimia Polimer": {"mn": 530, "mx": 600},
    },
    "Politeknik Perkapalan Negeri Surabaya": {
        "D4 Teknik Perkapalan": {"mn": 555, "mx": 625},
        "D4 Teknik Permesinan Kapal": {"mn": 545, "mx": 615},
        "D4 Teknik Kelistrikan Kapal": {"mn": 540, "mx": 610},
        "D4 Teknik Desain dan Manufaktur": {"mn": 540, "mx": 610},
        "D4 Teknik Keselamatan dan Kesehatan Kerja": {"mn": 530, "mx": 600},
        "D4 Teknologi Pengelasan Kapal": {"mn": 530, "mx": 600},
    },

    # ── UNIVERSITAS (D4 yang benar-benar ada) ──
    "Universitas Indonesia": {
        "D4 Teknologi Laboratorium Medis": {"mn": 580, "mx": 650},
        "D4 Fisioterapi": {"mn": 575, "mx": 645},
        "D4 Gizi Klinik": {"mn": 570, "mx": 640},
        "D4 Keperawatan": {"mn": 555, "mx": 625},
        "D4 Kebidanan": {"mn": 545, "mx": 615},
        "D4 Teknik Geomatika": {"mn": 580, "mx": 650},
        "D4 Rekayasa Perangkat Lunak": {"mn": 640, "mx": 710},
        "D4 Teknologi Informasi": {"mn": 630, "mx": 700},
        "D4 Teknik Mekatronika": {"mn": 600, "mx": 670},
        "D4 Teknik Perkapalan": {"mn": 580, "mx": 650},
        "D4 Teknologi Pangan": {"mn": 575, "mx": 645},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 565, "mx": 635},
        "D4 Akuntansi Sektor Publik": {"mn": 580, "mx": 650},
        "D4 Administrasi Bisnis": {"mn": 570, "mx": 640},
        "D4 Manajemen Pariwisata": {"mn": 555, "mx": 625},
        "D4 Bahasa Inggris Terapan": {"mn": 545, "mx": 615},
    },
    "Institut Teknologi Bandung": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 660, "mx": 730},
        "D4 Teknologi Informasi": {"mn": 650, "mx": 720},
        "D4 Teknik Mekatronika": {"mn": 635, "mx": 705},
        "D4 Teknologi Rekayasa Kimia": {"mn": 615, "mx": 685},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 605, "mx": 675},
        "D4 Teknik Geomatika": {"mn": 610, "mx": 680},
        "D4 Teknik Perkapalan": {"mn": 610, "mx": 680},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 620, "mx": 690},
        "D4 Teknik Otomasi": {"mn": 630, "mx": 700},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 595, "mx": 665},
        "D4 Teknologi Pangan": {"mn": 600, "mx": 670},
        "D4 Gizi Klinik": {"mn": 595, "mx": 665},
        "D4 Manajemen Bisnis": {"mn": 640, "mx": 710},
        "D4 Logistik dan Supply Chain": {"mn": 610, "mx": 680},
    },
    "Institut Teknologi Sepuluh Nopember": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 625, "mx": 695},
        "D4 Teknologi Informasi": {"mn": 615, "mx": 685},
        "D4 Teknik Mekatronika": {"mn": 605, "mx": 675},
        "D4 Teknologi Rekayasa Kimia": {"mn": 585, "mx": 655},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 575, "mx": 645},
        "D4 Teknik Geomatika": {"mn": 580, "mx": 650},
        "D4 Teknik Perkapalan": {"mn": 580, "mx": 650},
        "D4 Teknik Kelautan Terapan": {"mn": 570, "mx": 640},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 585, "mx": 655},
        "D4 Teknik Otomasi": {"mn": 595, "mx": 665},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 565, "mx": 635},
        "D4 Manajemen Bisnis": {"mn": 595, "mx": 665},
        "D4 Logistik dan Supply Chain": {"mn": 575, "mx": 645},
        "D4 Statistika Bisnis": {"mn": 580, "mx": 650},
    },
    "Institut Pertanian Bogor": {
        "D4 Teknologi Pangan": {"mn": 560, "mx": 630},
        "D4 Teknologi Rekayasa Pertanian": {"mn": 540, "mx": 610},
        "D4 Manajemen Agribisnis": {"mn": 530, "mx": 600},
        "D4 Teknologi Industri Benih": {"mn": 515, "mx": 585},
        "D4 Supervisor Jaminan Mutu Pangan": {"mn": 520, "mx": 590},
        "D4 Ekowisata": {"mn": 500, "mx": 570},
        "D4 Teknik dan Manajemen Lingkungan Hidup": {"mn": 510, "mx": 580},
        "D4 Manajemen Informatika": {"mn": 530, "mx": 600},
        "D4 Akuntansi Alih Program": {"mn": 510, "mx": 580},
    },
    "Universitas Gadjah Mada": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 620, "mx": 690},
        "D4 Teknologi Informasi": {"mn": 610, "mx": 680},
        "D4 Teknik Mekatronika": {"mn": 595, "mx": 665},
        "D4 Teknologi Rekayasa Kimia": {"mn": 570, "mx": 640},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 560, "mx": 630},
        "D4 Teknik Geomatika": {"mn": 565, "mx": 635},
        "D4 Teknik Pengelolaan dan Pemeliharaan Infrastruktur Sipil": {"mn": 550, "mx": 620},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 565, "mx": 635},
        "D4 Teknik Otomasi": {"mn": 575, "mx": 645},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 545, "mx": 615},
        "D4 Gizi Klinik": {"mn": 555, "mx": 625},
        "D4 Fisioterapi": {"mn": 555, "mx": 625},
        "D4 Teknologi Laboratorium Medis": {"mn": 560, "mx": 630},
        "D4 Teknologi Pangan": {"mn": 555, "mx": 625},
        "D4 Manajemen Bisnis": {"mn": 590, "mx": 660},
        "D4 Logistik dan Supply Chain": {"mn": 560, "mx": 630},
        "D4 Manajemen Penilaian Properti": {"mn": 545, "mx": 615},
        "D4 Manajemen Pariwisata": {"mn": 545, "mx": 615},
        "D4 Bahasa Inggris Terapan": {"mn": 530, "mx": 600},
        "D4 Akuntansi Sektor Publik": {"mn": 560, "mx": 630},
    },
    "Universitas Airlangga": {
        "D4 Teknologi Laboratorium Medis": {"mn": 560, "mx": 630},
        "D4 Fisioterapi": {"mn": 555, "mx": 625},
        "D4 Gizi Klinik": {"mn": 550, "mx": 620},
        "D4 Keperawatan": {"mn": 535, "mx": 605},
        "D4 Kebidanan": {"mn": 530, "mx": 600},
        "D4 Rekam Medis dan Informasi Kesehatan": {"mn": 540, "mx": 610},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 530, "mx": 600},
        "D4 Teknologi Pangan": {"mn": 540, "mx": 610},
        "D4 Akuntansi Sektor Publik": {"mn": 540, "mx": 610},
        "D4 Manajemen Pemasaran": {"mn": 530, "mx": 600},
        "D4 Keuangan dan Perbankan": {"mn": 530, "mx": 600},
        "D4 Administrasi Bisnis": {"mn": 520, "mx": 590},
        "D4 Manajemen Pariwisata": {"mn": 515, "mx": 585},
        "D4 Bahasa Inggris Terapan": {"mn": 510, "mx": 580},
        "D4 Rekayasa Perangkat Lunak": {"mn": 565, "mx": 635},
    },
    "Universitas Padjadjaran": {
        "D4 Teknologi Laboratorium Medis": {"mn": 545, "mx": 615},
        "D4 Fisioterapi": {"mn": 540, "mx": 610},
        "D4 Gizi Klinik": {"mn": 535, "mx": 605},
        "D4 Keperawatan": {"mn": 520, "mx": 590},
        "D4 Kebidanan": {"mn": 515, "mx": 585},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 515, "mx": 585},
        "D4 Teknologi Pangan": {"mn": 525, "mx": 595},
        "D4 Akuntansi Sektor Publik": {"mn": 525, "mx": 595},
        "D4 Manajemen Pemasaran": {"mn": 515, "mx": 585},
        "D4 Administrasi Bisnis": {"mn": 505, "mx": 575},
        "D4 Manajemen Pariwisata": {"mn": 505, "mx": 575},
        "D4 Bahasa Inggris Terapan": {"mn": 495, "mx": 565},
        "D4 Rekayasa Perangkat Lunak": {"mn": 550, "mx": 620},
        "D4 Teknologi Informasi": {"mn": 545, "mx": 615},
    },
    "Universitas Diponegoro": {
        "D4 Teknologi Laboratorium Medis": {"mn": 520, "mx": 590},
        "D4 Fisioterapi": {"mn": 515, "mx": 585},
        "D4 Gizi Klinik": {"mn": 510, "mx": 580},
        "D4 Keperawatan": {"mn": 495, "mx": 565},
        "D4 Kebidanan": {"mn": 490, "mx": 560},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 490, "mx": 560},
        "D4 Teknologi Pangan": {"mn": 500, "mx": 570},
        "D4 Akuntansi Sektor Publik": {"mn": 500, "mx": 570},
        "D4 Manajemen Pemasaran": {"mn": 490, "mx": 560},
        "D4 Administrasi Bisnis": {"mn": 480, "mx": 550},
        "D4 Teknik Geomatika": {"mn": 495, "mx": 565},
        "D4 Rekayasa Perangkat Lunak": {"mn": 525, "mx": 595},
        "D4 Teknologi Informasi": {"mn": 515, "mx": 585},
        "D4 Teknik Mekatronika": {"mn": 505, "mx": 575},
        "D4 Teknologi Rekayasa Kimia": {"mn": 490, "mx": 560},
    },
    "Universitas Brawijaya": {
        "D4 Teknologi Laboratorium Medis": {"mn": 505, "mx": 575},
        "D4 Gizi Klinik": {"mn": 495, "mx": 565},
        "D4 Keperawatan": {"mn": 480, "mx": 550},
        "D4 Kebidanan": {"mn": 475, "mx": 545},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 475, "mx": 545},
        "D4 Teknologi Pangan": {"mn": 490, "mx": 560},
        "D4 Akuntansi Sektor Publik": {"mn": 490, "mx": 560},
        "D4 Manajemen Pemasaran": {"mn": 475, "mx": 545},
        "D4 Administrasi Bisnis": {"mn": 465, "mx": 535},
        "D4 Rekayasa Perangkat Lunak": {"mn": 510, "mx": 580},
        "D4 Teknologi Informasi": {"mn": 500, "mx": 570},
        "D4 Teknik Pengairan Terapan": {"mn": 465, "mx": 535},
        "D4 Manajemen Agribisnis": {"mn": 465, "mx": 535},
    },
    "Universitas Sebelas Maret": {
        "D4 Teknologi Laboratorium Medis": {"mn": 495, "mx": 565},
        "D4 Fisioterapi": {"mn": 490, "mx": 560},
        "D4 Gizi Klinik": {"mn": 485, "mx": 555},
        "D4 Keperawatan": {"mn": 470, "mx": 540},
        "D4 Kebidanan": {"mn": 465, "mx": 535},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 465, "mx": 535},
        "D4 Teknologi Pangan": {"mn": 480, "mx": 550},
        "D4 Akuntansi Sektor Publik": {"mn": 480, "mx": 550},
        "D4 Manajemen Pemasaran": {"mn": 465, "mx": 535},
        "D4 Manajemen Pariwisata": {"mn": 455, "mx": 525},
        "D4 Usaha Perjalanan Wisata": {"mn": 450, "mx": 520},
        "D4 Bahasa Inggris Terapan": {"mn": 455, "mx": 525},
        "D4 Rekayasa Perangkat Lunak": {"mn": 495, "mx": 565},
        "D4 Teknologi Informasi": {"mn": 485, "mx": 555},
        "D4 Desain Komunikasi Visual": {"mn": 445, "mx": 515},
    },
    "Universitas Hasanuddin": {
        "D4 Teknologi Laboratorium Medis": {"mn": 485, "mx": 555},
        "D4 Fisioterapi": {"mn": 480, "mx": 550},
        "D4 Gizi Klinik": {"mn": 475, "mx": 545},
        "D4 Keperawatan": {"mn": 460, "mx": 530},
        "D4 Kebidanan": {"mn": 455, "mx": 525},
        "D4 Teknologi Pangan": {"mn": 465, "mx": 535},
        "D4 Akuntansi Sektor Publik": {"mn": 465, "mx": 535},
        "D4 Manajemen Pemasaran": {"mn": 450, "mx": 520},
        "D4 Administrasi Bisnis": {"mn": 445, "mx": 515},
        "D4 Rekayasa Perangkat Lunak": {"mn": 480, "mx": 550},
        "D4 Teknologi Informasi": {"mn": 470, "mx": 540},
        "D4 Teknik Geomatika": {"mn": 455, "mx": 525},
    },
    "Universitas Sumatera Utara": {
        "D4 Teknologi Laboratorium Medis": {"mn": 470, "mx": 540},
        "D4 Fisioterapi": {"mn": 455, "mx": 525},
        "D4 Gizi Klinik": {"mn": 460, "mx": 530},
        "D4 Keperawatan": {"mn": 445, "mx": 515},
        "D4 Kebidanan": {"mn": 440, "mx": 510},
        "D4 Teknologi Pangan": {"mn": 450, "mx": 520},
        "D4 Akuntansi Sektor Publik": {"mn": 450, "mx": 520},
        "D4 Manajemen Pemasaran": {"mn": 435, "mx": 505},
        "D4 Administrasi Bisnis": {"mn": 430, "mx": 500},
        "D4 Rekayasa Perangkat Lunak": {"mn": 465, "mx": 535},
        "D4 Teknologi Informasi": {"mn": 455, "mx": 525},
        "D4 Bahasa Inggris Terapan": {"mn": 430, "mx": 500},
    },
    "Universitas Andalas": {
        "D4 Teknologi Laboratorium Medis": {"mn": 455, "mx": 525},
        "D4 Gizi Klinik": {"mn": 450, "mx": 520},
        "D4 Keperawatan": {"mn": 435, "mx": 505},
        "D4 Kebidanan": {"mn": 430, "mx": 500},
        "D4 Teknologi Pangan": {"mn": 440, "mx": 510},
        "D4 Akuntansi Sektor Publik": {"mn": 440, "mx": 510},
        "D4 Manajemen Pemasaran": {"mn": 425, "mx": 495},
        "D4 Rekayasa Perangkat Lunak": {"mn": 455, "mx": 525},
        "D4 Teknologi Informasi": {"mn": 445, "mx": 515},
    },
    "Universitas Sriwijaya": {
        "D4 Gizi Klinik": {"mn": 430, "mx": 500},
        "D4 Keperawatan": {"mn": 415, "mx": 485},
        "D4 Kebidanan": {"mn": 410, "mx": 480},
        "D4 Teknologi Pangan": {"mn": 420, "mx": 490},
        "D4 Akuntansi Sektor Publik": {"mn": 420, "mx": 490},
        "D4 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D4 Rekayasa Perangkat Lunak": {"mn": 435, "mx": 505},
        "D4 Teknologi Informasi": {"mn": 425, "mx": 495},
    },
    "Universitas Udayana": {
        "D4 Teknologi Laboratorium Medis": {"mn": 455, "mx": 525},
        "D4 Fisioterapi": {"mn": 450, "mx": 520},
        "D4 Gizi Klinik": {"mn": 445, "mx": 515},
        "D4 Keperawatan": {"mn": 430, "mx": 500},
        "D4 Kebidanan": {"mn": 425, "mx": 495},
        "D4 Teknologi Pangan": {"mn": 435, "mx": 505},
        "D4 Akuntansi Sektor Publik": {"mn": 440, "mx": 510},
        "D4 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D4 Administrasi Bisnis": {"mn": 415, "mx": 485},
        "D4 Manajemen Pariwisata": {"mn": 440, "mx": 510},
        "D4 Rekayasa Perangkat Lunak": {"mn": 450, "mx": 520},
        "D4 Teknologi Informasi": {"mn": 440, "mx": 510},
    },
    "Universitas Jember": {
        "D4 Gizi Klinik": {"mn": 430, "mx": 500},
        "D4 Keperawatan": {"mn": 415, "mx": 485},
        "D4 Kebidanan": {"mn": 410, "mx": 480},
        "D4 Teknologi Pangan": {"mn": 425, "mx": 495},
        "D4 Akuntansi Sektor Publik": {"mn": 420, "mx": 490},
        "D4 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D4 Manajemen Agribisnis": {"mn": 400, "mx": 470},
        "D4 Rekayasa Perangkat Lunak": {"mn": 435, "mx": 505},
        "D4 Teknologi Informasi": {"mn": 425, "mx": 495},
    },
    "Universitas Lampung": {
        "D4 Keperawatan": {"mn": 405, "mx": 475},
        "D4 Kebidanan": {"mn": 400, "mx": 470},
        "D4 Akuntansi Sektor Publik": {"mn": 410, "mx": 480},
        "D4 Manajemen Pemasaran": {"mn": 415, "mx": 485},
        "D4 Rekayasa Perangkat Lunak": {"mn": 420, "mx": 490},
        "D4 Teknologi Informasi": {"mn": 410, "mx": 480},
    },
    "Universitas Negeri Yogyakarta": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 490, "mx": 560},
        "D4 Teknologi Informasi": {"mn": 480, "mx": 550},
        "D4 Teknik Otomasi Industri": {"mn": 470, "mx": 540},
        "D4 Manajemen Pemasaran": {"mn": 440, "mx": 510},
        "D4 Akuntansi Manajerial": {"mn": 445, "mx": 515},
        "D4 Tata Boga": {"mn": 420, "mx": 490},
        "D4 Tata Busana": {"mn": 415, "mx": 485},
    },
    "Universitas Negeri Malang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 480, "mx": 550},
        "D4 Teknologi Informasi": {"mn": 470, "mx": 540},
        "D4 Teknik Otomasi Industri": {"mn": 460, "mx": 530},
        "D4 Manajemen Pemasaran": {"mn": 430, "mx": 500},
        "D4 Akuntansi Manajerial": {"mn": 435, "mx": 505},
    },
    "Universitas Negeri Semarang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 465, "mx": 535},
        "D4 Teknologi Informasi": {"mn": 455, "mx": 525},
        "D4 Akuntansi Manajerial": {"mn": 420, "mx": 490},
        "D4 Manajemen Pemasaran": {"mn": 415, "mx": 485},
        "D4 Tata Boga": {"mn": 405, "mx": 475},
    },
    "Universitas Pendidikan Indonesia": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 470, "mx": 540},
        "D4 Teknologi Informasi": {"mn": 460, "mx": 530},
        "D4 Teknik Otomasi Industri": {"mn": 455, "mx": 525},
        "D4 Akuntansi Manajerial": {"mn": 430, "mx": 500},
        "D4 Manajemen Pemasaran": {"mn": 425, "mx": 495},
        "D4 Bahasa Inggris Terapan": {"mn": 435, "mx": 505},
        "D4 Tata Boga": {"mn": 410, "mx": 480},
        "D4 Tata Busana": {"mn": 405, "mx": 475},
    },
}


# ══════════════════════════════════════════════════════════
# DATABASE PRODI S1 AKURAT PER KAMPUS
# Sumber: website resmi masing-masing PTN & SNPMB 2022-2024
# ══════════════════════════════════════════════════════════
PTN_PRODI_S1 = {
    "Universitas Indonesia": {
        # FK / FKG / FF / FIK
        "Pendidikan Dokter": {"mn": 760, "mx": 830},
        "Kedokteran Gigi": {"mn": 710, "mx": 780},
        "Farmasi": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 620, "mx": 690},
        "Kesehatan Masyarakat": {"mn": 620, "mx": 690},
        "Gizi": {"mn": 620, "mx": 685},
        "Ilmu Keolahragaan": {"mn": 560, "mx": 630},
        # FTUI
        "Teknik Sipil": {"mn": 660, "mx": 730},
        "Teknik Mesin": {"mn": 660, "mx": 730},
        "Teknik Elektro": {"mn": 690, "mx": 760},
        "Teknik Kimia": {"mn": 660, "mx": 730},
        "Teknik Industri": {"mn": 700, "mx": 770},
        "Teknik Lingkungan": {"mn": 640, "mx": 710},
        "Teknik Metalurgi dan Material": {"mn": 630, "mx": 700},
        "Teknik Perkapalan": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 670, "mx": 740},
        "Teknik Komputer": {"mn": 700, "mx": 770},
        # FMIPA
        "Matematika": {"mn": 640, "mx": 710},
        "Fisika": {"mn": 630, "mx": 700},
        "Kimia": {"mn": 640, "mx": 710},
        "Biologi": {"mn": 640, "mx": 710},
        "Ilmu Komputer": {"mn": 730, "mx": 800},
        "Statistika": {"mn": 660, "mx": 730},
        "Geografi": {"mn": 620, "mx": 690},
        # FH
        "Ilmu Hukum": {"mn": 680, "mx": 750},
        # FEB
        "Ilmu Ekonomi": {"mn": 670, "mx": 740},
        "Akuntansi": {"mn": 700, "mx": 770},
        "Manajemen": {"mn": 710, "mx": 780},
        # FISIP
        "Ilmu Komunikasi": {"mn": 680, "mx": 750},
        "Hubungan Internasional": {"mn": 700, "mx": 770},
        "Sosiologi": {"mn": 640, "mx": 710},
        "Ilmu Politik": {"mn": 650, "mx": 720},
        "Ilmu Administrasi Fiskal": {"mn": 650, "mx": 720},
        "Ilmu Administrasi Niaga": {"mn": 660, "mx": 730},
        "Administrasi Negara": {"mn": 650, "mx": 720},
        "Ilmu Perpustakaan": {"mn": 590, "mx": 660},
        "Ilmu Kesejahteraan Sosial": {"mn": 620, "mx": 690},
        "Kriminologi": {"mn": 640, "mx": 710},
        # FIB
        "Sastra Indonesia": {"mn": 600, "mx": 670},
        "Sastra Inggris": {"mn": 630, "mx": 700},
        "Sastra Arab": {"mn": 590, "mx": 660},
        "Sastra Jepang": {"mn": 620, "mx": 690},
        "Sastra Belanda": {"mn": 580, "mx": 650},
        "Sastra Prancis": {"mn": 580, "mx": 650},
        "Sastra Cina": {"mn": 590, "mx": 660},
        "Filsafat": {"mn": 600, "mx": 670},
        # FPsi
        "Psikologi": {"mn": 680, "mx": 750},
        # FIA
        "Administrasi Bisnis": {"mn": 640, "mx": 710},
    },
    "Institut Teknologi Bandung": {
        # FTSL
        "Teknik Sipil": {"mn": 720, "mx": 790},
        "Teknik Lingkungan": {"mn": 700, "mx": 770},
        "Teknik Kelautan": {"mn": 680, "mx": 750},
        # FTMD
        "Teknik Mesin": {"mn": 730, "mx": 800},
        "Teknik Material": {"mn": 700, "mx": 770},
        "Teknik Dirgantara": {"mn": 710, "mx": 780},
        # FTTM
        "Teknik Pertambangan": {"mn": 690, "mx": 760},
        "Teknik Perminyakan": {"mn": 720, "mx": 790},
        "Teknik Geologi": {"mn": 700, "mx": 770},
        "Teknik Geodesi dan Geomatika": {"mn": 690, "mx": 760},
        "Meteorologi": {"mn": 680, "mx": 750},
        "Oseanografi": {"mn": 680, "mx": 750},
        # FTIF
        "Teknik Informatika": {"mn": 800, "mx": 870},
        "Sistem dan Teknologi Informasi": {"mn": 790, "mx": 860},
        # FTEIC
        "Teknik Elektro": {"mn": 760, "mx": 830},
        "Teknik Fisika": {"mn": 720, "mx": 790},
        "Teknik Tenaga Listrik": {"mn": 720, "mx": 790},
        "Teknik Telekomunikasi": {"mn": 730, "mx": 800},
        "Teknik Biomedis": {"mn": 720, "mx": 790},
        # FTI
        "Teknik Kimia": {"mn": 730, "mx": 800},
        "Teknik Industri": {"mn": 770, "mx": 840},
        "Manajemen Rekayasa": {"mn": 750, "mx": 820},
        # FMIPA
        "Matematika": {"mn": 720, "mx": 790},
        "Fisika": {"mn": 710, "mx": 780},
        "Kimia": {"mn": 720, "mx": 790},
        "Biologi": {"mn": 700, "mx": 770},
        "Astronomi": {"mn": 700, "mx": 770},
        "Aktuaria": {"mn": 750, "mx": 820},
        # SAPPK
        "Arsitektur": {"mn": 750, "mx": 820},
        "Perencanaan Wilayah dan Kota": {"mn": 730, "mx": 800},
        # FSRD
        "Desain Produk": {"mn": 720, "mx": 790},
        "Desain Komunikasi Visual": {"mn": 730, "mx": 800},
        "Seni Rupa": {"mn": 680, "mx": 750},
        "Kriya": {"mn": 670, "mx": 740},
        # SBM
        "Manajemen": {"mn": 780, "mx": 850},
        "Kewirausahaan": {"mn": 750, "mx": 820},
        # SF
        "Farmasi": {"mn": 740, "mx": 810},
        # SITH
        "Bioteknologi": {"mn": 720, "mx": 790},
        "Rekayasa Hayati": {"mn": 710, "mx": 780},
        "Rekayasa Pertanian": {"mn": 680, "mx": 750},
    },
    "Institut Teknologi Sepuluh Nopember": {
        # FTK
        "Teknik Perkapalan": {"mn": 630, "mx": 700},
        "Teknik Sistem Perkapalan": {"mn": 610, "mx": 680},
        "Teknik Kelautan": {"mn": 620, "mx": 690},
        "Transportasi Laut": {"mn": 600, "mx": 670},
        # FTI
        "Teknik Industri": {"mn": 670, "mx": 740},
        "Teknik Kimia": {"mn": 660, "mx": 730},
        "Teknik Material dan Metalurgi": {"mn": 630, "mx": 700},
        "Teknik Fisika": {"mn": 630, "mx": 700},
        "Teknik Geofisika": {"mn": 620, "mx": 690},
        # FTEIC
        "Teknik Elektro": {"mn": 700, "mx": 770},
        "Teknik Komputer": {"mn": 690, "mx": 760},
        "Teknik Informatika": {"mn": 740, "mx": 810},
        "Sistem Informasi": {"mn": 690, "mx": 760},
        "Teknologi Informasi": {"mn": 700, "mx": 770},
        # FTSP
        "Teknik Sipil": {"mn": 640, "mx": 710},
        "Teknik Lingkungan": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 670, "mx": 740},
        "Perencanaan Wilayah dan Kota": {"mn": 650, "mx": 720},
        "Desain Produk Industri": {"mn": 650, "mx": 720},
        "Desain Interior": {"mn": 640, "mx": 710},
        # FV (Teknik Mesin ada di ITS)
        "Teknik Mesin": {"mn": 640, "mx": 710},
        # FMKSD
        "Matematika": {"mn": 660, "mx": 730},
        "Fisika": {"mn": 630, "mx": 700},
        "Kimia": {"mn": 640, "mx": 710},
        "Biologi": {"mn": 610, "mx": 680},
        "Statistika": {"mn": 660, "mx": 730},
        "Aktuaria": {"mn": 670, "mx": 740},
        # SB
        "Manajemen Bisnis": {"mn": 680, "mx": 750},
        "Studi Pembangunan": {"mn": 610, "mx": 680},
    },
    "Institut Pertanian Bogor": {
        # FAPERTA
        "Agronomi dan Hortikultura": {"mn": 600, "mx": 670},
        "Ilmu Tanah": {"mn": 580, "mx": 650},
        "Proteksi Tanaman": {"mn": 590, "mx": 660},
        "Arsitektur Lanskap": {"mn": 620, "mx": 690},
        # FMIPA
        "Matematika": {"mn": 630, "mx": 700},
        "Statistika": {"mn": 650, "mx": 720},
        "Ilmu Komputer": {"mn": 680, "mx": 750},
        "Fisika": {"mn": 600, "mx": 670},
        "Kimia": {"mn": 605, "mx": 675},
        "Biologi": {"mn": 610, "mx": 680},
        "Biokimia": {"mn": 625, "mx": 695},
        "Meteorologi Terapan": {"mn": 590, "mx": 660},
        # FKH
        "Kedokteran Hewan": {"mn": 660, "mx": 730},
        # FPIK
        "Budidaya Perairan": {"mn": 590, "mx": 660},
        "Manajemen Sumber Daya Perairan": {"mn": 580, "mx": 650},
        "Ilmu Kelautan": {"mn": 600, "mx": 670},
        "Teknologi Hasil Perairan": {"mn": 580, "mx": 650},
        # FEM
        "Ekonomi Sumber Daya dan Lingkungan": {"mn": 610, "mx": 680},
        "Agribisnis": {"mn": 635, "mx": 705},
        "Ekonomi Syariah": {"mn": 590, "mx": 660},
        "Manajemen": {"mn": 650, "mx": 720},
        # FATETA / FTK
        "Teknologi Pangan": {"mn": 645, "mx": 715},
        "Ilmu Gizi": {"mn": 645, "mx": 715},
        "Teknik Pertanian dan Biosistem": {"mn": 610, "mx": 680},
        "Teknik Kimia": {"mn": 620, "mx": 690},
        # FAHUTAN
        "Manajemen Hutan": {"mn": 590, "mx": 660},
        "Teknologi Hasil Hutan": {"mn": 580, "mx": 650},
        "Konservasi Sumber Daya Hutan dan Ekowisata": {"mn": 590, "mx": 660},
        "Silvikultur": {"mn": 580, "mx": 650},
        # FAPET
        "Ilmu Nutrisi dan Teknologi Pakan": {"mn": 580, "mx": 650},
        "Teknologi Produksi Ternak": {"mn": 580, "mx": 650},
        # FEMA
        "Ilmu Keluarga dan Konsumen": {"mn": 600, "mx": 670},
        "Komunikasi dan Pengembangan Masyarakat": {"mn": 610, "mx": 680},
    },
    "Universitas Gadjah Mada": {
        # FK
        "Pendidikan Dokter": {"mn": 770, "mx": 840},
        "Ilmu Keperawatan": {"mn": 630, "mx": 700},
        "Gizi Kesehatan": {"mn": 650, "mx": 720},
        "Kedokteran Gigi": {"mn": 730, "mx": 800},
        "Kesehatan Masyarakat": {"mn": 635, "mx": 705},
        # FF
        "Farmasi": {"mn": 700, "mx": 770},
        # FT
        "Teknik Sipil": {"mn": 690, "mx": 760},
        "Teknik Mesin": {"mn": 690, "mx": 760},
        "Teknik Elektro": {"mn": 720, "mx": 790},
        "Teknik Kimia": {"mn": 700, "mx": 770},
        "Teknik Industri": {"mn": 730, "mx": 800},
        "Teknik Fisika": {"mn": 680, "mx": 750},
        "Teknik Nuklir dan Teknik Fisika": {"mn": 680, "mx": 750},
        "Teknik Geodesi": {"mn": 680, "mx": 750},
        "Teknik Geologi": {"mn": 685, "mx": 755},
        "Perencanaan Wilayah dan Kota": {"mn": 700, "mx": 770},
        "Arsitektur": {"mn": 720, "mx": 790},
        "Teknik Informatika": {"mn": 770, "mx": 840},
        "Ilmu Komputer": {"mn": 760, "mx": 830},
        "Teknologi Informasi": {"mn": 750, "mx": 820},
        # FMIPA
        "Matematika": {"mn": 660, "mx": 730},
        "Fisika": {"mn": 650, "mx": 720},
        "Kimia": {"mn": 660, "mx": 730},
        "Biologi": {"mn": 650, "mx": 720},
        "Statistika": {"mn": 680, "mx": 750},
        "Geofisika": {"mn": 640, "mx": 710},
        "Elektronika dan Instrumentasi": {"mn": 660, "mx": 730},
        # FH
        "Ilmu Hukum": {"mn": 700, "mx": 770},
        # FEB
        "Ilmu Ekonomi": {"mn": 690, "mx": 760},
        "Akuntansi": {"mn": 720, "mx": 790},
        "Manajemen": {"mn": 730, "mx": 800},
        # FISIPOL
        "Ilmu Komunikasi": {"mn": 690, "mx": 760},
        "Manajemen dan Kebijakan Publik": {"mn": 670, "mx": 740},
        "Sosiologi": {"mn": 650, "mx": 720},
        "Ilmu Politik": {"mn": 660, "mx": 730},
        "Pembangunan Sosial dan Kesejahteraan": {"mn": 640, "mx": 710},
        "Hubungan Internasional": {"mn": 710, "mx": 780},
        # FPN / Pertanian
        "Agronomi": {"mn": 610, "mx": 680},
        "Ilmu Tanah": {"mn": 590, "mx": 660},
        "Proteksi Tanaman": {"mn": 600, "mx": 670},
        "Teknologi Pangan dan Hasil Pertanian": {"mn": 625, "mx": 695},
        "Agribisnis": {"mn": 640, "mx": 710},
        "Penyuluhan dan Komunikasi Pertanian": {"mn": 590, "mx": 660},
        # FKH
        "Kedokteran Hewan": {"mn": 660, "mx": 730},
        # Kehutanan
        "Kehutanan": {"mn": 610, "mx": 680},
        # Peternakan
        "Peternakan": {"mn": 600, "mx": 670},
        # FIB
        "Sastra Indonesia": {"mn": 600, "mx": 670},
        "Sastra Inggris": {"mn": 640, "mx": 710},
        "Sastra Arab": {"mn": 590, "mx": 660},
        "Sastra Jawa": {"mn": 560, "mx": 630},
        "Arkeologi": {"mn": 590, "mx": 660},
        "Sejarah": {"mn": 590, "mx": 660},
        "Antropologi Budaya": {"mn": 600, "mx": 670},
        "Pariwisata": {"mn": 620, "mx": 690},
        "Bahasa Korea": {"mn": 610, "mx": 680},
        "Bahasa dan Sastra Prancis": {"mn": 600, "mx": 670},
        # Filsafat
        "Filsafat": {"mn": 595, "mx": 665},
        # FPsi
        "Psikologi": {"mn": 700, "mx": 770},
        # FGE
        "Geografi Lingkungan": {"mn": 620, "mx": 690},
        "Kartografi dan Penginderaan Jauh": {"mn": 610, "mx": 680},
        "Pembangunan Wilayah": {"mn": 620, "mx": 690},
    },
    "Universitas Airlangga": {
        # FK
        "Pendidikan Dokter": {"mn": 740, "mx": 810},
        "Ilmu Keperawatan": {"mn": 610, "mx": 680},
        "Ilmu Gizi": {"mn": 620, "mx": 690},
        "Kedokteran Gigi": {"mn": 700, "mx": 770},
        # FKM
        "Kesehatan Masyarakat": {"mn": 610, "mx": 680},
        # FF
        "Farmasi": {"mn": 680, "mx": 750},
        # FKH
        "Kedokteran Hewan": {"mn": 650, "mx": 720},
        # FST
        "Matematika": {"mn": 610, "mx": 680},
        "Fisika": {"mn": 590, "mx": 660},
        "Kimia": {"mn": 610, "mx": 680},
        "Biologi": {"mn": 610, "mx": 680},
        "Ilmu Komputer": {"mn": 670, "mx": 740},
        "Statistika": {"mn": 630, "mx": 700},
        "Teknik Lingkungan": {"mn": 605, "mx": 675},
        # FH
        "Ilmu Hukum": {"mn": 660, "mx": 730},
        # FEB
        "Ilmu Ekonomi": {"mn": 650, "mx": 720},
        "Akuntansi": {"mn": 680, "mx": 750},
        "Manajemen": {"mn": 690, "mx": 760},
        "Ekonomi Islam": {"mn": 625, "mx": 695},
        # FISIP
        "Ilmu Komunikasi": {"mn": 650, "mx": 720},
        "Hubungan Internasional": {"mn": 670, "mx": 740},
        "Sosiologi": {"mn": 610, "mx": 680},
        "Ilmu Politik": {"mn": 620, "mx": 690},
        "Ilmu Informasi dan Perpustakaan": {"mn": 570, "mx": 640},
        "Ilmu Kesejahteraan Sosial": {"mn": 590, "mx": 660},
        "Administrasi Publik": {"mn": 610, "mx": 680},
        "Administrasi Bisnis": {"mn": 620, "mx": 690},
        # FPsi
        "Psikologi": {"mn": 670, "mx": 740},
        # FIB
        "Sastra Indonesia": {"mn": 570, "mx": 640},
        "Sastra Inggris": {"mn": 610, "mx": 680},
        "Sastra Jepang": {"mn": 590, "mx": 660},
    },
    "Universitas Padjadjaran": {
        # FK
        "Pendidikan Dokter": {"mn": 730, "mx": 800},
        "Ilmu Keperawatan": {"mn": 600, "mx": 670},
        "Ilmu Gizi": {"mn": 610, "mx": 680},
        "Kedokteran Gigi": {"mn": 690, "mx": 760},
        # FKM
        "Kesehatan Masyarakat": {"mn": 600, "mx": 670},
        # FF
        "Farmasi": {"mn": 660, "mx": 730},
        # FKH
        "Kedokteran Hewan": {"mn": 630, "mx": 700},
        # FMIPA
        "Matematika": {"mn": 600, "mx": 670},
        "Fisika": {"mn": 580, "mx": 650},
        "Kimia": {"mn": 600, "mx": 670},
        "Biologi": {"mn": 600, "mx": 670},
        "Ilmu Komputer": {"mn": 660, "mx": 730},
        "Statistika": {"mn": 620, "mx": 690},
        "Geofisika": {"mn": 590, "mx": 660},
        # FT
        "Teknik Informatika": {"mn": 680, "mx": 750},
        "Teknik Elektro": {"mn": 650, "mx": 720},
        "Teknik Industri": {"mn": 650, "mx": 720},
        "Teknik Geologi": {"mn": 620, "mx": 690},
        "Teknik Pertambangan": {"mn": 610, "mx": 680},
        # FH
        "Ilmu Hukum": {"mn": 640, "mx": 710},
        # FEB
        "Ilmu Ekonomi": {"mn": 640, "mx": 710},
        "Akuntansi": {"mn": 660, "mx": 730},
        "Manajemen": {"mn": 670, "mx": 740},
        "Bisnis Digital": {"mn": 640, "mx": 710},
        # FISIP
        "Ilmu Komunikasi": {"mn": 650, "mx": 720},
        "Hubungan Internasional": {"mn": 660, "mx": 730},
        "Sosiologi": {"mn": 600, "mx": 670},
        "Ilmu Politik": {"mn": 610, "mx": 680},
        "Administrasi Publik": {"mn": 600, "mx": 670},
        "Kesejahteraan Sosial": {"mn": 580, "mx": 650},
        # FIB
        "Sastra Indonesia": {"mn": 570, "mx": 640},
        "Sastra Inggris": {"mn": 610, "mx": 680},
        "Sastra Arab": {"mn": 570, "mx": 640},
        "Sastra Jepang": {"mn": 590, "mx": 660},
        "Sastra Jerman": {"mn": 570, "mx": 640},
        "Sastra Prancis": {"mn": 570, "mx": 640},
        "Sejarah": {"mn": 560, "mx": 630},
        # FPsi
        "Psikologi": {"mn": 660, "mx": 730},
        # FPIK
        "Ilmu Kelautan": {"mn": 580, "mx": 650},
        "Perikanan": {"mn": 570, "mx": 640},
        # FAPERTA
        "Agribisnis": {"mn": 600, "mx": 670},
        "Agroteknologi": {"mn": 590, "mx": 660},
        # FAPET
        "Peternakan": {"mn": 570, "mx": 640},
    },
    "Universitas Diponegoro": {
        "Pendidikan Dokter": {"mn": 710, "mx": 780},
        "Ilmu Keperawatan": {"mn": 590, "mx": 660},
        "Kesehatan Masyarakat": {"mn": 590, "mx": 660},
        "Ilmu Gizi": {"mn": 590, "mx": 660},
        "Kedokteran Gigi": {"mn": 660, "mx": 730},
        "Farmasi": {"mn": 630, "mx": 700},
        "Teknik Sipil": {"mn": 640, "mx": 710},
        "Teknik Mesin": {"mn": 640, "mx": 710},
        "Teknik Elektro": {"mn": 660, "mx": 730},
        "Teknik Kimia": {"mn": 650, "mx": 720},
        "Teknik Industri": {"mn": 660, "mx": 730},
        "Teknik Lingkungan": {"mn": 620, "mx": 690},
        "Teknik Geologi": {"mn": 620, "mx": 690},
        "Teknik Perkapalan": {"mn": 610, "mx": 680},
        "Arsitektur": {"mn": 650, "mx": 720},
        "Perencanaan Wilayah dan Kota": {"mn": 640, "mx": 710},
        "Teknik Informatika": {"mn": 690, "mx": 760},
        "Sistem Komputer": {"mn": 655, "mx": 725},
        "Matematika": {"mn": 600, "mx": 670},
        "Fisika": {"mn": 580, "mx": 650},
        "Kimia": {"mn": 590, "mx": 660},
        "Biologi": {"mn": 580, "mx": 650},
        "Statistika": {"mn": 610, "mx": 680},
        "Ilmu Hukum": {"mn": 620, "mx": 690},
        "Ilmu Ekonomi": {"mn": 620, "mx": 690},
        "Akuntansi": {"mn": 640, "mx": 710},
        "Manajemen": {"mn": 650, "mx": 720},
        "Perpajakan": {"mn": 610, "mx": 680},
        "Ilmu Komunikasi": {"mn": 630, "mx": 700},
        "Hubungan Internasional": {"mn": 640, "mx": 710},
        "Administrasi Publik": {"mn": 590, "mx": 660},
        "Ilmu Politik": {"mn": 590, "mx": 660},
        "Ilmu Pemerintahan": {"mn": 590, "mx": 660},
        "Psikologi": {"mn": 640, "mx": 710},
        "Sastra Indonesia": {"mn": 555, "mx": 625},
        "Sastra Inggris": {"mn": 590, "mx": 660},
        "Ilmu Kelautan": {"mn": 570, "mx": 640},
        "Perikanan": {"mn": 560, "mx": 630},
        "Peternakan": {"mn": 550, "mx": 620},
        "Agribisnis": {"mn": 570, "mx": 640},
        "Teknologi Pangan": {"mn": 590, "mx": 660},
        "Ilmu Keolahragaan": {"mn": 530, "mx": 600},
    },
    "Universitas Brawijaya": {
        "Pendidikan Dokter": {"mn": 710, "mx": 780},
        "Ilmu Keperawatan": {"mn": 580, "mx": 650},
        "Ilmu Gizi": {"mn": 590, "mx": 660},
        "Kesehatan Masyarakat": {"mn": 580, "mx": 650},
        "Kedokteran Gigi": {"mn": 650, "mx": 720},
        "Farmasi": {"mn": 620, "mx": 690},
        "Kedokteran Hewan": {"mn": 620, "mx": 690},
        "Teknik Sipil": {"mn": 620, "mx": 690},
        "Teknik Mesin": {"mn": 620, "mx": 690},
        "Teknik Elektro": {"mn": 640, "mx": 710},
        "Teknik Kimia": {"mn": 630, "mx": 700},
        "Teknik Industri": {"mn": 640, "mx": 710},
        "Teknik Pengairan": {"mn": 590, "mx": 660},
        "Arsitektur": {"mn": 640, "mx": 710},
        "Teknik Informatika": {"mn": 680, "mx": 750},
        "Sistem Informasi": {"mn": 650, "mx": 720},
        "Teknologi Informasi": {"mn": 640, "mx": 710},
        "Teknik Komputer": {"mn": 640, "mx": 710},
        "Matematika": {"mn": 580, "mx": 650},
        "Fisika": {"mn": 560, "mx": 630},
        "Kimia": {"mn": 570, "mx": 640},
        "Biologi": {"mn": 570, "mx": 640},
        "Statistika": {"mn": 590, "mx": 660},
        "Ilmu Hukum": {"mn": 600, "mx": 670},
        "Ilmu Ekonomi": {"mn": 600, "mx": 670},
        "Akuntansi": {"mn": 620, "mx": 690},
        "Manajemen": {"mn": 630, "mx": 700},
        "Ilmu Komunikasi": {"mn": 610, "mx": 680},
        "Hubungan Internasional": {"mn": 620, "mx": 690},
        "Sosiologi": {"mn": 570, "mx": 640},
        "Ilmu Politik": {"mn": 570, "mx": 640},
        "Administrasi Bisnis": {"mn": 590, "mx": 660},
        "Administrasi Publik": {"mn": 575, "mx": 645},
        "Psikologi": {"mn": 630, "mx": 700},
        "Sastra Indonesia": {"mn": 540, "mx": 610},
        "Sastra Inggris": {"mn": 580, "mx": 650},
        "Sastra Jepang": {"mn": 560, "mx": 630},
        "Agribisnis": {"mn": 570, "mx": 640},
        "Agroekoteknologi": {"mn": 560, "mx": 630},
        "Kehutanan": {"mn": 560, "mx": 630},
        "Peternakan": {"mn": 550, "mx": 620},
        "Ilmu Kelautan": {"mn": 560, "mx": 630},
        "Budidaya Perairan": {"mn": 550, "mx": 620},
        "Teknologi Pangan": {"mn": 580, "mx": 650},
        "Ilmu Tanah": {"mn": 550, "mx": 620},
    },
    "Universitas Sebelas Maret": {
        "Pendidikan Dokter": {"mn": 700, "mx": 770},
        "Ilmu Keperawatan": {"mn": 570, "mx": 640},
        "Ilmu Gizi": {"mn": 580, "mx": 650},
        "Kesehatan Masyarakat": {"mn": 570, "mx": 640},
        "Kedokteran Gigi": {"mn": 640, "mx": 710},
        "Farmasi": {"mn": 610, "mx": 680},
        "Teknik Sipil": {"mn": 610, "mx": 680},
        "Teknik Mesin": {"mn": 610, "mx": 680},
        "Teknik Elektro": {"mn": 620, "mx": 690},
        "Teknik Kimia": {"mn": 610, "mx": 680},
        "Teknik Industri": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 630, "mx": 700},
        "Teknik Informatika": {"mn": 660, "mx": 730},
        "Informatika": {"mn": 655, "mx": 725},
        "Matematika": {"mn": 570, "mx": 640},
        "Fisika": {"mn": 550, "mx": 620},
        "Kimia": {"mn": 560, "mx": 630},
        "Biologi": {"mn": 560, "mx": 630},
        "Statistika": {"mn": 580, "mx": 650},
        "Ilmu Hukum": {"mn": 590, "mx": 660},
        "Ilmu Ekonomi": {"mn": 590, "mx": 660},
        "Akuntansi": {"mn": 610, "mx": 680},
        "Manajemen": {"mn": 620, "mx": 690},
        "Ilmu Komunikasi": {"mn": 600, "mx": 670},
        "Hubungan Internasional": {"mn": 610, "mx": 680},
        "Sosiologi": {"mn": 560, "mx": 630},
        "Ilmu Politik": {"mn": 560, "mx": 630},
        "Administrasi Negara": {"mn": 565, "mx": 635},
        "Psikologi": {"mn": 620, "mx": 690},
        "Sastra Indonesia": {"mn": 530, "mx": 600},
        "Sastra Inggris": {"mn": 570, "mx": 640},
        "Sastra Jawa": {"mn": 510, "mx": 580},
        "Sastra Daerah (Jawa)": {"mn": 505, "mx": 575},
        "Sejarah": {"mn": 520, "mx": 590},
        "Seni Rupa Murni": {"mn": 500, "mx": 570},
        "Kriya Seni": {"mn": 490, "mx": 560},
        "Agribisnis": {"mn": 550, "mx": 620},
        "Agroteknologi": {"mn": 540, "mx": 610},
        "Peternakan": {"mn": 530, "mx": 600},
        "Ilmu Tanah": {"mn": 530, "mx": 600},
        "Kehutanan": {"mn": 535, "mx": 605},
        "Teknologi Pangan": {"mn": 560, "mx": 630},
        "Pendidikan Matematika": {"mn": 565, "mx": 635},
        "Pendidikan Biologi": {"mn": 545, "mx": 615},
        "Pendidikan Kimia": {"mn": 545, "mx": 615},
        "Pendidikan Fisika": {"mn": 545, "mx": 615},
        "Pendidikan Bahasa Inggris": {"mn": 570, "mx": 640},
        "Pendidikan Bahasa Indonesia": {"mn": 530, "mx": 600},
        "Pendidikan Ekonomi": {"mn": 540, "mx": 610},
        "Pendidikan Sejarah": {"mn": 510, "mx": 580},
        "Pendidikan Sosiologi Antropologi": {"mn": 510, "mx": 580},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 510, "mx": 580},
    },
    "Universitas Hasanuddin": {
        "Pendidikan Dokter": {"mn": 690, "mx": 760},
        "Ilmu Keperawatan": {"mn": 560, "mx": 630},
        "Ilmu Gizi": {"mn": 570, "mx": 640},
        "Kesehatan Masyarakat": {"mn": 560, "mx": 630},
        "Kedokteran Gigi": {"mn": 640, "mx": 710},
        "Farmasi": {"mn": 600, "mx": 670},
        "Kedokteran Hewan": {"mn": 590, "mx": 660},
        "Teknik Sipil": {"mn": 600, "mx": 670},
        "Teknik Mesin": {"mn": 600, "mx": 670},
        "Teknik Elektro": {"mn": 620, "mx": 690},
        "Teknik Kimia": {"mn": 600, "mx": 670},
        "Teknik Industri": {"mn": 610, "mx": 680},
        "Teknik Geologi": {"mn": 600, "mx": 670},
        "Teknik Perminyakan": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 620, "mx": 690},
        "Perencanaan Wilayah dan Kota": {"mn": 600, "mx": 670},
        "Teknik Informatika": {"mn": 650, "mx": 720},
        "Sistem Informasi": {"mn": 620, "mx": 690},
        "Teknik Lingkungan": {"mn": 590, "mx": 660},
        "Teknik Kelautan": {"mn": 580, "mx": 650},
        "Matematika": {"mn": 560, "mx": 630},
        "Fisika": {"mn": 540, "mx": 610},
        "Kimia": {"mn": 550, "mx": 620},
        "Biologi": {"mn": 550, "mx": 620},
        "Statistika": {"mn": 570, "mx": 640},
        "Ilmu Hukum": {"mn": 580, "mx": 650},
        "Ilmu Ekonomi": {"mn": 580, "mx": 650},
        "Akuntansi": {"mn": 600, "mx": 670},
        "Manajemen": {"mn": 610, "mx": 680},
        "Ilmu Komunikasi": {"mn": 590, "mx": 660},
        "Hubungan Internasional": {"mn": 600, "mx": 670},
        "Sosiologi": {"mn": 550, "mx": 620},
        "Ilmu Politik": {"mn": 555, "mx": 625},
        "Administrasi Negara": {"mn": 560, "mx": 630},
        "Ilmu Pemerintahan": {"mn": 560, "mx": 630},
        "Psikologi": {"mn": 610, "mx": 680},
        "Sastra Indonesia": {"mn": 520, "mx": 590},
        "Sastra Inggris": {"mn": 560, "mx": 630},
        "Sejarah": {"mn": 510, "mx": 580},
        "Agribisnis": {"mn": 540, "mx": 610},
        "Agroteknologi": {"mn": 530, "mx": 600},
        "Kehutanan": {"mn": 530, "mx": 600},
        "Peternakan": {"mn": 520, "mx": 590},
        "Ilmu Kelautan": {"mn": 540, "mx": 610},
        "Budidaya Perairan": {"mn": 530, "mx": 600},
        "Teknologi Pangan": {"mn": 560, "mx": 630},
    },
    "Universitas Sumatera Utara": {
        "Pendidikan Dokter": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 550, "mx": 620},
        "Ilmu Gizi": {"mn": 560, "mx": 630},
        "Kesehatan Masyarakat": {"mn": 550, "mx": 620},
        "Kedokteran Gigi": {"mn": 630, "mx": 700},
        "Farmasi": {"mn": 590, "mx": 660},
        "Teknik Sipil": {"mn": 590, "mx": 660},
        "Teknik Mesin": {"mn": 590, "mx": 660},
        "Teknik Elektro": {"mn": 610, "mx": 680},
        "Teknik Kimia": {"mn": 590, "mx": 660},
        "Teknik Industri": {"mn": 600, "mx": 670},
        "Teknik Informatika": {"mn": 630, "mx": 700},
        "Arsitektur": {"mn": 600, "mx": 670},
        "Teknik Lingkungan": {"mn": 575, "mx": 645},
        "Matematika": {"mn": 540, "mx": 610},
        "Fisika": {"mn": 520, "mx": 590},
        "Kimia": {"mn": 530, "mx": 600},
        "Biologi": {"mn": 530, "mx": 600},
        "Statistika": {"mn": 550, "mx": 620},
        "Ilmu Komputer": {"mn": 600, "mx": 670},
        "Ilmu Hukum": {"mn": 560, "mx": 630},
        "Ilmu Ekonomi": {"mn": 560, "mx": 630},
        "Akuntansi": {"mn": 580, "mx": 650},
        "Manajemen": {"mn": 590, "mx": 660},
        "Ilmu Komunikasi": {"mn": 570, "mx": 640},
        "Hubungan Internasional": {"mn": 580, "mx": 650},
        "Sosiologi": {"mn": 530, "mx": 600},
        "Ilmu Politik": {"mn": 530, "mx": 600},
        "Administrasi Negara": {"mn": 540, "mx": 610},
        "Administrasi Bisnis": {"mn": 545, "mx": 615},
        "Ilmu Perpustakaan": {"mn": 500, "mx": 570},
        "Kesejahteraan Sosial": {"mn": 520, "mx": 590},
        "Psikologi": {"mn": 580, "mx": 650},
        "Sastra Indonesia": {"mn": 500, "mx": 570},
        "Sastra Inggris": {"mn": 540, "mx": 610},
        "Sastra Melayu": {"mn": 490, "mx": 560},
        "Sastra Arab": {"mn": 490, "mx": 560},
        "Sastra Jepang": {"mn": 510, "mx": 580},
        "Sastra Cina": {"mn": 510, "mx": 580},
        "Sejarah": {"mn": 490, "mx": 560},
        "Agribisnis": {"mn": 520, "mx": 590},
        "Agroekoteknologi": {"mn": 510, "mx": 580},
        "Kehutanan": {"mn": 510, "mx": 580},
        "Peternakan": {"mn": 500, "mx": 570},
        "Ilmu Kelautan": {"mn": 510, "mx": 580},
        "Budidaya Perairan": {"mn": 500, "mx": 570},
        "Teknologi Pangan": {"mn": 530, "mx": 600},
    },
    "Universitas Andalas": {
        "Pendidikan Dokter": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 550, "mx": 620},
        "Ilmu Gizi": {"mn": 560, "mx": 630},
        "Kesehatan Masyarakat": {"mn": 550, "mx": 620},
        "Kedokteran Gigi": {"mn": 620, "mx": 690},
        "Farmasi": {"mn": 590, "mx": 660},
        "Kedokteran Hewan": {"mn": 580, "mx": 650},
        "Teknik Sipil": {"mn": 580, "mx": 650},
        "Teknik Mesin": {"mn": 580, "mx": 650},
        "Teknik Elektro": {"mn": 600, "mx": 670},
        "Teknik Kimia": {"mn": 580, "mx": 650},
        "Teknik Industri": {"mn": 590, "mx": 660},
        "Teknik Lingkungan": {"mn": 570, "mx": 640},
        "Arsitektur": {"mn": 590, "mx": 660},
        "Teknik Informatika": {"mn": 620, "mx": 690},
        "Sistem Informasi": {"mn": 600, "mx": 670},
        "Matematika": {"mn": 530, "mx": 600},
        "Fisika": {"mn": 510, "mx": 580},
        "Kimia": {"mn": 520, "mx": 590},
        "Biologi": {"mn": 520, "mx": 590},
        "Statistika": {"mn": 540, "mx": 610},
        "Ilmu Hukum": {"mn": 550, "mx": 620},
        "Ilmu Ekonomi": {"mn": 550, "mx": 620},
        "Akuntansi": {"mn": 570, "mx": 640},
        "Manajemen": {"mn": 580, "mx": 650},
        "Ilmu Komunikasi": {"mn": 560, "mx": 630},
        "Sosiologi": {"mn": 520, "mx": 590},
        "Ilmu Politik": {"mn": 520, "mx": 590},
        "Administrasi Publik": {"mn": 525, "mx": 595},
        "Ilmu Pemerintahan": {"mn": 525, "mx": 595},
        "Hubungan Internasional": {"mn": 560, "mx": 630},
        "Psikologi": {"mn": 570, "mx": 640},
        "Sastra Indonesia": {"mn": 490, "mx": 560},
        "Sastra Inggris": {"mn": 530, "mx": 600},
        "Sastra Minangkabau": {"mn": 460, "mx": 530},
        "Sejarah": {"mn": 480, "mx": 550},
        "Agribisnis": {"mn": 510, "mx": 580},
        "Agroteknologi": {"mn": 500, "mx": 570},
        "Peternakan": {"mn": 490, "mx": 560},
        "Kehutanan": {"mn": 490, "mx": 560},
        "Teknologi Pangan": {"mn": 540, "mx": 610},
        "Ilmu Kelautan": {"mn": 500, "mx": 570},
        "Budidaya Perairan": {"mn": 490, "mx": 560},
        "Ilmu Tanah": {"mn": 490, "mx": 560},
    },
    "Universitas Sriwijaya": {
        "Pendidikan Dokter": {"mn": 650, "mx": 720},
        "Ilmu Keperawatan": {"mn": 530, "mx": 600},
        "Kesehatan Masyarakat": {"mn": 530, "mx": 600},
        "Kedokteran Gigi": {"mn": 600, "mx": 670},
        "Farmasi": {"mn": 570, "mx": 640},
        "Teknik Sipil": {"mn": 560, "mx": 630},
        "Teknik Mesin": {"mn": 560, "mx": 630},
        "Teknik Elektro": {"mn": 580, "mx": 650},
        "Teknik Kimia": {"mn": 570, "mx": 640},
        "Teknik Industri": {"mn": 575, "mx": 645},
        "Teknik Pertambangan": {"mn": 560, "mx": 630},
        "Teknik Geologi": {"mn": 560, "mx": 630},
        "Teknik Informatika": {"mn": 600, "mx": 670},
        "Sistem Informasi": {"mn": 580, "mx": 650},
        "Ilmu Komputer": {"mn": 580, "mx": 650},
        "Arsitektur": {"mn": 565, "mx": 635},
        "Teknik Kimia": {"mn": 570, "mx": 640},
        "Matematika": {"mn": 510, "mx": 580},
        "Fisika": {"mn": 490, "mx": 560},
        "Kimia": {"mn": 500, "mx": 570},
        "Biologi": {"mn": 500, "mx": 570},
        "Ilmu Hukum": {"mn": 530, "mx": 600},
        "Ilmu Ekonomi": {"mn": 530, "mx": 600},
        "Akuntansi": {"mn": 550, "mx": 620},
        "Manajemen": {"mn": 560, "mx": 630},
        "Ilmu Komunikasi": {"mn": 540, "mx": 610},
        "Sosiologi": {"mn": 500, "mx": 570},
        "Administrasi Negara": {"mn": 510, "mx": 580},
        "Hubungan Internasional": {"mn": 550, "mx": 620},
        "Ilmu Pemerintahan": {"mn": 510, "mx": 580},
        "Psikologi": {"mn": 550, "mx": 620},
        "Sastra Indonesia": {"mn": 470, "mx": 540},
        "Sastra Inggris": {"mn": 510, "mx": 580},
        "Sastra Arab": {"mn": 460, "mx": 530},
        "Agribisnis": {"mn": 490, "mx": 560},
        "Agroekoteknologi": {"mn": 480, "mx": 550},
        "Peternakan": {"mn": 470, "mx": 540},
        "Kehutanan": {"mn": 470, "mx": 540},
        "Ilmu Kelautan": {"mn": 480, "mx": 550},
        "Budidaya Perairan": {"mn": 470, "mx": 540},
        "Teknologi Pangan": {"mn": 510, "mx": 580},
    },
    "Universitas Udayana": {
        "Pendidikan Dokter": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 550, "mx": 620},
        "Ilmu Gizi": {"mn": 560, "mx": 630},
        "Kesehatan Masyarakat": {"mn": 550, "mx": 620},
        "Kedokteran Gigi": {"mn": 630, "mx": 700},
        "Farmasi": {"mn": 590, "mx": 660},
        "Kedokteran Hewan": {"mn": 600, "mx": 670},
        "Teknik Sipil": {"mn": 580, "mx": 650},
        "Teknik Mesin": {"mn": 575, "mx": 645},
        "Teknik Elektro": {"mn": 600, "mx": 670},
        "Teknik Kimia": {"mn": 575, "mx": 645},
        "Teknik Industri": {"mn": 580, "mx": 650},
        "Arsitektur": {"mn": 600, "mx": 670},
        "Teknik Informatika": {"mn": 630, "mx": 700},
        "Sistem Informasi": {"mn": 600, "mx": 670},
        "Teknologi Informasi": {"mn": 610, "mx": 680},
        "Teknik Lingkungan": {"mn": 570, "mx": 640},
        "Matematika": {"mn": 530, "mx": 600},
        "Fisika": {"mn": 510, "mx": 580},
        "Kimia": {"mn": 520, "mx": 590},
        "Biologi": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 600, "mx": 670},
        "Ilmu Hukum": {"mn": 550, "mx": 620},
        "Ilmu Ekonomi": {"mn": 550, "mx": 620},
        "Akuntansi": {"mn": 570, "mx": 640},
        "Manajemen": {"mn": 580, "mx": 650},
        "Ilmu Komunikasi": {"mn": 560, "mx": 630},
        "Sosiologi": {"mn": 520, "mx": 590},
        "Ilmu Politik": {"mn": 520, "mx": 590},
        "Administrasi Negara": {"mn": 530, "mx": 600},
        "Ilmu Pemerintahan": {"mn": 530, "mx": 600},
        "Hubungan Internasional": {"mn": 565, "mx": 635},
        "Psikologi": {"mn": 570, "mx": 640},
        "Sastra Indonesia": {"mn": 490, "mx": 560},
        "Sastra Inggris": {"mn": 530, "mx": 600},
        "Sastra Bali": {"mn": 450, "mx": 520},
        "Sejarah": {"mn": 480, "mx": 550},
        "Pariwisata": {"mn": 560, "mx": 630},
        "Destinasi Pariwisata": {"mn": 550, "mx": 620},
        "Agribisnis": {"mn": 510, "mx": 580},
        "Agroteknologi": {"mn": 500, "mx": 570},
        "Peternakan": {"mn": 490, "mx": 560},
        "Ilmu Kelautan": {"mn": 510, "mx": 580},
        "Budidaya Perairan": {"mn": 500, "mx": 570},
        "Teknologi Pangan": {"mn": 530, "mx": 600},
    },
    "Universitas Pendidikan Indonesia": {
        "Pendidikan Matematika": {"mn": 580, "mx": 650},
        "Pendidikan Biologi": {"mn": 560, "mx": 630},
        "Pendidikan Kimia": {"mn": 560, "mx": 630},
        "Pendidikan Fisika": {"mn": 560, "mx": 630},
        "Pendidikan Ilmu Komputer": {"mn": 600, "mx": 670},
        "Ilmu Komputer": {"mn": 610, "mx": 680},
        "Teknik Informatika": {"mn": 620, "mx": 690},
        "Teknik Elektro": {"mn": 580, "mx": 650},
        "Teknik Mesin": {"mn": 560, "mx": 630},
        "Pendidikan Teknik Arsitektur": {"mn": 560, "mx": 630},
        "Pendidikan Teknik Bangunan": {"mn": 545, "mx": 615},
        "Pendidikan Bahasa Inggris": {"mn": 590, "mx": 660},
        "Pendidikan Bahasa Indonesia": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Jepang": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Arab": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Perancis": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Jerman": {"mn": 515, "mx": 585},
        "Pendidikan Ekonomi": {"mn": 540, "mx": 610},
        "Manajemen": {"mn": 580, "mx": 650},
        "Akuntansi": {"mn": 580, "mx": 650},
        "Pendidikan Akuntansi": {"mn": 540, "mx": 610},
        "Pendidikan Sejarah": {"mn": 520, "mx": 590},
        "Pendidikan Sosiologi": {"mn": 520, "mx": 590},
        "Pendidikan Geografi": {"mn": 520, "mx": 590},
        "Bimbingan dan Konseling": {"mn": 500, "mx": 570},
        "Pendidikan Luar Biasa": {"mn": 500, "mx": 570},
        "Pendidikan Luar Sekolah": {"mn": 490, "mx": 560},
        "Psikologi": {"mn": 600, "mx": 670},
        "Ilmu Komunikasi": {"mn": 580, "mx": 650},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 490, "mx": 560},
        "Pendidikan Kepelatihan Olahraga": {"mn": 480, "mx": 550},
        "Pendidikan Seni Rupa": {"mn": 460, "mx": 530},
        "Pendidikan Seni Musik": {"mn": 460, "mx": 530},
        "Perpustakaan dan Sains Informasi": {"mn": 490, "mx": 560},
        "Administrasi Pendidikan": {"mn": 490, "mx": 560},
        "Teknologi Pendidikan": {"mn": 490, "mx": 560},
        "Pendidikan Guru Sekolah Dasar": {"mn": 510, "mx": 580},
    },
    "Universitas Negeri Yogyakarta": {
        "Pendidikan Matematika": {"mn": 580, "mx": 650},
        "Pendidikan Biologi": {"mn": 560, "mx": 630},
        "Pendidikan Kimia": {"mn": 560, "mx": 630},
        "Pendidikan Fisika": {"mn": 560, "mx": 630},
        "Matematika": {"mn": 560, "mx": 630},
        "Biologi": {"mn": 540, "mx": 610},
        "Kimia": {"mn": 540, "mx": 610},
        "Fisika": {"mn": 540, "mx": 610},
        "Ilmu Komputer": {"mn": 590, "mx": 660},
        "Teknik Informatika": {"mn": 600, "mx": 670},
        "Teknik Elektro": {"mn": 560, "mx": 630},
        "Teknik Mesin": {"mn": 550, "mx": 620},
        "Pendidikan Teknik Sipil dan Perencanaan": {"mn": 545, "mx": 615},
        "Teknik Boga": {"mn": 490, "mx": 560},
        "Teknik Busana": {"mn": 470, "mx": 540},
        "Pendidikan Bahasa Inggris": {"mn": 580, "mx": 650},
        "Pendidikan Bahasa Indonesia": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Jerman": {"mn": 510, "mx": 580},
        "Pendidikan Bahasa Prancis": {"mn": 510, "mx": 580},
        "Pendidikan Ekonomi": {"mn": 540, "mx": 610},
        "Manajemen": {"mn": 570, "mx": 640},
        "Akuntansi": {"mn": 570, "mx": 640},
        "Pendidikan Akuntansi": {"mn": 530, "mx": 600},
        "Pendidikan Sejarah": {"mn": 510, "mx": 580},
        "Pendidikan Sosiologi": {"mn": 510, "mx": 580},
        "Pendidikan Geografi": {"mn": 510, "mx": 580},
        "Ilmu Keolahragaan": {"mn": 490, "mx": 560},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 480, "mx": 550},
        "Psikologi": {"mn": 590, "mx": 660},
        "Pendidikan Luar Biasa": {"mn": 490, "mx": 560},
        "Pendidikan Seni Rupa": {"mn": 460, "mx": 530},
        "Pendidikan Seni Musik": {"mn": 460, "mx": 530},
        "Administrasi Pendidikan": {"mn": 490, "mx": 560},
        "Bimbingan dan Konseling": {"mn": 490, "mx": 560},
        "Pendidikan Guru Sekolah Dasar": {"mn": 510, "mx": 580},
        "Teknologi Pendidikan": {"mn": 490, "mx": 560},
    },
    "Universitas Negeri Malang": {
        "Pendidikan Matematika": {"mn": 560, "mx": 630},
        "Pendidikan Biologi": {"mn": 540, "mx": 610},
        "Pendidikan Kimia": {"mn": 540, "mx": 610},
        "Pendidikan Fisika": {"mn": 540, "mx": 610},
        "Matematika": {"mn": 540, "mx": 610},
        "Biologi": {"mn": 520, "mx": 590},
        "Kimia": {"mn": 520, "mx": 590},
        "Fisika": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 570, "mx": 640},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Teknik Elektro": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Sipil": {"mn": 530, "mx": 600},
        "Arsitektur": {"mn": 550, "mx": 620},
        "Pendidikan Bahasa Inggris": {"mn": 560, "mx": 630},
        "Pendidikan Bahasa Indonesia": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Arab": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Jepang": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Mandarin": {"mn": 500, "mx": 570},
        "Pendidikan Ekonomi": {"mn": 520, "mx": 590},
        "Manajemen": {"mn": 550, "mx": 620},
        "Akuntansi": {"mn": 550, "mx": 620},
        "Pendidikan Akuntansi": {"mn": 510, "mx": 580},
        "Pendidikan Sejarah": {"mn": 490, "mx": 560},
        "Pendidikan Sosiologi": {"mn": 490, "mx": 560},
        "Pendidikan Geografi": {"mn": 490, "mx": 560},
        "Ilmu Keolahragaan": {"mn": 470, "mx": 540},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 460, "mx": 530},
        "Psikologi": {"mn": 570, "mx": 640},
        "Bimbingan dan Konseling": {"mn": 470, "mx": 540},
        "Pendidikan Luar Biasa": {"mn": 460, "mx": 530},
        "Administrasi Pendidikan": {"mn": 470, "mx": 540},
        "Teknologi Pendidikan": {"mn": 470, "mx": 540},
        "Pendidikan Guru Sekolah Dasar": {"mn": 490, "mx": 560},
        "Seni dan Desain": {"mn": 460, "mx": 530},
    },
    "Universitas Negeri Semarang": {
        "Pendidikan Matematika": {"mn": 540, "mx": 610},
        "Pendidikan Biologi": {"mn": 520, "mx": 590},
        "Pendidikan Kimia": {"mn": 520, "mx": 590},
        "Pendidikan Fisika": {"mn": 520, "mx": 590},
        "Matematika": {"mn": 520, "mx": 590},
        "Biologi": {"mn": 500, "mx": 570},
        "Kimia": {"mn": 500, "mx": 570},
        "Fisika": {"mn": 500, "mx": 570},
        "Ilmu Komputer": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 560, "mx": 630},
        "Teknik Elektro": {"mn": 520, "mx": 590},
        "Teknik Mesin": {"mn": 510, "mx": 580},
        "Teknik Sipil": {"mn": 510, "mx": 580},
        "Teknik Kimia": {"mn": 510, "mx": 580},
        "Arsitektur": {"mn": 530, "mx": 600},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Indonesia": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Jawa": {"mn": 460, "mx": 530},
        "Pendidikan Ekonomi": {"mn": 500, "mx": 570},
        "Manajemen": {"mn": 530, "mx": 600},
        "Akuntansi": {"mn": 530, "mx": 600},
        "Ekonomi Pembangunan": {"mn": 510, "mx": 580},
        "Pendidikan Sejarah": {"mn": 470, "mx": 540},
        "Pendidikan Sosiologi dan Antropologi": {"mn": 470, "mx": 540},
        "Pendidikan Geografi": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 520, "mx": 590},
        "Ilmu Keolahragaan": {"mn": 450, "mx": 520},
        "Psikologi": {"mn": 550, "mx": 620},
        "Kesehatan Masyarakat": {"mn": 530, "mx": 600},
        "Bimbingan dan Konseling": {"mn": 450, "mx": 520},
        "Pendidikan Guru Sekolah Dasar": {"mn": 490, "mx": 560},
        "Teknologi Pendidikan": {"mn": 450, "mx": 520},
        "Pendidikan Luar Sekolah": {"mn": 440, "mx": 510},
        "Seni Rupa": {"mn": 440, "mx": 510},
    },
    "Universitas Lampung": {
        "Pendidikan Dokter": {"mn": 640, "mx": 710},
        "Ilmu Keperawatan": {"mn": 520, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 510, "mx": 580},
        "Farmasi": {"mn": 545, "mx": 615},
        "Teknik Sipil": {"mn": 550, "mx": 620},
        "Teknik Mesin": {"mn": 540, "mx": 610},
        "Teknik Elektro": {"mn": 560, "mx": 630},
        "Teknik Kimia": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Ilmu Komputer": {"mn": 570, "mx": 640},
        "Arsitektur": {"mn": 550, "mx": 620},
        "Matematika": {"mn": 500, "mx": 570},
        "Fisika": {"mn": 480, "mx": 550},
        "Kimia": {"mn": 490, "mx": 560},
        "Biologi": {"mn": 490, "mx": 560},
        "Ilmu Hukum": {"mn": 510, "mx": 580},
        "Ilmu Ekonomi": {"mn": 510, "mx": 580},
        "Akuntansi": {"mn": 530, "mx": 600},
        "Manajemen": {"mn": 540, "mx": 610},
        "Ilmu Komunikasi": {"mn": 520, "mx": 590},
        "Sosiologi": {"mn": 480, "mx": 550},
        "Ilmu Pemerintahan": {"mn": 490, "mx": 560},
        "Administrasi Negara": {"mn": 490, "mx": 560},
        "Hubungan Internasional": {"mn": 530, "mx": 600},
        "Psikologi": {"mn": 540, "mx": 610},
        "Sastra Indonesia": {"mn": 450, "mx": 520},
        "Sastra Inggris": {"mn": 490, "mx": 560},
        "Agribisnis": {"mn": 480, "mx": 550},
        "Agroteknologi": {"mn": 470, "mx": 540},
        "Peternakan": {"mn": 460, "mx": 530},
        "Kehutanan": {"mn": 460, "mx": 530},
        "Teknologi Pangan": {"mn": 490, "mx": 560},
        "Ilmu Kelautan": {"mn": 465, "mx": 535},
        "Perikanan": {"mn": 455, "mx": 525},
        "Ilmu Tanah": {"mn": 455, "mx": 525},
    },
    "Universitas Riau": {
        "Pendidikan Dokter": {"mn": 620, "mx": 690},
        "Ilmu Keperawatan": {"mn": 500, "mx": 570},
        "Kesehatan Masyarakat": {"mn": 490, "mx": 560},
        "Farmasi": {"mn": 545, "mx": 615},
        "Teknik Sipil": {"mn": 530, "mx": 600},
        "Teknik Mesin": {"mn": 520, "mx": 590},
        "Teknik Elektro": {"mn": 540, "mx": 610},
        "Teknik Kimia": {"mn": 530, "mx": 600},
        "Teknik Informatika": {"mn": 560, "mx": 630},
        "Sistem Informasi": {"mn": 540, "mx": 610},
        "Ilmu Komputer": {"mn": 550, "mx": 620},
        "Teknik Lingkungan": {"mn": 510, "mx": 580},
        "Teknik Perminyakan": {"mn": 540, "mx": 610},
        "Matematika": {"mn": 480, "mx": 550},
        "Fisika": {"mn": 460, "mx": 530},
        "Kimia": {"mn": 470, "mx": 540},
        "Biologi": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 490, "mx": 560},
        "Ilmu Ekonomi": {"mn": 490, "mx": 560},
        "Akuntansi": {"mn": 510, "mx": 580},
        "Manajemen": {"mn": 520, "mx": 590},
        "Ilmu Komunikasi": {"mn": 500, "mx": 570},
        "Sosiologi": {"mn": 460, "mx": 530},
        "Ilmu Pemerintahan": {"mn": 470, "mx": 540},
        "Administrasi Negara": {"mn": 460, "mx": 530},
        "Hubungan Internasional": {"mn": 500, "mx": 570},
        "Ilmu Politik": {"mn": 460, "mx": 530},
        "Psikologi": {"mn": 510, "mx": 580},
        "Sastra Indonesia": {"mn": 430, "mx": 500},
        "Sastra Inggris": {"mn": 460, "mx": 530},
        "Sastra Melayu": {"mn": 410, "mx": 480},
        "Agribisnis": {"mn": 450, "mx": 520},
        "Agroteknologi": {"mn": 440, "mx": 510},
        "Peternakan": {"mn": 430, "mx": 500},
        "Kehutanan": {"mn": 440, "mx": 510},
        "Ilmu Kelautan": {"mn": 450, "mx": 520},
        "Budidaya Perairan": {"mn": 430, "mx": 500},
        "Teknologi Pangan": {"mn": 470, "mx": 540},
        "Ilmu Tanah": {"mn": 430, "mx": 500},
    },
    "Universitas Jember": {
        "Pendidikan Dokter": {"mn": 640, "mx": 710},
        "Ilmu Keperawatan": {"mn": 510, "mx": 580},
        "Kesehatan Masyarakat": {"mn": 500, "mx": 570},
        "Kedokteran Gigi": {"mn": 600, "mx": 670},
        "Farmasi": {"mn": 560, "mx": 630},
        "Teknik Sipil": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Elektro": {"mn": 550, "mx": 620},
        "Teknik Kimia": {"mn": 540, "mx": 610},
        "Teknik Informatika": {"mn": 570, "mx": 640},
        "Sistem Informasi": {"mn": 550, "mx": 620},
        "Ilmu Komputer": {"mn": 555, "mx": 625},
        "Matematika": {"mn": 490, "mx": 560},
        "Fisika": {"mn": 470, "mx": 540},
        "Kimia": {"mn": 480, "mx": 550},
        "Biologi": {"mn": 480, "mx": 550},
        "Ilmu Hukum": {"mn": 500, "mx": 570},
        "Ilmu Ekonomi": {"mn": 500, "mx": 570},
        "Akuntansi": {"mn": 520, "mx": 590},
        "Manajemen": {"mn": 530, "mx": 600},
        "Ilmu Komunikasi": {"mn": 510, "mx": 580},
        "Sosiologi": {"mn": 470, "mx": 540},
        "Ilmu Pemerintahan": {"mn": 470, "mx": 540},
        "Administrasi Bisnis": {"mn": 490, "mx": 560},
        "Hubungan Internasional": {"mn": 510, "mx": 580},
        "Ilmu Politik": {"mn": 470, "mx": 540},
        "Psikologi": {"mn": 520, "mx": 590},
        "Sastra Indonesia": {"mn": 440, "mx": 510},
        "Sastra Inggris": {"mn": 470, "mx": 540},
        "Sejarah": {"mn": 440, "mx": 510},
        "Agribisnis": {"mn": 460, "mx": 530},
        "Agroteknologi": {"mn": 450, "mx": 520},
        "Peternakan": {"mn": 440, "mx": 510},
        "Kehutanan": {"mn": 440, "mx": 510},
        "Teknologi Pangan": {"mn": 480, "mx": 550},
        "Ilmu Kelautan": {"mn": 460, "mx": 530},
        "Budidaya Perairan": {"mn": 450, "mx": 520},
        "Ilmu Tanah": {"mn": 440, "mx": 510},
    },
    "Universitas Mulawarman": {
        "Pendidikan Dokter": {"mn": 590, "mx": 660},
        "Ilmu Keperawatan": {"mn": 470, "mx": 540},
        "Kesehatan Masyarakat": {"mn": 460, "mx": 530},
        "Farmasi": {"mn": 520, "mx": 590},
        "Teknik Sipil": {"mn": 490, "mx": 560},
        "Teknik Mesin": {"mn": 480, "mx": 550},
        "Teknik Elektro": {"mn": 500, "mx": 570},
        "Teknik Kimia": {"mn": 490, "mx": 560},
        "Teknik Informatika": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 510, "mx": 580},
        "Teknik Pertambangan": {"mn": 490, "mx": 560},
        "Teknik Geologi": {"mn": 490, "mx": 560},
        "Teknik Perminyakan": {"mn": 510, "mx": 580},
        "Arsitektur": {"mn": 490, "mx": 560},
        "Teknik Lingkungan": {"mn": 470, "mx": 540},
        "Matematika": {"mn": 440, "mx": 510},
        "Fisika": {"mn": 420, "mx": 490},
        "Kimia": {"mn": 430, "mx": 500},
        "Biologi": {"mn": 430, "mx": 500},
        "Ilmu Hukum": {"mn": 450, "mx": 520},
        "Ilmu Ekonomi": {"mn": 450, "mx": 520},
        "Akuntansi": {"mn": 470, "mx": 540},
        "Manajemen": {"mn": 480, "mx": 550},
        "Ilmu Komunikasi": {"mn": 460, "mx": 530},
        "Sosiologi": {"mn": 420, "mx": 490},
        "Ilmu Pemerintahan": {"mn": 430, "mx": 500},
        "Administrasi Bisnis": {"mn": 440, "mx": 510},
        "Administrasi Negara": {"mn": 435, "mx": 505},
        "Sastra Indonesia": {"mn": 405, "mx": 475},
        "Sastra Inggris": {"mn": 430, "mx": 500},
        "Agribisnis": {"mn": 415, "mx": 485},
        "Agroteknologi": {"mn": 410, "mx": 480},
        "Peternakan": {"mn": 405, "mx": 475},
        "Kehutanan": {"mn": 415, "mx": 485},
        "Ilmu Kelautan": {"mn": 415, "mx": 485},
        "Budidaya Perairan": {"mn": 410, "mx": 480},
        "Teknologi Pangan": {"mn": 435, "mx": 505},
        "Ilmu Tanah": {"mn": 405, "mx": 475},
    },
    "Universitas Syiah Kuala": {
        "Pendidikan Dokter": {"mn": 650, "mx": 720},
        "Ilmu Keperawatan": {"mn": 530, "mx": 600},
        "Kesehatan Masyarakat": {"mn": 520, "mx": 590},
        "Kedokteran Gigi": {"mn": 600, "mx": 670},
        "Farmasi": {"mn": 560, "mx": 630},
        "Kedokteran Hewan": {"mn": 560, "mx": 630},
        "Teknik Sipil": {"mn": 550, "mx": 620},
        "Teknik Mesin": {"mn": 540, "mx": 610},
        "Teknik Elektro": {"mn": 560, "mx": 630},
        "Teknik Kimia": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Arsitektur": {"mn": 560, "mx": 630},
        "Teknik Geologi": {"mn": 540, "mx": 610},
        "Teknik Industri": {"mn": 545, "mx": 615},
        "Matematika": {"mn": 490, "mx": 560},
        "Fisika": {"mn": 470, "mx": 540},
        "Kimia": {"mn": 480, "mx": 550},
        "Biologi": {"mn": 480, "mx": 550},
        "Ilmu Hukum": {"mn": 500, "mx": 570},
        "Ilmu Ekonomi": {"mn": 500, "mx": 570},
        "Akuntansi": {"mn": 520, "mx": 590},
        "Manajemen": {"mn": 530, "mx": 600},
        "Ilmu Komunikasi": {"mn": 510, "mx": 580},
        "Sosiologi": {"mn": 470, "mx": 540},
        "Ilmu Pemerintahan": {"mn": 480, "mx": 550},
        "Administrasi Negara": {"mn": 480, "mx": 550},
        "Hubungan Internasional": {"mn": 510, "mx": 580},
        "Ilmu Politik": {"mn": 475, "mx": 545},
        "Psikologi": {"mn": 530, "mx": 600},
        "Sastra Indonesia": {"mn": 440, "mx": 510},
        "Sastra Inggris": {"mn": 470, "mx": 540},
        "Sastra Arab": {"mn": 450, "mx": 520},
        "Agribisnis": {"mn": 460, "mx": 530},
        "Agroteknologi": {"mn": 450, "mx": 520},
        "Peternakan": {"mn": 440, "mx": 510},
        "Kehutanan": {"mn": 440, "mx": 510},
        "Teknologi Pangan": {"mn": 470, "mx": 540},
        "Ilmu Kelautan": {"mn": 460, "mx": 530},
        "Budidaya Perairan": {"mn": 445, "mx": 515},
    },
    "Universitas Negeri Jakarta": {
        "Pendidikan Matematika": {"mn": 560, "mx": 630},
        "Pendidikan Biologi": {"mn": 540, "mx": 610},
        "Pendidikan Kimia": {"mn": 540, "mx": 610},
        "Pendidikan Fisika": {"mn": 540, "mx": 610},
        "Matematika": {"mn": 540, "mx": 610},
        "Biologi": {"mn": 520, "mx": 590},
        "Kimia": {"mn": 520, "mx": 590},
        "Fisika": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 570, "mx": 640},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Teknik Elektro": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Sipil": {"mn": 530, "mx": 600},
        "Pendidikan Bahasa Inggris": {"mn": 570, "mx": 640},
        "Pendidikan Bahasa Indonesia": {"mn": 530, "mx": 600},
        "Pendidikan Bahasa Jerman": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Perancis": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Arab": {"mn": 495, "mx": 565},
        "Pendidikan Ekonomi": {"mn": 530, "mx": 600},
        "Manajemen": {"mn": 560, "mx": 630},
        "Akuntansi": {"mn": 560, "mx": 630},
        "Pendidikan Akuntansi": {"mn": 520, "mx": 590},
        "Pendidikan Sejarah": {"mn": 490, "mx": 560},
        "Pendidikan Sosiologi": {"mn": 490, "mx": 560},
        "Pendidikan Geografi": {"mn": 490, "mx": 560},
        "Sosiologi": {"mn": 500, "mx": 570},
        "Ilmu Komunikasi": {"mn": 560, "mx": 630},
        "Psikologi": {"mn": 575, "mx": 645},
        "Ilmu Keolahragaan": {"mn": 460, "mx": 530},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 450, "mx": 520},
        "Pendidikan Kepelatihan Olahraga": {"mn": 445, "mx": 515},
        "Pendidikan Luar Biasa": {"mn": 470, "mx": 540},
        "Pendidikan Guru Sekolah Dasar": {"mn": 490, "mx": 560},
        "Bimbingan dan Konseling": {"mn": 470, "mx": 540},
        "Administrasi Pendidikan": {"mn": 470, "mx": 540},
        "Teknologi Pendidikan": {"mn": 470, "mx": 540},
        "Pendidikan Seni Rupa": {"mn": 445, "mx": 515},
        "Pendidikan Seni Musik": {"mn": 445, "mx": 515},
        "Desain Komunikasi Visual": {"mn": 555, "mx": 625},
        "Pendidikan Vokasional Teknik Elektronika": {"mn": 500, "mx": 570},
        "Pendidikan Vokasional Konstruksi Bangunan": {"mn": 490, "mx": 560},
    },
    "Universitas Negeri Makassar": {
        "Pendidikan Matematika": {"mn": 530, "mx": 600},
        "Pendidikan Biologi": {"mn": 510, "mx": 580},
        "Pendidikan Kimia": {"mn": 510, "mx": 580},
        "Pendidikan Fisika": {"mn": 510, "mx": 580},
        "Matematika": {"mn": 510, "mx": 580},
        "Biologi": {"mn": 490, "mx": 560},
        "Kimia": {"mn": 490, "mx": 560},
        "Fisika": {"mn": 490, "mx": 560},
        "Ilmu Komputer": {"mn": 540, "mx": 610},
        "Teknik Informatika": {"mn": 550, "mx": 620},
        "Teknik Elektro": {"mn": 510, "mx": 580},
        "Teknik Mesin": {"mn": 500, "mx": 570},
        "Teknik Sipil": {"mn": 510, "mx": 580},
        "Arsitektur": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Indonesia": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Arab": {"mn": 480, "mx": 550},
        "Pendidikan Ekonomi": {"mn": 500, "mx": 570},
        "Manajemen": {"mn": 530, "mx": 600},
        "Akuntansi": {"mn": 530, "mx": 600},
        "Pendidikan Akuntansi": {"mn": 490, "mx": 560},
        "Ilmu Ekonomi": {"mn": 510, "mx": 580},
        "Administrasi Bisnis": {"mn": 490, "mx": 560},
        "Administrasi Negara": {"mn": 485, "mx": 555},
        "Pendidikan Sejarah": {"mn": 460, "mx": 530},
        "Pendidikan Sosiologi": {"mn": 460, "mx": 530},
        "Pendidikan Geografi": {"mn": 460, "mx": 530},
        "Sosiologi": {"mn": 470, "mx": 540},
        "Ilmu Komunikasi": {"mn": 520, "mx": 590},
        "Psikologi": {"mn": 540, "mx": 610},
        "Ilmu Keolahragaan": {"mn": 440, "mx": 510},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 430, "mx": 500},
        "Pendidikan Luar Biasa": {"mn": 440, "mx": 510},
        "Pendidikan Guru Sekolah Dasar": {"mn": 460, "mx": 530},
        "Bimbingan dan Konseling": {"mn": 440, "mx": 510},
        "Teknologi Pendidikan": {"mn": 440, "mx": 510},
        "Pendidikan Seni Rupa": {"mn": 420, "mx": 490},
        "Seni Rupa": {"mn": 420, "mx": 490},
        "Pendidikan Teknik Otomotif": {"mn": 460, "mx": 530},
        "Pendidikan Teknik Bangunan": {"mn": 455, "mx": 525},
    },
    "Universitas Tanjungpura": {
        "Pendidikan Dokter": {"mn": 610, "mx": 680},
        "Ilmu Keperawatan": {"mn": 490, "mx": 560},
        "Kesehatan Masyarakat": {"mn": 480, "mx": 550},
        "Farmasi": {"mn": 530, "mx": 600},
        "Teknik Sipil": {"mn": 510, "mx": 580},
        "Teknik Mesin": {"mn": 500, "mx": 570},
        "Teknik Elektro": {"mn": 520, "mx": 590},
        "Teknik Kimia": {"mn": 510, "mx": 580},
        "Teknik Informatika": {"mn": 540, "mx": 610},
        "Ilmu Komputer": {"mn": 530, "mx": 600},
        "Teknik Lingkungan": {"mn": 495, "mx": 565},
        "Arsitektur": {"mn": 510, "mx": 580},
        "Teknik Pertambangan": {"mn": 495, "mx": 565},
        "Matematika": {"mn": 460, "mx": 530},
        "Fisika": {"mn": 440, "mx": 510},
        "Kimia": {"mn": 450, "mx": 520},
        "Biologi": {"mn": 450, "mx": 520},
        "Statistika": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 470, "mx": 540},
        "Ilmu Ekonomi": {"mn": 470, "mx": 540},
        "Akuntansi": {"mn": 490, "mx": 560},
        "Manajemen": {"mn": 500, "mx": 570},
        "Ilmu Komunikasi": {"mn": 480, "mx": 550},
        "Sosiologi": {"mn": 440, "mx": 510},
        "Ilmu Pemerintahan": {"mn": 445, "mx": 515},
        "Administrasi Publik": {"mn": 445, "mx": 515},
        "Ilmu Politik": {"mn": 440, "mx": 510},
        "Hubungan Internasional": {"mn": 475, "mx": 545},
        "Psikologi": {"mn": 500, "mx": 570},
        "Sastra Indonesia": {"mn": 415, "mx": 485},
        "Sastra Inggris": {"mn": 445, "mx": 515},
        "Sejarah": {"mn": 415, "mx": 485},
        "Agribisnis": {"mn": 430, "mx": 500},
        "Agroteknologi": {"mn": 420, "mx": 490},
        "Peternakan": {"mn": 410, "mx": 480},
        "Kehutanan": {"mn": 420, "mx": 490},
        "Ilmu Kelautan": {"mn": 430, "mx": 500},
        "Budidaya Perairan": {"mn": 415, "mx": 485},
        "Teknologi Pangan": {"mn": 445, "mx": 515},
    },
    "Universitas Mataram": {
        "Pendidikan Dokter": {"mn": 630, "mx": 700},
        "Ilmu Keperawatan": {"mn": 500, "mx": 570},
        "Kesehatan Masyarakat": {"mn": 490, "mx": 560},
        "Kedokteran Gigi": {"mn": 580, "mx": 650},
        "Farmasi": {"mn": 540, "mx": 610},
        "Teknik Sipil": {"mn": 520, "mx": 590},
        "Teknik Mesin": {"mn": 510, "mx": 580},
        "Teknik Elektro": {"mn": 530, "mx": 600},
        "Teknik Informatika": {"mn": 550, "mx": 620},
        "Sistem Informasi": {"mn": 530, "mx": 600},
        "Teknik Pertambangan": {"mn": 500, "mx": 570},
        "Teknik Lingkungan": {"mn": 495, "mx": 565},
        "Arsitektur": {"mn": 515, "mx": 585},
        "Matematika": {"mn": 470, "mx": 540},
        "Fisika": {"mn": 450, "mx": 520},
        "Kimia": {"mn": 460, "mx": 530},
        "Biologi": {"mn": 460, "mx": 530},
        "Ilmu Hukum": {"mn": 480, "mx": 550},
        "Ilmu Ekonomi": {"mn": 480, "mx": 550},
        "Akuntansi": {"mn": 500, "mx": 570},
        "Manajemen": {"mn": 510, "mx": 580},
        "Ilmu Komunikasi": {"mn": 490, "mx": 560},
        "Sosiologi": {"mn": 450, "mx": 520},
        "Ilmu Pemerintahan": {"mn": 455, "mx": 525},
        "Administrasi Negara": {"mn": 455, "mx": 525},
        "Hubungan Internasional": {"mn": 480, "mx": 550},
        "Ilmu Politik": {"mn": 450, "mx": 520},
        "Psikologi": {"mn": 510, "mx": 580},
        "Sastra Indonesia": {"mn": 425, "mx": 495},
        "Sastra Inggris": {"mn": 455, "mx": 525},
        "Sastra Arab": {"mn": 430, "mx": 500},
        "Agribisnis": {"mn": 440, "mx": 510},
        "Agroteknologi": {"mn": 430, "mx": 500},
        "Peternakan": {"mn": 420, "mx": 490},
        "Kehutanan": {"mn": 425, "mx": 495},
        "Ilmu Kelautan": {"mn": 435, "mx": 505},
        "Budidaya Perairan": {"mn": 425, "mx": 495},
        "Teknologi Pangan": {"mn": 455, "mx": 525},
        "Ilmu Tanah": {"mn": 420, "mx": 490},
        "Pariwisata": {"mn": 480, "mx": 550},
    },
    "Universitas Bengkulu": {
        "Pendidikan Dokter": {"mn": 600, "mx": 670},
        "Ilmu Keperawatan": {"mn": 480, "mx": 550},
        "Kesehatan Masyarakat": {"mn": 470, "mx": 540},
        "Farmasi": {"mn": 510, "mx": 580},
        "Teknik Sipil": {"mn": 495, "mx": 565},
        "Teknik Mesin": {"mn": 485, "mx": 555},
        "Teknik Elektro": {"mn": 505, "mx": 575},
        "Teknik Informatika": {"mn": 525, "mx": 595},
        "Ilmu Komputer": {"mn": 515, "mx": 585},
        "Teknik Kimia": {"mn": 490, "mx": 560},
        "Teknik Lingkungan": {"mn": 475, "mx": 545},
        "Matematika": {"mn": 445, "mx": 515},
        "Fisika": {"mn": 425, "mx": 495},
        "Kimia": {"mn": 435, "mx": 505},
        "Biologi": {"mn": 435, "mx": 505},
        "Ilmu Hukum": {"mn": 455, "mx": 525},
        "Ilmu Ekonomi": {"mn": 455, "mx": 525},
        "Akuntansi": {"mn": 475, "mx": 545},
        "Manajemen": {"mn": 485, "mx": 555},
        "Ilmu Komunikasi": {"mn": 465, "mx": 535},
        "Sosiologi": {"mn": 425, "mx": 495},
        "Ilmu Pemerintahan": {"mn": 430, "mx": 500},
        "Administrasi Negara": {"mn": 430, "mx": 500},
        "Ilmu Politik": {"mn": 425, "mx": 495},
        "Hubungan Internasional": {"mn": 455, "mx": 525},
        "Psikologi": {"mn": 485, "mx": 555},
        "Sastra Indonesia": {"mn": 400, "mx": 470},
        "Sastra Inggris": {"mn": 430, "mx": 500},
        "Sejarah": {"mn": 400, "mx": 470},
        "Agribisnis": {"mn": 415, "mx": 485},
        "Agroteknologi": {"mn": 405, "mx": 475},
        "Peternakan": {"mn": 400, "mx": 470},
        "Kehutanan": {"mn": 410, "mx": 480},
        "Ilmu Kelautan": {"mn": 415, "mx": 485},
        "Budidaya Perairan": {"mn": 405, "mx": 475},
        "Teknologi Pangan": {"mn": 430, "mx": 500},
        "Ilmu Tanah": {"mn": 400, "mx": 470},
    },
    "Universitas Sam Ratulangi": {
        "Pendidikan Dokter": {"mn": 640, "mx": 710},
        "Ilmu Keperawatan": {"mn": 520, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 510, "mx": 580},
        "Kedokteran Gigi": {"mn": 590, "mx": 660},
        "Farmasi": {"mn": 550, "mx": 620},
        "Kedokteran Hewan": {"mn": 545, "mx": 615},
        "Teknik Sipil": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Elektro": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 570, "mx": 640},
        "Arsitektur": {"mn": 550, "mx": 620},
        "Teknik Lingkungan": {"mn": 520, "mx": 590},
        "Matematika": {"mn": 480, "mx": 550},
        "Fisika": {"mn": 460, "mx": 530},
        "Kimia": {"mn": 470, "mx": 540},
        "Biologi": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 490, "mx": 560},
        "Ilmu Ekonomi": {"mn": 490, "mx": 560},
        "Akuntansi": {"mn": 510, "mx": 580},
        "Manajemen": {"mn": 520, "mx": 590},
        "Ilmu Komunikasi": {"mn": 500, "mx": 570},
        "Sosiologi": {"mn": 460, "mx": 530},
        "Ilmu Pemerintahan": {"mn": 460, "mx": 530},
        "Administrasi Bisnis": {"mn": 470, "mx": 540},
        "Hubungan Internasional": {"mn": 490, "mx": 560},
        "Ilmu Politik": {"mn": 460, "mx": 530},
        "Psikologi": {"mn": 510, "mx": 580},
        "Sastra Indonesia": {"mn": 430, "mx": 500},
        "Sastra Inggris": {"mn": 460, "mx": 530},
        "Agribisnis": {"mn": 440, "mx": 510},
        "Agroteknologi": {"mn": 430, "mx": 500},
        "Peternakan": {"mn": 420, "mx": 490},
        "Ilmu Kelautan": {"mn": 440, "mx": 510},
        "Budidaya Perairan": {"mn": 430, "mx": 500},
        "Teknologi Pangan": {"mn": 450, "mx": 520},
        "Kehutanan": {"mn": 430, "mx": 500},
    },
}

@st.cache_data(ttl=3600)
def load_database():
    import io
    def read_xlsx(source):
        return pd.read_excel(source, sheet_name=None, engine="openpyxl")
    def load_file(local_path, url):
        if os.path.exists(local_path):
            try:
                return read_xlsx(local_path), None
            except:
                pass
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=20) as resp:
                data = resp.read()
            return read_xlsx(io.BytesIO(data)), None
        except Exception as e:
            return None, str(e)

    # ── S1: gunakan database akurat per kampus (menggantikan Excel yg semua PTN sama) ──
    ptn_s1 = {k: {p: dict(v) for p, v in vv.items()} for k, vv in PTN_PRODI_S1.items()}

    # D3/D4: gunakan database akurat per kampus (Excel juga semua PTN sama persis)
    ptn_d3 = {k: {p: dict(v) for p, v in vv.items()} for k, vv in PTN_PRODI_D3.items()}
    ptn_d4 = {k: {p: dict(v) for p, v in vv.items()} for k, vv in PTN_PRODI_D4.items()}

    # df_s1 dummy agar kode lain yang referens df_s1 tidak error
    df_s1 = pd.DataFrame(
        [{"No": str(i+1), "Prodi": p, "Kelompok": "-", "PTN": ptn,
          "Rank": "-", "NilaiAman": str(v["mn"]), "Rentang": f"{v['mn']}-{v['mx']}", "Catatan": ""}
         for i, (ptn, pd_map) in enumerate(PTN_PRODI_S1.items())
         for p, v in pd_map.items()]
    )

    return ptn_s1, ptn_d3, ptn_d4, df_s1, None

_PTN_S1, _PTN_D3, _PTN_D4, _DF_S1, _DB_ERR = load_database()

def get_db(jenjang="S1 (Sarjana)"):
    if "D4" in jenjang:
        return _PTN_D4 or {}
    elif "D3" in jenjang:
        return _PTN_D3 or {}
    return _PTN_S1 or {}

def get_daftar_ptn(jenjang="S1 (Sarjana)"):
    db = get_db(jenjang)
    return sorted(db.keys())

def get_daftar_prodi(ptn, jenjang="S1 (Sarjana)"):
    db = get_db(jenjang)
    return sorted(db.get(ptn, {}).keys())

def get_skor_info(ptn, prodi, jenjang="S1 (Sarjana)"):
    db = get_db(jenjang)
    ptn_data = db.get(ptn, {})
    data = ptn_data.get(prodi, None)
    if data is None:
        return {"mn": 600, "mx": 670}
    return data

# ══════════════════════════════════════════════════════════
# KATEGORI SKOR — 4 Level
# ══════════════════════════════════════════════════════════
def get_kategori_skor(sw, mn, mx):
    if sw >= mx:
        return ("Sangat Aman",  "#148a42", "badge-sa", "🏆",
                min(95.0, 80 + (sw - mx) / max(mx, 1) * 15))
    elif sw >= mn:
        return ("Aman",         "#1a5fa0", "badge-a",  "✅",
                60 + (sw - mn) / max(mx - mn, 1) * 18)
    elif sw >= mn - 70:
        gap = sw - mn
        return ("Berisiko",     "#e67e22", "badge-br", "⚡",
                max(20, 35 + gap / 70 * 20))
    else:
        return ("Tidak Aman",   "#c0392b", "badge-na", "🔴",
                max(5, 18 + (sw - (mn - 140)) / 70 * 12))

# ══════════════════════════════════════════════════════════
# BOBOT PER JURUSAN
# ══════════════════════════════════════════════════════════
BOBOT_KEYWORD = {
    "Teknik Informatika":    {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Rekayasa Perangkat Lunak":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknologi Informasi":   {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Ilmu Komputer":         {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Komputer":       {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Sipil":          {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Mesin":          {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Elektro":        {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Industri":       {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Kimia":          {"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Mekatronika":           {"PU":.19,"PPU":.06,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.37},
    "Matematika":            {"PU":.15,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.45},
    "Fisika":                {"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.40},
    "Kimia":                 {"PU":.18,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.05,"PM":.35},
    "Biologi":               {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Statistika":            {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Aktuaria":              {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Bioteknologi":          {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Arsitektur":            {"PU":.20,"PPU":.10,"PBM":.10,"PK":.18,"LBI":.10,"LBE":.10,"PM":.22},
    "Teknik Lingkungan":     {"PU":.20,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.30},
    "Teknik Geologi":        {"PU":.20,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.30},
    "Teknik Perminyakan":    {"PU":.20,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.30},
    "Teknik Perkapalan":     {"PU":.20,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.35},
    "Teknik Geodesi":        {"PU":.20,"PPU":.08,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.32},
    "Teknik Otomotif":       {"PU":.20,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.35},
    "Teknik Elektronika":    {"PU":.20,"PPU":.06,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.36},
    "Rekayasa Kimia":        {"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Teknologi Pangan":      {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Analisis Kimia":        {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.07,"PM":.29},
    "Manufaktur":            {"PU":.20,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.35},
    "Geomatika":             {"PU":.20,"PPU":.08,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.32},
    "Geofisika":             {"PU":.18,"PPU":.08,"PBM":.06,"PK":.20,"LBI":.06,"LBE":.07,"PM":.35},
    "Penginderaan Jauh":     {"PU":.18,"PPU":.10,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.30},
    "Logistik":              {"PU":.20,"PPU":.12,"PBM":.14,"PK":.16,"LBI":.14,"LBE":.10,"PM":.14},
    "Supply Chain":          {"PU":.20,"PPU":.12,"PBM":.14,"PK":.16,"LBI":.14,"LBE":.10,"PM":.14},
    "Kedokteran":            {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Kedokteran Gigi":       {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Farmasi":               {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.28},
    "Gizi":                  {"PU":.18,"PPU":.13,"PBM":.10,"PK":.15,"LBI":.13,"LBE":.08,"PM":.23},
    "Gizi Klinik":           {"PU":.18,"PPU":.13,"PBM":.10,"PK":.15,"LBI":.13,"LBE":.08,"PM":.23},
    "Keperawatan":           {"PU":.18,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.23},
    "Kesehatan Masyarakat":  {"PU":.20,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.21},
    "Fisioterapi":           {"PU":.19,"PPU":.13,"PBM":.12,"PK":.13,"LBI":.15,"LBE":.08,"PM":.20},
    "Kebidanan":             {"PU":.18,"PPU":.14,"PBM":.13,"PK":.12,"LBI":.17,"LBE":.08,"PM":.18},
    "Radiologi":             {"PU":.18,"PPU":.12,"PBM":.08,"PK":.20,"LBI":.10,"LBE":.07,"PM":.25},
    "Rekam Medis":           {"PU":.18,"PPU":.12,"PBM":.14,"PK":.15,"LBI":.16,"LBE":.08,"PM":.17},
    "Analis Kesehatan":      {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
    "Laboratorium Medis":    {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
    "Keselamatan Kesehatan": {"PU":.20,"PPU":.13,"PBM":.12,"PK":.12,"LBI":.14,"LBE":.10,"PM":.19},
    "Ekonomi":               {"PU":.20,"PPU":.15,"PBM":.10,"PK":.20,"LBI":.10,"LBE":.10,"PM":.15},
    "Manajemen":             {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Akuntansi":             {"PU":.18,"PPU":.15,"PBM":.10,"PK":.22,"LBI":.10,"LBE":.10,"PM":.15},
    "Bisnis":                {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Perpajakan":            {"PU":.18,"PPU":.14,"PBM":.12,"PK":.22,"LBI":.12,"LBE":.08,"PM":.14},
    "Keuangan":              {"PU":.18,"PPU":.13,"PBM":.12,"PK":.22,"LBI":.12,"LBE":.08,"PM":.15},
    "Perbankan":             {"PU":.18,"PPU":.13,"PBM":.12,"PK":.22,"LBI":.12,"LBE":.08,"PM":.15},
    "Manajemen Pemasaran":   {"PU":.20,"PPU":.14,"PBM":.17,"PK":.12,"LBI":.18,"LBE":.12,"PM":.07},
    "Administrasi Bisnis":   {"PU":.20,"PPU":.15,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.10,"PM":.07},
    "Penilaian Properti":    {"PU":.20,"PPU":.13,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.15},
    "Pariwisata":            {"PU":.18,"PPU":.13,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.18,"PM":.07},
    "Perhotelan":            {"PU":.18,"PPU":.12,"PBM":.17,"PK":.08,"LBI":.18,"LBE":.20,"PM":.07},
    "Perjalanan Wisata":     {"PU":.18,"PPU":.12,"PBM":.17,"PK":.08,"LBI":.18,"LBE":.20,"PM":.07},
    "Ilmu Hukum":            {"PU":.22,"PPU":.18,"PBM":.20,"PK":.08,"LBI":.18,"LBE":.10,"PM":.04},
    "Psikologi":             {"PU":.22,"PPU":.15,"PBM":.18,"PK":.10,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Komunikasi":       {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Hubungan Masyarakat":   {"PU":.20,"PPU":.15,"PBM":.22,"PK":.07,"LBI":.22,"LBE":.10,"PM":.04},
    "Hubungan Internasional":{"PU":.20,"PPU":.15,"PBM":.15,"PK":.08,"LBI":.17,"LBE":.20,"PM":.05},
    "Administrasi Publik":   {"PU":.22,"PPU":.15,"PBM":.18,"PK":.08,"LBI":.20,"LBE":.10,"PM":.07},
    "Sosiologi":             {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Politik":          {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Sejarah":               {"PU":.20,"PPU":.20,"PBM":.18,"PK":.05,"LBI":.22,"LBE":.10,"PM":.05},
    "Geografi":              {"PU":.20,"PPU":.15,"PBM":.15,"PK":.12,"LBI":.15,"LBE":.08,"PM":.15},
    "Komunikasi":            {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Sastra Inggris":        {"PU":.12,"PPU":.12,"PBM":.20,"PK":.05,"LBI":.15,"LBE":.31,"PM":.05},
    "Bahasa Inggris":        {"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Bahasa Indonesia":      {"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Pendidikan Bahasa Inggris":{"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Pendidikan Bahasa Indonesia":{"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Desain Grafis":         {"PU":.18,"PPU":.10,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.12,"PM":.12},
    "Animasi":               {"PU":.18,"PPU":.10,"PBM":.15,"PK":.15,"LBI":.17,"LBE":.12,"PM":.13},
    "Seni":                  {"PU":.18,"PPU":.12,"PBM":.20,"PK":.08,"LBI":.20,"LBE":.12,"PM":.10},
    "Agribisnis":            {"PU":.20,"PPU":.15,"PBM":.12,"PK":.15,"LBI":.15,"LBE":.08,"PM":.15},
    "Kehutanan":             {"PU":.20,"PPU":.15,"PBM":.12,"PK":.15,"LBI":.15,"LBE":.08,"PM":.15},
    "Peternakan":            {"PU":.20,"PPU":.15,"PBM":.12,"PK":.14,"LBI":.14,"LBE":.08,"PM":.17},
}
DEFAULT_BOBOT = {"PU":.16,"PPU":.14,"PBM":.14,"PK":.14,"LBI":.14,"LBE":.14,"PM":.14}

def get_bobot(prodi_name):
    if prodi_name in BOBOT_KEYWORD:
        return BOBOT_KEYWORD[prodi_name]
    prodi_lower = prodi_name.lower()
    best_match = None
    best_len = 0
    for keyword, bobot in BOBOT_KEYWORD.items():
        if keyword.lower() in prodi_lower and len(keyword) > best_len:
            best_match = bobot
            best_len = len(keyword)
    return best_match if best_match else DEFAULT_BOBOT

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
    bobot = get_bobot(d["prodi"])
    sw    = hitung_tw(skor, bobot)
    rata  = float(np.mean([skor[k] for k in SUBTES]))
    jenjang = d.get("jenjang","S1 (Sarjana)")
    info  = get_skor_info(d["kampus"], d["prodi"], jenjang)
    mn, mx = info["mn"], info["mx"]
    gap   = sw - mn
    kat, kat_clr, kat_badge, kat_icon, ppct = get_kategori_skor(sw, mn, mx)

    psiko   = (d["fokus"]*1.5 + d["pede"]*1.5 + (6-d["cemas"]) + (6-d["distrak"])) / 20 * 100
    konsist = min(100, (d["jam"]*2 + d["hari"]*2.2 + d["latihan"]*1.8 + d["tryout"]*1.5 + d["review"]*1.5)*2)
    pos  = (d["fokus"]*1.5 + d["pede"]*1.5)*10
    neg  = (d["cemas"]*1.2 + d["distrak"]*1.2)*8
    stab = max(0, min(100, pos - neg + 50))
    rgb  = stab*0.6 + konsist*0.4
    if rgb >= 75:   risk=("Rendah","✅","Kemungkinan perform sesuai/di atas kemampuan")
    elif rgb >= 60: risk=("Sedang","⚠️","Ada potensi fluktuasi, jaga konsistensi")
    else:           risk=("Tinggi","🔴","Risiko perform di bawah kemampuan, perlu perbaikan")

    lgbm_r = predict_lgbm(lgbm_model, d) if lgbm_model else None

    return {**d,"skor":skor,"bobot":bobot,"sw":sw,"rata":rata,
            "kat":kat,"kat_clr":kat_clr,"kat_badge":kat_badge,"kat_icon":kat_icon,
            "ppct":ppct,"info":info,"mn":mn,"mx":mx,"gap":gap,
            "psiko":psiko,"konsist":konsist,"stab":stab,"risk":risk,
            "lgbm_r":lgbm_r,"jenjang":jenjang}


# ══════════════════════════════════════════════════════════
# REKOMENDASI ALTERNATIF
# ══════════════════════════════════════════════════════════

def get_rekomendasi_alternatif(skor, sw, prodi_target, kampus_target, jenjang, top_n=10):
    db = get_db(jenjang)
    kat_order = {"Sangat Aman": 0, "Aman": 1, "Berisiko": 2, "Tidak Aman": 3}

    # ── 1. Prodi lain di kampus yang sama ──
    alt_kampus_sama = []
    prodi_di_kampus = db.get(kampus_target, {})
    for prodi, info in prodi_di_kampus.items():
        if prodi == prodi_target:
            continue
        bobot_p = get_bobot(prodi)
        sw_p    = hitung_tw(skor, bobot_p)
        kat_p, kat_clr_p, badge_p, icon_p, pct_p = get_kategori_skor(sw_p, info["mn"], info["mx"])
        alt_kampus_sama.append({
            "prodi": prodi, "kampus": kampus_target,
            "mn": info["mn"], "mx": info["mx"],
            "sw": round(sw_p, 1), "gap": round(sw_p - info["mn"], 1),
            "kat": kat_p, "kat_clr": kat_clr_p,
            "badge": badge_p, "icon": icon_p, "ppct": round(pct_p, 1),
        })
    alt_kampus_sama.sort(key=lambda x: (kat_order.get(x["kat"], 9), -x["gap"]))
    alt_kampus_sama = alt_kampus_sama[:top_n]

    # ── 2. Prodi sama / mirip di kampus lain ──
    prodi_lower = prodi_target.lower()
    prodi_clean = prodi_lower.replace("d3 ", "").replace("d4 ", "").strip()
    alt_prodi_sama = []
    for kampus, prodi_map in db.items():
        if kampus == kampus_target:
            continue
        for prodi, info in prodi_map.items():
            prodi_cmp = prodi.lower().replace("d3 ", "").replace("d4 ", "").strip()
            if prodi_cmp == prodi_clean or prodi_clean in prodi_cmp or prodi_cmp in prodi_clean:
                bobot_p = get_bobot(prodi)
                sw_p    = hitung_tw(skor, bobot_p)
                kat_p, kat_clr_p, badge_p, icon_p, pct_p = get_kategori_skor(sw_p, info["mn"], info["mx"])
                alt_prodi_sama.append({
                    "prodi": prodi, "kampus": kampus,
                    "mn": info["mn"], "mx": info["mx"],
                    "sw": round(sw_p, 1), "gap": round(sw_p - info["mn"], 1),
                    "kat": kat_p, "kat_clr": kat_clr_p,
                    "badge": badge_p, "icon": icon_p, "ppct": round(pct_p, 1),
                })
    alt_prodi_sama.sort(key=lambda x: (kat_order.get(x["kat"], 9), -x["gap"]))
    alt_prodi_sama = alt_prodi_sama[:top_n]

    return alt_kampus_sama, alt_prodi_sama


def render_alt_cards(items, show_kampus=False, show_prodi=False):
    if not items:
        st.info("Tidak ada data alternatif yang ditemukan.")
        return
    badge_bg = {
        "Sangat Aman": ("#e6f5ee", "#148a42", "#9adbb8"),
        "Aman":        ("#edf6ff", "#1a5fa0", "#90c0f0"),
        "Berisiko":    ("#fff4e6", "#e67e22", "#f4c08a"),
        "Tidak Aman":  ("#fff0f0", "#c0392b", "#f4a0a0"),
    }
    for item in items:
        bg, fc, bc = badge_bg.get(item["kat"], ("#f8faff","#334466","#ccd9f0"))
        gap_str  = f"+{item['gap']:.0f}" if item["gap"] >= 0 else f"{item['gap']:.0f}"
        gap_clr  = "#148a42" if item["gap"] >= 0 else "#c0392b"
        if show_kampus:
            nama_utama = item["kampus"]
            nama_sub   = item["prodi"]
        else:
            nama_utama = item["prodi"]
            nama_sub   = item["kampus"]
        st.markdown(f"""
        <div style="background:#fff;border:1.5px solid {bc};border-radius:12px;
                    padding:.9rem 1.2rem;margin-bottom:.55rem;
                    border-left:5px solid {fc};
                    box-shadow:0 2px 10px rgba(30,60,140,.07);">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.4rem">
            <div>
              <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:.92rem;color:#12203f">{nama_utama}</div>
              <div style="font-size:.75rem;color:#6a7a9a;margin-top:2px">{nama_sub}</div>
            </div>
            <div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap">
              <span style="background:{bg};color:{fc};border:1.5px solid {bc};padding:.22rem .75rem;border-radius:99px;font-size:.72rem;font-weight:700">{item['icon']} {item['kat']}</span>
              <span style="background:#f0f4fa;color:#334466;border:1px solid #dde8f4;padding:.22rem .75rem;border-radius:99px;font-size:.72rem;font-weight:600">~{item['ppct']:.0f}% peluang</span>
            </div>
          </div>
          <div style="display:flex;gap:1.5rem;margin-top:.55rem;font-size:.78rem;flex-wrap:wrap">
            <span>🎯 <strong>Skor kamu:</strong> <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#3464c8">{item['sw']:.0f}</span></span>
            <span>📏 <strong>Rentang aman:</strong> {item['mn']} – {item['mx']}</span>
            <span>📊 <strong>Gap:</strong> <span style="font-weight:700;color:{gap_clr}">{gap_str}</span></span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# RENCANA BELAJAR MINGGUAN
# ══════════════════════════════════════════════════════════
def buat_rencana_mingguan(r, n_minggu=8):
    skor = r["skor"]; sw = r["sw"]; mn = r["mn"]; mx = r["mx"]
    ranked = sorted(SUBTES, key=lambda k: skor[k])
    terlemah3 = ranked[:3]; sedang2 = ranked[3:5]
    gap = r["gap"]
    target_pm = abs(gap)/n_minggu + 10 if gap < 0 else (mx-sw)/n_minggu + 5 if sw < mx else 5
    rencana = []
    for w in range(1, n_minggu+1):
        fase = "Fondasi" if w<=2 else "Intensif" if w<=5 else "Pemantapan" if w<=7 else "Final"
        target_sw = min(mx+20, sw + target_pm * w)
        if fase == "Fondasi":
            tasks = [
                f"Review konsep dasar {SUBTES_FULL[terlemah3[0]]} (skor {skor[terlemah3[0]]} → target +30)",
                f"50 soal latihan {SUBTES_FULL[terlemah3[1]]} dengan timer",
                f"Pelajari pola soal {SUBTES_FULL[terlemah3[2]]}",
                "Buat catatan kesalahan (error log)",
                "Tryout mini: 30 soal campuran + analisis",
            ]; jam = "2–3 jam/hari"
        elif fase == "Intensif":
            subtes_minggu = terlemah3 + sedang2
            subtes_ini = subtes_minggu[(w-3) % len(subtes_minggu)] if subtes_minggu else "PU"
            tasks = [
                f"100 soal latihan {SUBTES_FULL[subtes_ini]} + timer ketat",
                "Review error log minggu sebelumnya",
                f"Mini tryout {SUBTES_FULL[sedang2[0] if sedang2 else 'PU']} (50 soal, 45 mnt)",
                "Simulasi 1 paket soal lengkap (90 mnt)",
                "Analisis & rekap kesalahan pola berulang",
            ]; jam = "3–4 jam/hari"
        elif fase == "Pemantapan":
            tasks = [
                "Full tryout 1 paket lengkap + evaluasi",
                f"Review intensif {SUBTES_FULL[terlemah3[0]]} (subtes fokus utama)",
                "Latihan manajemen waktu (simulasi kondisi ujian)",
                "Review catatan penting semua subtes",
                "Rest day: hanya review ringan 1 jam",
            ]; jam = "3–4 jam/hari (1 hari libur)"
        else:
            tasks = [
                "Full tryout final + review mendalam",
                "Revisi soal-soal sulit yang pernah salah",
                "Persiapan mental: teknik relaksasi & tidur cukup",
                "Cek strategi manajemen waktu ujian",
                "Istirahat — jaga kondisi fisik & mental",
            ]; jam = "2 jam/hari + istirahat cukup"
        rencana.append({
            "minggu":w,"fase":fase,"target_skor":f"{target_sw:.0f}",
            "jam":jam,"fokus":SUBTES_FULL.get(terlemah3[0],"TPS"),"tasks":tasks,
        })
    return rencana

# ══════════════════════════════════════════════════════════
# CHART THEME
# ══════════════════════════════════════════════════════════
CTH = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#3a4a65'),
    margin=dict(l=10,r=10,t=45,b=10)
)

def ch_radar(skor, bobot, prodi, key=None):
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal Prodi',
        fillcolor='rgba(200,137,10,.08)',line=dict(color='#c8890a',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)',line=dict(color='#3b6cb7',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9,color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9.5,color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#3a4a65')),
        title=dict(text=f"Radar TPS — {prodi}",font=dict(size=13,color='#1a2540')),height=400)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("radar"))

def ch_bar_subtes(skor, bobot, info, key=None):
    lbl  = [SUBTES_FULL[k] for k in SUBTES]
    vals = [skor[k] for k in SUBTES]
    tgt  = [min(SKOR_MAX_TPS,(info["mn"]+info["mx"])/2*bobot[k]*7) for k in SUBTES]
    clrs = [SUBTES_CLR[k] for k in SUBTES]
    fig  = go.Figure()
    fig.add_trace(go.Bar(name='Skor Kamu',x=lbl,y=vals,marker_color=clrs,marker_line_width=0,
        text=[str(v) for v in vals],textposition='outside',textfont=dict(size=10,color='#1a2540')))
    fig.add_trace(go.Scatter(name='Target Kampus',x=lbl,y=tgt,mode='markers+lines',
        marker=dict(symbol='diamond',size=9,color='#c8890a'),
        line=dict(color='#c8890a',dash='dot',width=1.5)))
    fig.update_layout(**CTH,barmode='group',
        xaxis=dict(tickfont=dict(size=9,color='#3a4a65'),gridcolor='#dde3ec'),
        yaxis=dict(range=[0,SKOR_MAX_TPS*1.07],gridcolor='#eef1f5',tickfont=dict(size=9,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.2,font=dict(color='#3a4a65')),
        title=dict(text="Skor Per Subtes vs Target Kampus",font=dict(size=13,color='#1a2540')),height=370)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("bar"))

def ch_bobot(prodi, key=None):
    bobot = get_bobot(prodi)
    lbl   = [SUBTES_FULL[k] for k in SUBTES]
    vals  = [bobot[k]*100 for k in SUBTES]
    clrs  = [SUBTES_CLR[k] for k in SUBTES]
    fig   = go.Figure(go.Bar(x=lbl,y=vals,marker_color=clrs,marker_line_width=0,
        text=[f"{v:.0f}%" for v in vals],textposition='outside',textfont=dict(size=10,color='#1a2540')))
    fig.update_layout(**CTH,
        xaxis=dict(tickfont=dict(size=9,color='#3a4a65'),gridcolor='#dde3ec'),
        yaxis=dict(range=[0,55],ticksuffix="%",gridcolor='#eef1f5',tickfont=dict(size=9,color='#3a4a65')),
        title=dict(text=f"Distribusi Bobot Subtes — {prodi}",font=dict(size=13,color='#1a2540')),height=300)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("bobot"))

def ch_pipeline(skor, bobot, info, prodi, key=None):
    lbl    = [SUBTES_FULL[k] for k in SUBTES]
    aktual = [skor[k]*bobot[k] for k in SUBTES]
    ideal  = [info["mn"]*bobot[k] for k in SUBTES]
    clrs   = [SUBTES_CLR[k] for k in SUBTES]
    fig    = go.Figure()
    fig.add_trace(go.Bar(name='Target Min Kampus',y=lbl,x=ideal,orientation='h',
        marker_color=['rgba(200,137,10,.12)']*7,marker_line_color='#c8890a',marker_line_width=1.5))
    fig.add_trace(go.Bar(name='Kontribusi Aktual',y=lbl,x=aktual,orientation='h',
        marker_color=clrs,text=[f"{v:.1f}" for v in aktual],
        textposition='inside',textfont=dict(size=10,color='#fff')))
    fig.update_layout(**CTH,barmode='overlay',
        xaxis=dict(title="Kontribusi ke Skor Total",gridcolor='#eef1f5',title_font=dict(color='#6a7a95'),tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(gridcolor='#dde3ec',tickfont=dict(size=10,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.13,font=dict(color='#3a4a65')),
        title=dict(text=f"Pipeline Kontribusi Subtes — {prodi}",font=dict(size=13,color='#1a2540')),height=380)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("pipe"))

def ch_skor_gauge(sw, mn, mx, key=None):
    na_end  = mn - 70
    br_end  = mn
    a_end   = mx
    sa_end  = min(mx + 80, 1000)
    fig = go.Figure()
    zones = [
        (200,   na_end, "rgba(255,0,0,.08)",   "Tidak Aman"),
        (na_end, br_end, "rgba(230,126,34,.10)", "Berisiko"),
        (br_end, a_end,  "rgba(26,95,160,.08)",  "Aman"),
        (a_end,  sa_end, "rgba(20,138,66,.10)",  "Sangat Aman"),
    ]
    for x0, x1, clr, lbl in zones:
        if x1 > x0:
            fig.add_vrect(x0=x0, x1=x1, fillcolor=clr, layer="below",
                          line_width=0, annotation_text=lbl,
                          annotation_position="top",
                          annotation_font=dict(size=9, color='#3a4a65'))
    fig.add_vline(x=sw, line_dash="dash", line_color="#7048c8", line_width=3,
                  annotation_text=f"  Skormu: {sw:.0f}", annotation_font_color="#7048c8", annotation_font_size=12)
    fig.add_vline(x=mn, line_dash="dot", line_color="#d4620a", line_width=1.5,
                  annotation_text=f"  Min ({mn})", annotation_font_color="#d4620a", annotation_font_size=10)
    fig.add_vline(x=mx, line_dash="dot", line_color="#148a42", line_width=1.5,
                  annotation_text=f"  Aman ({mx})", annotation_font_color="#148a42", annotation_font_size=10)
    fig.add_trace(go.Scatter(x=[sw], y=[0.5], mode='markers',
        marker=dict(size=18, color='#7048c8', symbol='diamond',
                    line=dict(color='#fff', width=2)),
        name=f'Skor {sw:.0f}', showlegend=False))
    fig.update_layout(**CTH,
        xaxis=dict(range=[max(200, mn-150), min(1000, mx+100)],
                   title="Skor Tertimbang", gridcolor='#eef1f5', tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(visible=False),
        title=dict(text="📊 Posisi Skor — 4 Kategori Kesiapan", font=dict(size=13,color='#1a2540')),
        height=200)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("gauge"))

def ch_psiko(psiko, konsist, stab, key=None):
    cats = ["Kesiapan Mental","Konsistensi Belajar","Stabilitas Mental"]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=cats,y=[psiko,konsist,stab],
        marker_color=["#3b6cb7","#1a8a4a","#7048c8"],marker_line_width=0,
        text=[f"{v:.0f}%" for v in [psiko,konsist,stab]],
        textposition='outside',textfont=dict(size=11,color='#1a2540')))
    fig.add_hline(y=80,line_dash="dot",line_color="#c8890a",line_width=1.5,
        annotation_text="  Target 80%",annotation_font_color="#c8890a",annotation_font_size=10)
    fig.update_layout(**CTH,
        yaxis=dict(range=[0,115],ticksuffix="%",gridcolor='#eef1f5',tickfont=dict(size=9,color='#3a4a65')),
        xaxis=dict(gridcolor='#dde3ec',tickfont=dict(size=10,color='#3a4a65')),
        title=dict(text="Indikator Psikologis & Konsistensi",font=dict(size=13,color='#1a2540')),height=300)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("psiko"))

def ch_progress(r, key=None):
    sw=r["sw"]; mn=r["mn"]; mx=r["mx"]
    gap=abs(r["gap"]) if r["gap"]<0 else 0
    ppm = gap/8+8
    weeks = list(range(0,9))
    preds = [min(mx+30, sw+ppm*w) for w in weeks]
    fig = go.Figure()
    fig.add_hrect(y0=mn,y1=mx,fillcolor="rgba(26,138,74,.07)",layer="below",line_width=0,
                  annotation_text="  Zona Aman",annotation_position="top right",
                  annotation_font=dict(color="#1a8a4a",size=10))
    fig.add_trace(go.Scatter(x=weeks,y=preds,mode='lines+markers+text',
        line=dict(color='#3b6cb7',width=2.5),
        marker=dict(size=8,color='#3b6cb7',line=dict(color='#ffffff',width=1.5)),
        text=[f"{v:.0f}" for v in preds],textposition='top center',
        textfont=dict(size=9,color='#3a4a65'),name='Proyeksi Skor'))
    fig.add_trace(go.Scatter(x=[0],y=[sw],mode='markers',
        marker=dict(size=12,color='#c8890a',symbol='star'),
        name=f'Skor Sekarang ({sw:.0f})'))
    fig.add_hline(y=mn,line_dash="dash",line_color="#d4620a",line_width=1.5,
        annotation_text=f"  Minimum ({mn})",annotation_font_color="#d4620a",annotation_font_size=10)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter',color='#3a4a65'),margin=dict(l=10,r=10,t=45,b=30),
        xaxis=dict(title="Minggu ke-",tickvals=weeks,gridcolor='#eef1f5',title_font=dict(color='#6a7a95'),tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(range=[max(400,sw-100),min(1000,mx+60)],gridcolor='#eef1f5',title="Proyeksi Skor",title_font=dict(color='#6a7a95'),tickfont=dict(size=9,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)',font=dict(color='#3a4a65')),
        title=dict(text="Proyeksi Skor 8 Minggu ke Depan",font=dict(size=13,color='#1a2540')),height=340)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("prog"))

# ══════════════════════════════════════════════════════════
# PDF EXPORT — CHANGE 1: rounded total skor + alt recommendations
# ══════════════════════════════════════════════════════════
def generate_pdf(r):
    now  = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    nama = r.get("nama","—")
    jenjang_lbl = r.get("jenjang","S1 (Sarjana)")
    bobot_rows = "".join(
        f"<tr><td>{SUBTES_FULL[k]}</td><td>{int(r['bobot'][k]*100)}%</td>"
        f"<td>{r['skor'][k]}</td><td>{r['skor'][k]*r['bobot'][k]:.1f}</td></tr>"
        for k in SUBTES)
    lgbm_txt = ""
    if r.get("lgbm_r") and r["lgbm_r"].get("ok"):
        h = r["lgbm_r"]
        kp = f"{h['kpct']:.1f}%" if h.get("kpct") else "—"
        lgbm_txt = f"<p><strong>Rekomendasi Strategi Skoolnow AI AI:</strong> {h['strategi']} (kepercayaan: {kp})</p>"
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

    # ── Rekomendasi alternatif untuk PDF ──
    skor = r["skor"]
    sw   = r["sw"]
    alt_kampus, alt_ptn = get_rekomendasi_alternatif(
        skor, sw, r["prodi"], r["kampus"], r["jenjang"], top_n=5
    )
    def alt_rows(items, show_kampus=False):
        rows = ""
        for item in items:
            gap_str = f"+{item['gap']:.0f}" if item["gap"] >= 0 else f"{item['gap']:.0f}"
            if show_kampus:
                col1, col2 = item["kampus"], item["prodi"]
            else:
                col1, col2 = item["prodi"], item["kampus"]
            rows += f"<tr><td>{col1}</td><td>{col2}</td><td>{item['sw']:.0f}</td><td>{item['mn']}–{item['mx']}</td><td>{gap_str}</td><td>{item['icon']} {item['kat']}</td><td>{item['ppct']:.0f}%</td></tr>"
        return rows

    alt_kampus_html = ""
    if alt_kampus:
        alt_kampus_html = f"""
        <h2>🏛️ Rekomendasi Prodi Lain di {r['kampus']}</h2>
        <table>
          <tr><th>Program Studi</th><th>Kampus</th><th>Skor Kamu</th><th>Rentang Aman</th><th>Gap</th><th>Status</th><th>Peluang</th></tr>
          {alt_rows(alt_kampus, show_kampus=False)}
        </table>"""

    alt_ptn_html = ""
    if alt_ptn:
        alt_ptn_html = f"""
        <h2>🔄 {r['prodi']} di Kampus Lain</h2>
        <table>
          <tr><th>Kampus</th><th>Program Studi</th><th>Skor Kamu</th><th>Rentang Aman</th><th>Gap</th><th>Status</th><th>Peluang</th></tr>
          {alt_rows(alt_ptn, show_kampus=True)}
        </table>"""

    # CHANGE 1: round skor tertimbang to integer in PDF
    sw_rounded = round(r["sw"])

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8">
<title>Laporan Skoolnow AI — {nama}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',sans-serif;font-size:11pt;color:#1e293b;background:#fff;padding:1.2cm 1.8cm}}
h1{{font-size:18pt;font-weight:800;color:#0f172a}}
h2{{font-size:11pt;font-weight:700;color:#0f172a;margin:16px 0 7px;border-bottom:2px solid #3b6cb7;padding-bottom:3px}}
p{{font-size:10pt;line-height:1.65;color:#374151;margin-bottom:5px}}
.hdr{{background:linear-gradient(135deg,#2a4a8c,#3b6cb7);color:#fff;padding:1.1cm 1.4cm;border-radius:12px;margin-bottom:.9cm}}
.brand{{font-size:12pt;font-weight:800;color:#ffd166;margin-bottom:3px}}
.hdr .sub{{color:rgba(255,255,255,.75);font-size:9pt;margin-top:3px}}
.kpi-row{{display:flex;gap:10px;margin-bottom:10px}}
.kpi{{flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center}}
.kpi .val{{font-size:18pt;font-weight:800}}
.kpi .lbl{{font-size:7.5pt;color:#64748b;text-transform:uppercase;letter-spacing:.05em}}
.green{{color:#16a34a}}.orange{{color:#ca8a04}}.red{{color:#dc2626}}.blue{{color:#1d4ed8}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:9px}}
th{{background:#eef3fc;text-align:left;padding:5px 9px;font-weight:600;border:1px solid #dde3ec}}
td{{padding:5px 9px;border:1px solid #dde3ec;color:#374151}}
tr:nth-child(even) td{{background:#f7f9fc}}
.footer{{margin-top:.8cm;font-size:8pt;color:#94a3b8;text-align:center;border-top:1px solid #e2e8f0;padding-top:7px}}
@media print{{body{{padding:.8cm 1cm}}}}
.badge-sa{{background:#e6f5ee;color:#148a42;padding:3px 10px;border-radius:99px;font-weight:700}}
.badge-a {{background:#edf6ff;color:#1a5fa0;padding:3px 10px;border-radius:99px;font-weight:700}}
.badge-br{{background:#fff4e6;color:#d4620a;padding:3px 10px;border-radius:99px;font-weight:700}}
.badge-na{{background:#fff0f0;color:#c0392b;padding:3px 10px;border-radius:99px;font-weight:700}}
</style></head><body>
<div class="hdr">
  <div class="brand">🎯 Skoolnow AI</div>
  <h1>AI UTBK Readiness Report</h1>
  <div class="sub">Laporan Kesiapan UTBK · {now}</div>
</div>
<h2>👤 Profil Siswa</h2>
<table><tr><th>Nama</th><td>{nama}</td><th>Jenjang</th><td>{jenjang_lbl}</td></tr>
<tr><th>Program Studi</th><td>{r['prodi']}</td><th>Kampus Target</th><td>{r['kampus']}</td></tr></table>
<h2>📊 Ringkasan Hasil</h2>
<div class="kpi-row">
<div class="kpi"><div class="lbl">Skor Tertimbang</div><div class="val {gc}">{sw_rounded}</div><div class="lbl">dari 1000</div></div>
<div class="kpi"><div class="lbl">Rentang Aman</div><div class="val blue">{r['mn']} – {r['mx']}</div></div>
<div class="kpi"><div class="lbl">Peluang Lolos</div><div class="val {pc}">{r['ppct']:.0f}%</div></div>
<div class="kpi"><div class="lbl">Gap vs Minimum</div><div class="val {gc}">{r['gap']:+.0f}</div></div>
</div>
<p>Status: <span class="badge-{r['kat_badge'].replace('badge-','')}">{r['kat_icon']} {r['kat']}</span> | Skor Aman: {r['mn']}–{r['mx']}</p>
<p>Kategori: <strong>Tidak Aman</strong> = &lt;{r['mn']-70} | <strong>Berisiko</strong> = {r['mn']-70}–{r['mn']-1} | <strong>Aman</strong> = {r['mn']}–{r['mx']-1} | <strong>Sangat Aman</strong> = ≥{r['mx']}</p>
{lgbm_txt}
<h2>📋 Bobot & Skor Subtes</h2>
<table><tr><th>Subtes</th><th>Bobot</th><th>Skor</th><th>Kontribusi</th></tr>
{bobot_rows}
<tr style="background:#eef3fc"><th colspan="2">Total Skor Tertimbang</th><th colspan="2"><strong>{sw_rounded}</strong></th></tr></table>
<h2>🧠 Indikator Psikologis</h2>
<table>
<tr><th>Fokus</th><td>{r['fokus']}/5</td><th>Percaya Diri</th><td>{r['pede']}/5</td></tr>
<tr><th>Kecemasan</th><td>{r['cemas']}/5</td><th>Distraksi</th><td>{r['distrak']}/5</td></tr>
<tr><th>Kesiapan Mental</th><td>{r['psiko']:.0f}/100</td><th>Konsistensi</th><td>{r['konsist']:.0f}/100</td></tr>
<tr><th>Stabilitas</th><td>{r['stab']:.0f}/100</td><th>Risiko Underperform</th><td>{r['risk'][0]} {r['risk'][1]}</td></tr></table>
{alt_kampus_html}
{alt_ptn_html}
<h2>📅 Rencana Belajar Mingguan (8 Minggu)</h2>
{minggu_html}
<div class="footer">🎯 Skoolnow AI — AI UTBK Intelligence · Data SNPMB/BPPP Kemdikbud 2025/2026 · Skor skala 200–1000</div>
<div style="margin-top:16px;text-align:center">
<button onclick="window.print()" style="padding:8px 20px;background:#3b6cb7;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:11pt;color:#fff">
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
      <div class="topbar-brand"><img src="data:image/png;base64,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" style="height:38px;width:38px;object-fit:contain;border-radius:6px" /> Skoolnow AI <span class="topbar-tag">AI UTBK Intelligence · S1 · D4 · D3 · 2025/2026</span></div>
      <div style="flex:1"></div>
      <div class="step-pill {s1}">{'✓' if p in ['survey','result'] else '①'} Beranda</div>
      <div class="step-pill {s2}">{'✓' if p=='result' else '②'} Input Data</div>
      <div class="step-pill {s3}">③ Hasil Analisis</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def prog_bar(label, val, color):
    pct = max(0, min(100, val))
    st.markdown(f"""<div class="prog-wrap">
      <div class="prog-lbl"><span>{label}</span>
        <span style="color:{color};font-weight:800;font-family:'Space Grotesk',sans-serif">{pct:.0f}/100</span></div>
      <div class="prog-bg">
        <div class="prog-fill" style="width:{pct:.0f}%;background:linear-gradient(90deg,{color},{color}cc)"></div>
      </div>
    </div>""", unsafe_allow_html=True)

def bobot_chips(prodi):
    b = get_bobot(prodi)
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

def render_skor_legend(mn, mx):
    st.markdown(f"""<div class="skor-legend">
      <span class="skor-legend-item sl-na">🔴 Tidak Aman &lt;{mn-70}</span>
      <span class="skor-legend-item sl-br">⚡ Berisiko {mn-70}–{mn-1}</span>
      <span class="skor-legend-item sl-a">✅ Aman {mn}–{mx-1}</span>
      <span class="skor-legend-item sl-sa">🏆 Sangat Aman ≥{mx}</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE: HOME — CHANGE 3: Feature explanation panel added
# ══════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="ticker-wrap">
      <div class="ticker-inner">
        <span class="ticker-item">🎯 Skoolnow AI v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1</span> · <span>D4</span> · <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Data Estimasi Historis 2022–2024</span>
        <span class="ticker-item">📚 <span>60+</span> Prodi S1 · <span>D3/D4</span> dari database xlsx</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📊 4 Kategori Skor: <span>Tidak Aman</span> · <span>Berisiko</span> · <span>Aman</span> · <span>Sangat Aman</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
        <span class="ticker-item">🎯 Skoolnow AI v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1</span> · <span>D4</span> · <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Data Estimasi Historis 2022–2024</span>
        <span class="ticker-item">📚 <span>60+</span> Prodi S1 · <span>D3/D4</span> dari database xlsx</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📊 4 Kategori Skor: <span>Tidak Aman</span> · <span>Berisiko</span> · <span>Aman</span> · <span>Sangat Aman</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="hero">
      <div class="hero-badge">🚀 v5.0 · S1 · D4 · D3 · 30 PTN · Database xlsx Real-time</div>
      <h1>Skoolnow AI — Analisis Kesiapan<br><span>UTBK</span> Berbasis AI</h1>
      <p>Platform AI untuk memahami peluang, gap skor, dan strategi belajar personal.<br>
         Data skor estimasi S1/D4/D3 dari database SNPMB/BPPP Kemdikbud 2022–2024.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="stat-row">
      <div class="stat-box"><div class="stat-num">30</div><div class="stat-lbl">🏛️ PTN</div></div>
      <div class="stat-box"><div class="stat-num">4</div><div class="stat-lbl">📊 Kategori Skor</div></div>
      <div class="stat-box"><div class="stat-num">7</div><div class="stat-lbl">📝 Subtes TPS</div></div>
      <div class="stat-box"><div class="stat-num">8</div><div class="stat-lbl">📅 Minggu Rencana</div></div>
    </div>""", unsafe_allow_html=True)

    # ── CHANGE 3: Penjelasan fitur / hasil yang bisa didapat ──
    fitur_items = [
        ("📊", "d1", "Skor Tertimbang (TW)",
         "Skor akhir yang dihitung berdasarkan 7 subtes TPS dengan bobot yang disesuaikan per program studi, persis seperti cara penilaian nyata UTBK."),
        ("🏆", "d2", "4 Kategori Kesiapan",
         "Status lolos dikelompokkan menjadi <b>Tidak Aman &middot; Berisiko &middot; Aman &middot; Sangat Aman</b> lengkap dengan estimasi persentase peluang lolos."),
        ("📏", "d3", "Gap vs Skor Minimum",
         "Selisih skor kamu dengan batas minimum dan batas aman kampus/prodi target &mdash; kamu tahu persis berapa poin yang perlu ditingkatkan."),
        ("🎯", "d4", "Rekomendasi Prodi Alternatif",
         "Jika peluang masih kurang, Skoolnow AI menampilkan prodi lain di kampus yang sama dan prodi serupa di kampus berbeda yang lebih sesuai skormu."),
        ("🤖", "d5", "Strategi Belajar AI (LightGBM)",
         "Model machine learning menganalisis kebiasaan &amp; kondisi psikologismu lalu merekomendasikan strategi yang paling tepat dari 4 pendekatan berbeda."),
        ("📅", "d6", "Rencana Belajar 8 Minggu",
         "Jadwal belajar personal mingguan &mdash; Fondasi, Intensif, Pemantapan, hingga Final &mdash; dengan target skor per minggu dan tugas harian yang spesifik."),
        ("📡", "d1", "Radar TPS vs Profil Ideal",
         "Grafik radar interaktif membandingkan skormu dengan profil ideal prodi &mdash; langsung terlihat subtes mana yang perlu diperkuat lebih dulu."),
        ("🧠", "d2", "Analisis Psikologis",
         "Indikator Kesiapan Mental, Konsistensi Belajar, dan Stabilitas Mental yang membantumu memahami faktor non-akademik yang mempengaruhi performa UTBK."),
        ("📄", "d3", "Export Laporan PDF",
         "Seluruh hasil analisis &mdash; skor, gap, rekomendasi alternatif, dan rencana 8 minggu &mdash; bisa diunduh sebagai laporan HTML siap cetak menjadi PDF."),
    ]
    items_html = "".join(
        f'<div class="fitur-item {d}">'
        f'<span class="fitur-item-icon">{icon}</span>'
        f'<div class="fitur-item-title">{title}</div>'
        f'<div class="fitur-item-desc">{desc}</div>'
        f'</div>'
        for icon, d, title, desc in fitur_items
    )
    st.markdown(
        f'<div class="fitur-panel">'
        f'<div class="fitur-panel-title">&#128269; Apa Saja yang Bisa Kamu Dapatkan dari Skoolnow AI AI?</div>'
        f'<div class="fitur-grid-3">{items_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Legenda 4 kategori
    st.markdown("""<div style="background:#fff;border:1px solid #e0e8f4;border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.2rem;box-shadow:0 2px 12px rgba(30,60,140,.08)">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:.9rem;font-weight:700;color:#12203f;margin-bottom:.7rem">📊 4 Kategori Rentang Skor Skoolnow AI</div>
      <div style="display:flex;gap:.6rem;flex-wrap:wrap">
        <span style="background:#fff0f0;color:#c0392b;border:1.5px solid #f4a0a0;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">🔴 Tidak Aman — Butuh peningkatan signifikan</span>
        <span style="background:#fff4e6;color:#e67e22;border:1.5px solid #f4c08a;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">⚡ Berisiko — Mendekati zona aman</span>
        <span style="background:#edf6ff;color:#1a5fa0;border:1.5px solid #90c0f0;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">✅ Aman — Dalam zona aman</span>
        <span style="background:#e6f5ee;color:#148a42;border:1.5px solid #9adbb8;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">🏆 Sangat Aman — Melampaui batas aman</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="feat-grid">
      <div class="feat-card d1"><span class="feat-icon">🗃️</span><div class="feat-title">Database xlsx Real</div><div class="feat-desc">Data dari file xlsx estimasi historis UTBK 2022–2024 langsung terhubung</div></div>
      <div class="feat-card d2"><span class="feat-icon">📊</span><div class="feat-title">4 Kategori Skor</div><div class="feat-desc">Tidak Aman · Berisiko · Aman · Sangat Aman dengan rentang skor visual</div></div>
      <div class="feat-card d3"><span class="feat-icon">🤖</span><div class="feat-title">AI LightGBM</div><div class="feat-desc">Prediksi strategi belajar otomatis dari model machine learning</div></div>
      <div class="feat-card d4"><span class="feat-icon">📄</span><div class="feat-title">Export PDF</div><div class="feat-desc">Laporan lengkap 8 minggu + rekomendasi alternatif siap cetak</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)

    if _DB_ERR:
        st.markdown(f'<div class="al al-d"><h4>⚠️ Database Error</h4>{_DB_ERR}<br>Pastikan file xlsx tersedia atau URL GitHub benar.</div>', unsafe_allow_html=True)
    elif _PTN_S1:
        n_ptn_s1 = len(_PTN_S1)
        n_prodi_s1 = sum(len(v) for v in _PTN_S1.values())
        n_ptn_d3 = len(_PTN_D3) if _PTN_D3 else 0
        n_ptn_d4 = len(_PTN_D4) if _PTN_D4 else 0
        st.markdown(f'<div class="al al-s"><h4>✅ Database Berhasil Dimuat</h4>S1: <strong>{n_ptn_s1} PTN</strong>, {n_prodi_s1}+ prodi · D3: <strong>{n_ptn_d3} PTN</strong> · D4: <strong>{n_ptn_d4} PTN</strong><br><small style="color:#6a7a95">Estimasi historis UTBK 2022–2024 · Data resmi: snpmb.bppp.kemdikbud.go.id</small></div>', unsafe_allow_html=True)

    ai_status = f'<div class="al al-s"><h4>✅ Model AI Aktif</h4>File: <code>{lgbm_fname}</code></div>' if lgbm_model else '<div class="al al-w"><h4>⚠️ Model AI Tidak Ditemukan</h4>Letakkan <code>lgbm_model_2_.pkl</code> di folder yang sama. Kalkulasi manual tetap berjalan.</div>'
    st.markdown(ai_status, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_cta, col_info = st.columns([2,3])
    with col_cta:
        if st.button("🚀  Mulai Analisis UTBK Sekarang", type="primary", use_container_width=True):
            st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with col_info:
        st.markdown("""<div style="padding:.7rem 0;font-size:.81rem;color:#6a7a9a;line-height:1.8">
          ⏱ Waktu pengisian: ~5 menit &nbsp;·&nbsp; 🔒 Data tidak tersimpan &nbsp;·&nbsp; 📱 Mobile friendly
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE: SURVEY — CHANGE 4: urutan Nama → Jenjang → Kampus → Jurusan (sudah benar, diperkuat)
# ══════════════════════════════════════════════════════════
def step1():
    st.markdown("""<div class="al al-i d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>👤 Langkah 1 dari 4 — Profil &amp; Target</h4>
      Isi <strong>① Nama Lengkap</strong> → pilih <strong>② Jenjang Pendidikan</strong> → pilih <strong>③ Kampus</strong> → lalu <strong>④ Jurusan/Prodi</strong>.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Profil &amp; Target</h3>', unsafe_allow_html=True)
    d = st.session_state.data

    # ① Nama Lengkap — PERTAMA
    nama = st.text_input("① Nama Lengkap", value=d.get("nama",""), placeholder="Masukkan nama kamu...")

    # ② Jenjang Pendidikan — KEDUA
    prev_jenjang = d.get("jenjang", DAFTAR_JENJANG[0])
    if prev_jenjang not in DAFTAR_JENJANG:
        prev_jenjang = DAFTAR_JENJANG[0]
    jenjang = st.radio(
        "② Jenjang Pendidikan yang Dituju",
        DAFTAR_JENJANG,
        index=DAFTAR_JENJANG.index(prev_jenjang),
        horizontal=True,
        help="S1 = Sarjana (4 th) | D4 = Sarjana Terapan (4 th, vokasi) | D3 = Diploma Tiga (3 th, vokasi)"
    )

    # ③ Kampus — KETIGA (setelah jenjang dipilih)
    daftar_ptn = get_daftar_ptn(jenjang)
    if not daftar_ptn:
        st.warning(f"⚠️ Data PTN untuk jenjang {jenjang} belum tersedia. Cek koneksi atau file xlsx.")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("◀ Kembali ke Beranda"):
            st.session_state.page = "home"; st.rerun()
        return

    prev_kampus = d.get("kampus", daftar_ptn[0])
    if prev_kampus not in daftar_ptn:
        prev_kampus = daftar_ptn[0]
    kampus = st.selectbox(
        "③ Kampus Target (PTN)",
        daftar_ptn,
        index=daftar_ptn.index(prev_kampus),
        help="Pilih PTN yang kamu tuju — daftar disesuaikan dengan jenjang yang dipilih"
    )

    # ④ Jurusan/Prodi — KEEMPAT (setelah kampus dipilih)
    daftar_prodi = get_daftar_prodi(kampus, jenjang)
    if not daftar_prodi:
        st.warning(f"⚠️ Tidak ada data prodi untuk {kampus} ({jenjang}).")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    prev_prodi = d.get("prodi", daftar_prodi[0])
    if prev_prodi not in daftar_prodi:
        prev_prodi = daftar_prodi[0]
    prodi = st.selectbox(
        "④ Program Studi / Jurusan",
        daftar_prodi,
        index=daftar_prodi.index(prev_prodi),
        help="Pilih program studi setelah memilih kampus — daftar difilter otomatis"
    )

    # Info skor aman
    info = get_skor_info(kampus, prodi, jenjang)
    mn, mx = info["mn"], info["mx"]
    render_skor_legend(mn, mx)

    st.markdown(f"""<div class="al al-i" style="margin-top:.7rem">
      <h4>🏛️ {kampus}</h4>
      Rentang skor aman <strong>{jenjang}</strong> — <strong>{prodi}</strong>:
      <br>
      <span style="font-size:1.1rem;font-weight:800;color:#3464c8">{mn} – {mx}</span>
      <br><small style="color:#6a7a95">Estimasi historis UTBK 2022–2024 · Sumber: SNPMB/BPPP Kemdikbud & referensi media pendidikan</small>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**Distribusi bobot subtes untuk _{prodi}_:**")
    bobot_chips(prodi)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Lanjut → Skor TPS ▶", type="primary"):
        if not nama.strip():
            st.error("❌ Nama harus diisi!")
            return
        st.session_state.data.update({"nama":nama,"jenjang":jenjang,"kampus":kampus,"prodi":prodi})
        st.session_state.step=2; st.rerun()

def step2():
    st.markdown("""<div class="al al-p d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>📊 Langkah 2 dari 4 — Skor TPS</h4>
      Masukkan skor tryout terbaru untuk 7 subtes TPS.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Skor TPS (Tes Potensi Skolastik)</h3>', unsafe_allow_html=True)
    st.caption(f"Masukkan skor tryout terbaru. Skala: {SKOR_MIN_TPS} – {SKOR_MAX_TPS}")
    d = st.session_state.data
    skor = {}
    pairs = [("PU","PPU"),("PBM","PK"),("LBI","LBE"),("PM",None)]
    for pair in pairs:
        cols = st.columns(2)
        for col, k in zip(cols, pair):
            if k is None: continue
            with col:
                skor[k] = st.number_input(
                    f"{SUBTES_FULL[k]} ({k})",
                    min_value=SKOR_MIN_TPS, max_value=SKOR_MAX_TPS,
                    value=int(d.get(k, 550)), step=5, key=f"n_{k}",
                )

    prodi  = d.get("prodi","")
    bobot  = get_bobot(prodi)
    cats   = [SUBTES_FULL[k] for k in SUBTES]+[SUBTES_FULL[SUBTES[0]]]
    vals   = [skor[k] for k in SUBTES]+[skor[SUBTES[0]]]
    ideal  = [min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES]+[min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig    = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal',
        fillcolor='rgba(200,137,10,.08)',line=dict(color='#c8890a',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)',line=dict(color='#3b6cb7',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9,color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9.5,color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#3a4a65')),
        title=dict(text=f"Preview Radar — {prodi}",font=dict(size=13,color='#1a2540')),height=380)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key="survey_radar")
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=1; st.rerun()
    with cb:
        if st.button("Lanjut → Psikologis ▶", type="primary"):
            st.session_state.data.update(skor); st.session_state.step=3; st.rerun()

def step3():
    st.markdown("""<div class="al al-w d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>🧠 Langkah 3 dari 4 — Kondisi Psikologis</h4>
      Nilai kondisi mental dan emosional kamu saat belajar.
    </div>""", unsafe_allow_html=True)
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
    pc = "#148a42" if psiko>=65 else "#d4900a" if psiko>=45 else "#c0392b"
    pct_p = f"{psiko:.0f}%"
    st.markdown(f"""<div class="score-ring-wrap">
      <div class="score-ring" style="--pct:{pct_p};background:conic-gradient({pc} {pct_p},#e8eef8 {pct_p})">
        <div class="score-ring-val" style="color:{pc}">{psiko:.0f}</div>
        <div class="score-ring-sub">Mental Score</div>
      </div>
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
    st.markdown("""<div class="al al-s d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>📚 Langkah 4 dari 4 — Kebiasaan Belajar</h4>
      Langkah terakhir! Data ini digunakan oleh model AI untuk rekomendasi strategi.
    </div>""", unsafe_allow_html=True)
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
    kc = "#148a42" if konsist>=65 else "#d4900a" if konsist>=45 else "#c0392b"
    pct_deg = f"{konsist:.0f}%"
    st.markdown(f"""<div class="score-ring-wrap">
      <div class="score-ring" style="--pct:{pct_deg};background:conic-gradient({kc} {pct_deg},#e8eef8 {pct_deg})">
        <div class="score-ring-val" style="color:{kc}">{konsist:.0f}</div>
        <div class="score-ring-sub">Konsistensi</div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=3; st.rerun()
    with cb:
        if st.button("🎯  Lihat Hasil Analisis Skoolnow AI", type="primary"):
            st.session_state.data.update({"jam":jb,"hari":hb,"latihan":lat,"tryout":try_,"review":rev})
            st.session_state.result = compute(st.session_state.data)
            st.session_state.page="result"; st.rerun()

def page_survey():
    step_bar(st.session_state.step)
    {1:step1, 2:step2, 3:step3, 4:step4}[st.session_state.step]()

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

    kat_cls_map = {
        "Sangat Aman":"badge-sa", "Aman":"badge-a",
        "Berisiko":"badge-br",    "Tidak Aman":"badge-na"
    }
    sb_cls = kat_cls_map.get(r["kat"], "badge-na")

    st.markdown(f"""<div class="hero">
      <div class="hero-badge">🎓 {jenjang_lbl} · {r['prodi']} · {r['kampus']}</div>
      <h1 style="font-size:1.65rem!important">{salam}, <span>{nama}!</span> 👋</h1>
      <p>Hasil analisis <strong style="color:#ffd166">Skoolnow AI AI</strong> berdasarkan skor TPS, psikologis, dan kebiasaan belajarmu</p>
      <div style="margin-top:1rem">
        <span class="status-badge {sb_cls}">{r['kat_icon']} {r['kat']} · Skor {r['sw']:.0f}</span>
        &nbsp;
        <span class="status-badge badge-a">📊 Peluang ~{r['ppct']:.0f}%</span>
      </div>
    </div>""", unsafe_allow_html=True)

    mn, mx = r["mn"], r["mx"]
    gc = "c-green" if r["gap"]>=0 else "c-red"
    pc = "c-green" if r["ppct"]>=65 else "c-orange" if r["ppct"]>=35 else "c-red"
    kc_map = {"Sangat Aman":"c-green","Aman":"c-blue","Berisiko":"c-orange","Tidak Aman":"c-red"}
    kc = kc_map.get(r["kat"],"c-red")

    k1,k2,k3,k4,k5 = st.columns(5)
    kampus_short = r["kampus"].split("(")[0].strip()[:22]
    for i,(col,lbl,val,cls,sub) in enumerate([
        (k1,"Skor Tertimbang",f"{r['sw']:.0f}",kc,"dari 1000"),
        (k2,"Rentang Aman",f"{mn}–{mx}","c-blue",kampus_short),
        (k3,"Peluang Lolos",f"{r['ppct']:.0f}%",pc,r["kat"]),
        (k4,"Gap vs Minimum",f"{r['gap']:+.0f}",gc,f"Min {mn}"),
        (k5,"Risiko Underperform",r["risk"][0],
             "c-green" if r["risk"][0]=="Rendah" else "c-orange" if r["risk"][0]=="Sedang" else "c-red",
             r["risk"][1]),
    ]):
        with col:
            st.markdown(f"""<div class="card d{i+1}">
              <div class="kpi-lbl">{lbl}</div>
              <div class="kpi-val {cls}">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)
    render_skor_legend(mn, mx)

    if r.get("lgbm_r") and r["lgbm_r"].get("ok"):
        h=r["lgbm_r"]; det=h.get("detail",{})
        kpct = f"{h['kpct']:.1f}%" if h.get("kpct") else ""
        tips = "".join(f"<li>{t}</li>" for t in det.get("tips",[]))
        st.markdown(f"""<div class="al al-s">
          <h4>🤖 Rekomendasi Strategi Skoolnow AI AI — {det.get('icon','')} {h['strategi']}
            <span style="font-size:.78rem;font-weight:500;color:#6a7a95"> · Kepercayaan: {kpct}</span></h4>
          <em>{det.get('desc','')}</em>
          <ul style="margin-top:.35rem">{tips}</ul>
        </div>""", unsafe_allow_html=True)

    if r["kat"] == "Sangat Aman":
        st.markdown(f"""<div class="al al-s"><h4>🏆 Status: SANGAT AMAN</h4>
          Skor tertimbang <strong>{r['sw']:.0f}</strong> melampaui batas aman atas {mx}.
          Pertahankan performa & jaga kondisi mental menjelang UTBK!</div>""", unsafe_allow_html=True)
    elif r["kat"] == "Aman":
        st.markdown(f"""<div class="al al-s"><h4>✅ Status: AMAN</h4>
          Skor {r['sw']:.0f} dalam zona aman ({mn}–{mx-1}).
          Tambah <strong>{mx-r['sw']:.0f} poin</strong> lagi untuk zona Sangat Aman.</div>""", unsafe_allow_html=True)
    elif r["kat"] == "Berisiko":
        st.markdown(f"""<div class="al al-br"><h4>⚡ Status: BERISIKO</h4>
          Kurang <strong>{mn-r['sw']:.0f} poin</strong> dari batas aman minimum {mn}.
          Intensifkan latihan — masih bisa dikejar!</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="al al-na"><h4>🔴 Status: TIDAK AMAN</h4>
          Gap <strong>{abs(r['gap']):.0f} poin</strong> dari minimum {mn}.
          Butuh peningkatan signifikan atau pertimbangkan PTN/prodi alternatif.</div>""", unsafe_allow_html=True)

    t1,t2,t3,t4,t5,t6,t7 = st.tabs([
        "📡 Radar & Skor TPS",
        "📊 Posisi & Peluang",
        "🎯 Alternatif",
        "🔀 Pipeline & Bobot",
        "🚀 Strategi Belajar",
        "📅 Rencana Mingguan",
        "📄 Export PDF",
    ])

    with t1:
        st.markdown('<div class="sec">📡 Radar TPS vs Profil Ideal Prodi</div>', unsafe_allow_html=True)
        ch_radar(r["skor"],r["bobot"],r["prodi"], key="r_radar_t1")
        st.markdown('<div class="sec">📊 Skor Per Subtes vs Target</div>', unsafe_allow_html=True)
        ch_bar_subtes(r["skor"],r["bobot"],r["info"], key="r_bar_t1")
        st.markdown('<div class="sec">Detail Skor Subtes</div>', unsafe_allow_html=True)
        df_data = []
        for k in SUBTES:
            sv = r["skor"][k]
            status = "✅ Kuat" if sv>=750 else "⚡ Sedang" if sv>=550 else "🔴 Perlu Fokus"
            df_data.append({"Subtes":SUBTES_FULL[k],"Bobot (%)":f"{r['bobot'][k]*100:.0f}%",
                            "Skor":sv,"Kontribusi":f"{sv*r['bobot'][k]:.1f}","Status":status})
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True,
            column_config={"Skor": st.column_config.ProgressColumn("Skor",min_value=200,max_value=1000,format="%d")})

    with t2:
        st.markdown('<div class="sec">📊 Posisi Skor — 4 Kategori</div>', unsafe_allow_html=True)
        ch_skor_gauge(r["sw"], mn, mx, key="r_gauge_t2")
        render_skor_legend(mn, mx)
        st.markdown('<div class="sec">📋 Ringkasan Peluang di Semua Prodi</div>', unsafe_allow_html=True)
        daftar_prodi_ptn = get_daftar_prodi(r["kampus"], r["jenjang"])
        rows = []
        for prodi_lain in daftar_prodi_ptn[:30]:
            info_l = get_skor_info(r["kampus"], prodi_lain, r["jenjang"])
            bobot_l = get_bobot(prodi_lain)
            sw_l = hitung_tw(r["skor"], bobot_l)
            kat_l, _, _, icon_l, pct_l = get_kategori_skor(sw_l, info_l["mn"], info_l["mx"])
            rows.append({
                "Program Studi": prodi_lain,
                "Skor Aman": f"{info_l['mn']}–{info_l['mx']}",
                "Skor Kamu": f"{sw_l:.0f}",
                "Status": f"{icon_l} {kat_l}",
                "Est. Peluang": f"{pct_l:.0f}%"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        d1,d2,d3 = st.columns(3)
        with d1: st.metric("Skor Minimum",mn)
        with d2: st.metric("Skor Sangat Aman (atas)",mx)
        with d3: st.metric("Skor Kamu",f"{r['sw']:.0f}",delta=f"{r['gap']:+.0f}",delta_color="normal" if r["gap"]>=0 else "inverse")

    with t3:
        sw   = r["sw"]
        skor = r["skor"]
        alt_kampus, alt_ptn = get_rekomendasi_alternatif(
            skor, sw, r["prodi"], r["kampus"], r["jenjang"]
        )
        kat_cls_info = {"Sangat Aman":"al-s","Aman":"al-i","Berisiko":"al-w","Tidak Aman":"al-d"}
        info_cls = kat_cls_info.get(r["kat"], "al-i")
        st.markdown(f'''<div class="al {info_cls}" style="padding:.75rem 1.1rem;margin-bottom:1rem">
          <h4>{r["kat_icon"]} Skor Tertimbang Kamu: <strong>{sw:.0f}</strong> &nbsp;·&nbsp; Status: {r["kat"]}</h4>
          Rekomendasi di bawah dihitung menggunakan <strong>skor TPS kamu yang sama</strong>
          dengan bobot masing-masing program studi — skor kamu mungkin berbeda tiap prodi.
        </div>''', unsafe_allow_html=True)

        st.markdown('<div class="sec">🏛️ Prodi Lain di Kampus yang Sama</div>', unsafe_allow_html=True)
        st.caption(f"Prodi lain di {r['kampus']} — diurutkan dari peluang terbaik")
        if alt_kampus:
            fa1, fa2, fa3 = st.tabs(["Semua Prodi", "✅ Aman & Sangat Aman", "⚡ Berisiko & Tidak Aman"])
            with fa1:
                render_alt_cards(alt_kampus, show_kampus=False)
            with fa2:
                aman_list = [x for x in alt_kampus if x["kat"] in ("Sangat Aman","Aman")]
                if aman_list: render_alt_cards(aman_list, show_kampus=False)
                else: st.info("Tidak ada prodi dengan kategori Aman/Sangat Aman.")
            with fa3:
                risiko_list = [x for x in alt_kampus if x["kat"] in ("Berisiko","Tidak Aman")]
                if risiko_list: render_alt_cards(risiko_list, show_kampus=False)
                else: st.info("Semua prodi masuk kategori Aman atau Sangat Aman! 🎉")
        else:
            st.info("Data prodi untuk kampus ini tidak tersedia.")

        st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">🔄 Prodi Serupa di Kampus Berbeda</div>', unsafe_allow_html=True)
        st.caption(f"Mencari \"{r['prodi']}\" atau prodi serupa di PTN lain")
        if alt_ptn:
            fb1, fb2, fb3 = st.tabs(["Semua PTN", "✅ Aman & Sangat Aman", "⚡ Berisiko & Tidak Aman"])
            with fb1:
                render_alt_cards(alt_ptn, show_kampus=True)
            with fb2:
                aman_ptn = [x for x in alt_ptn if x["kat"] in ("Sangat Aman","Aman")]
                if aman_ptn: render_alt_cards(aman_ptn, show_kampus=True)
                else: st.info("Tidak ada PTN dengan kategori Aman/Sangat Aman untuk prodi ini.")
            with fb3:
                risiko_ptn = [x for x in alt_ptn if x["kat"] in ("Berisiko","Tidak Aman")]
                if risiko_ptn: render_alt_cards(risiko_ptn, show_kampus=True)
                else: st.info("Semua PTN masuk kategori Aman atau Sangat Aman! 🎉")
        else:
            st.info(f"Tidak ditemukan prodi serupa di PTN lain dengan data yang tersedia.")

        st.markdown('<div class="sec">📋 Tabel Ringkasan Semua Alternatif</div>', unsafe_allow_html=True)
        all_alt = []
        for item in alt_kampus[:5]:
            all_alt.append({"Tipe":"Kampus Sama","Program Studi":item["prodi"],"Kampus":item["kampus"],
                "Skor Kamu":f"{item['sw']:.0f}","Rentang Aman":f"{item['mn']}–{item['mx']}",
                "Gap":f"{item['gap']:+.0f}","Status":f"{item['icon']} {item['kat']}","Peluang":f"{item['ppct']:.0f}%"})
        for item in alt_ptn[:5]:
            all_alt.append({"Tipe":"Prodi Serupa","Program Studi":item["prodi"],"Kampus":item["kampus"],
                "Skor Kamu":f"{item['sw']:.0f}","Rentang Aman":f"{item['mn']}–{item['mx']}",
                "Gap":f"{item['gap']:+.0f}","Status":f"{item['icon']} {item['kat']}","Peluang":f"{item['ppct']:.0f}%"})
        if all_alt:
            st.dataframe(pd.DataFrame(all_alt), use_container_width=True, hide_index=True)

    with t4:
        st.markdown('<div class="sec">🔀 Pipeline Kontribusi Subtes</div>', unsafe_allow_html=True)
        ch_pipeline(r["skor"],r["bobot"],r["info"],r["prodi"], key="r_pipe_t3")
        st.markdown(f'<div class="sec">📐 Distribusi Bobot — {r["prodi"]}</div>', unsafe_allow_html=True)
        ch_bobot(r["prodi"], key="r_bobot_t3")
        st.markdown('<div class="sec">Tabel Bobot & Kontribusi</div>', unsafe_allow_html=True)
        df_b = []
        for k in SUBTES:
            df_b.append({"Subtes":SUBTES_FULL[k],"Bobot":f"{r['bobot'][k]*100:.0f}%","Skor":r["skor"][k],
                         "Kontribusi Aktual":f"{r['skor'][k]*r['bobot'][k]:.1f}",
                         "Target Minimum":f"{mn*r['bobot'][k]:.1f}",
                         "Selisih":f"{(r['skor'][k]-mn)*r['bobot'][k]:+.1f}"})
        df_b.append({"Subtes":"TOTAL","Bobot":"100%","Skor":"—",
                     "Kontribusi Aktual":f"{r['sw']:.1f}","Target Minimum":f"{mn:.0f}","Selisih":f"{r['gap']:+.1f}"})
        st.dataframe(pd.DataFrame(df_b), use_container_width=True, hide_index=True)

    with t5:
        st.markdown('<div class="sec">🚀 Strategi Belajar Personal</div>', unsafe_allow_html=True)
        ch_psiko(r["psiko"],r["konsist"],r["stab"], key="r_psiko_t4")
        prog_bar("Kesiapan Mental",r["psiko"],"#3b6cb7")
        prog_bar("Konsistensi Belajar",r["konsist"],"#1a8a4a")
        prog_bar("Stabilitas Mental",r["stab"],"#7048c8")
        st.markdown('<div class="sec">📌 Prioritas Subtes</div>', unsafe_allow_html=True)
        ss = sorted(r["skor"].items(),key=lambda x:x[1])
        lemah3=ss[:3]; kuat2=ss[-2:]
        cp1,cp2 = st.columns(2)
        with cp1:
            il="".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} → perlu +{max(0,750-v)} poin</li>" for k,v in lemah3)
            st.markdown(f'<div class="al al-d"><h4>🔴 3 Subtes Perlu Fokus</h4><ul>{il}</ul></div>',unsafe_allow_html=True)
        with cp2:
            ik="".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} ✅</li>" for k,v in kuat2)
            st.markdown(f'<div class="al al-s"><h4>🟢 Kekuatan Akademik</h4><ul>{ik}</ul></div>',unsafe_allow_html=True)
        st.markdown('<div class="sec">📋 Rencana Aksi</div>', unsafe_allow_html=True)
        if r["kat"]=="Sangat Aman":
            st.markdown("""<div class="al al-s"><h4>🏆 Maintenance Mode</h4><ul>
              <li>Tryout 1–2x/minggu menjaga ketajaman</li>
              <li>Review kesalahan kecil yang masih berulang</li>
              <li>Fokus manajemen waktu & kondisi mental</li>
              <li>Jaga pola tidur 7–8 jam/malam</li></ul></div>""",unsafe_allow_html=True)
        elif r["kat"]=="Aman":
            st.markdown(f"""<div class="al al-i"><h4>✅ Penguatan & Konsistensi</h4><ul>
              <li>Target +{mx-r['sw']:.0f} poin untuk zona Sangat Aman</li>
              <li>60% waktu pada {SUBTES_FULL[ss[0][0]]} (terlemah)</li>
              <li>Tryout min. 2x/bulan + review mendalam</li>
              <li>Simulasi 150 soal dalam 2.5 jam/sesi</li></ul></div>""",unsafe_allow_html=True)
        elif r["kat"]=="Berisiko":
            st.markdown(f"""<div class="al al-w"><h4>⚡ Intensifikasi Bertarget</h4><ul>
              <li>Target +{mn-r['sw']:.0f} poin untuk zona Aman</li>
              <li>Belajar 3–4 jam/hari terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Fokus subtes berbobot tinggi untuk prodimu</li></ul></div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-d"><h4>🔴 Intensifikasi Penuh</h4><ul>
              <li>Target +{abs(r['gap']):.0f} poin — bertahap setiap bulan</li>
              <li>Belajar 4–5 jam/hari terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Konsultasi tutor untuk subtes berbobot tinggi</li>
              <li>Pertimbangkan prodi/PTN yang lebih sesuai</li></ul></div>""",unsafe_allow_html=True)

    with t6:
        st.markdown('<div class="sec">📅 Proyeksi Skor 8 Minggu</div>', unsafe_allow_html=True)
        ch_progress(r, key="r_prog_t5")
        st.markdown('<div class="sec">📋 Detail Rencana Per Minggu</div>', unsafe_allow_html=True)
        rencana = buat_rencana_mingguan(r, 8)
        fase_clr = {"Fondasi":"#3b6cb7","Intensif":"#d4620a","Pemantapan":"#1a8a4a","Final":"#c8890a"}
        for m in rencana:
            clr = fase_clr.get(m["fase"],"#7048c8")
            tasks_html = "".join(f'<div style="padding:.1rem 0;color:#3a4a65">• {t}</div>' for t in m["tasks"])
            st.markdown(f"""<div class="week-card">
              <div class="week-num" style="color:{clr}">MINGGU {m['minggu']} — {m['fase'].upper()}</div>
              <div class="week-target">🎯 Target: <strong style="color:{clr}">{m['target_skor']}</strong> &nbsp;|&nbsp; ⏰ {m['jam']}</div>
              <div class="week-tasks">{tasks_html}</div>
            </div>""", unsafe_allow_html=True)

    with t7:
        st.markdown('<div class="sec">📄 Export Laporan ke PDF</div>', unsafe_allow_html=True)
        st.markdown("""<div class="al al-i"><h4>📋 Laporan PDF Mencakup:</h4><ul>
          <li>Profil siswa & target kampus/prodi</li>
          <li>Skor tertimbang (dibulatkan) & status kategori kesiapan</li>
          <li>Tabel bobot & kontribusi per subtes</li>
          <li>Indikator psikologis & konsistensi belajar</li>
          <li><strong>Rekomendasi prodi alternatif</strong> di kampus yang sama & prodi serupa di kampus lain</li>
          <li>Rencana belajar 8 minggu personal (Fondasi → Intensif → Pemantapan → Final)</li>
        </ul></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="al al-s"><h4>Cara Menyimpan sebagai PDF</h4><ol>
          <li>Klik tombol <strong>Generate & Download Laporan HTML</strong></li>
          <li>Buka file HTML di browser</li>
          <li>Tekan <strong>Ctrl+P</strong> (Win) atau <strong>Cmd+P</strong> (Mac)</li>
          <li>Pilih <strong>"Save as PDF"</strong> → klik Save</li>
        </ol></div>""", unsafe_allow_html=True)
        if st.button("📄  Generate & Download Laporan HTML", type="primary"):
            html = generate_pdf(r)
            b64  = base64.b64encode(html.encode()).decode()
            fn   = f"skoolnow_ai_{r.get('nama','').replace(' ','_')}.html"
            st.markdown(f"""<a href="data:text/html;base64,{b64}" download="{fn}"
              style="display:inline-block;background:linear-gradient(135deg,#3b6cb7,#2a4a8c);
                     color:#ffffff;font-weight:700;padding:.6rem 1.4rem;border-radius:8px;
                     text-decoration:none;font-size:.9rem;margin-top:.5rem">
              ⬇️ Download {fn}</a>""", unsafe_allow_html=True)
        pp1,pp2 = st.columns(2)
        with pp1:
            st.dataframe(pd.DataFrame([
                {"Info":"Nama","Detail":r.get("nama","—")},
                {"Info":"Jenjang","Detail":r.get("jenjang","—")},
                {"Info":"Program Studi","Detail":r["prodi"]},
                {"Info":"Kampus","Detail":r["kampus"]},
                {"Info":"Skor Tertimbang","Detail":f"{round(r['sw'])} / 1000"},
                {"Info":"Gap vs Minimum","Detail":f"{r['gap']:+.0f}"},
            ]), use_container_width=True, hide_index=True)
        with pp2:
            st.dataframe(pd.DataFrame([
                {"Indikator":"Kategori Skor","Nilai":f"{r['kat_icon']} {r['kat']}"},
                {"Indikator":"Peluang Lolos","Nilai":f"{r['ppct']:.0f}%"},
                {"Indikator":"Kesiapan Mental","Nilai":f"{r['psiko']:.0f}/100"},
                {"Indikator":"Konsistensi","Nilai":f"{r['konsist']:.0f}/100"},
                {"Indikator":"Stabilitas","Nilai":f"{r['stab']:.0f}/100"},
                {"Indikator":"Risiko Underperform","Nilai":f"{r['risk'][0]} {r['risk'][1]}"},
            ]), use_container_width=True, hide_index=True)

    st.divider()
    nb1,nb2,_ = st.columns([1,1,4])
    with nb1:
        if st.button("◀ Ubah Data"): st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with nb2:
        if st.button("🏠 Beranda"): st.session_state.page="home"; st.rerun()

    st.markdown(f"""<div style="text-align:center;padding:1.4rem;background:var(--surf);
      border-radius:var(--r);border:1px solid var(--border);margin-top:.8rem">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:800;color:#1a2540">
        💪 {nama}, kamu pasti bisa!
      </div>
      <div style="color:#6a7a95;font-size:.82rem;margin-top:.3rem">
        Konsistensi + strategi tepat = PTN impianmu pasti bisa diraih 🚀
      </div>
      <div style="color:#b0b8c8;font-size:.7rem;margin-top:.3rem">
        🎯 Skoolnow AI v5.0 — AI UTBK Intelligence · Data xlsx SNPMB 2022–2024 · S1/D4/D3 · 4 Kategori Skor
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    render_nav()
    {"home":page_home, "survey":page_survey, "result":page_result}[st.session_state.page]()

if __name__ == "__main__":
    main()
