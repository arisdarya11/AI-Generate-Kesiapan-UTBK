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

    wb_s1, err = load_file(LOCAL_S1, URL_S1)
    if wb_s1 is None:
        return None, None, None, None, f"Gagal load S1: {err}"
    wb_d34, err = load_file(LOCAL_D34, URL_D34)
    if wb_d34 is None:
        return None, None, None, None, f"Gagal load D3/D4: {err}"

    df_s1 = wb_s1.get("DATA UTBK SNBT ESTIMASI", pd.DataFrame())
    df_s1 = df_s1[df_s1.iloc[:,0].apply(
        lambda x: str(x).isdigit() if pd.notna(x) else False)].copy()
    df_s1.columns = ['No','Prodi','Kelompok','PTN','Rank','NilaiAman','Rentang','Catatan']
    df_s1 = df_s1.dropna(subset=['Prodi','PTN','NilaiAman'])

    ptn_s1 = {}
    for _, row in df_s1.iterrows():
        ptn = str(row['PTN']).strip()
        prodi = str(row['Prodi']).strip()
        mn, mx = parse_rentang(row['Rentang'])
        if mn is None:
            try:
                na = int(float(row['NilaiAman']))
                mn, mx = na - 15, na + 15
            except:
                continue
        if ptn not in ptn_s1:
            ptn_s1[ptn] = {}
        ptn_s1[ptn][prodi] = {'mn': mn, 'mx': mx}

    df_d34 = wb_d34.get("DATA D3 D4 ESTIMASI", pd.DataFrame())
    df_d34 = df_d34[df_d34.iloc[:,0].apply(
        lambda x: str(x).isdigit() if pd.notna(x) else False)].copy()
    df_d34.columns = ['No','Prodi','Jenjang','Kelompok','PTN','Rank','NilaiAman','Rentang','Catatan']
    df_d34 = df_d34[(df_d34['NilaiAman'] != '—') & (df_d34['NilaiAman'].notna())]

    ptn_d3 = {}
    ptn_d4 = {}
    for _, row in df_d34.iterrows():
        ptn = str(row['PTN']).strip()
        prodi = str(row['Prodi']).strip()
        jenjang = str(row['Jenjang']).strip()
        mn, mx = parse_rentang(row['Rentang'])
        if mn is None:
            try:
                na = int(float(row['NilaiAman']))
                mn, mx = na - 15, na + 15
            except:
                continue
        d = ptn_d3 if jenjang == 'D3' else ptn_d4
        if ptn not in d:
            d[ptn] = {}
        d[ptn][prodi] = {'mn': mn, 'mx': mx}

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
<title>Laporan SKORIA — {nama}</title>
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
  <div class="brand">🎯 SKORIA</div>
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
<div class="footer">🎯 SKORIA — AI UTBK Intelligence · Data SNPMB/BPPP Kemdikbud 2025/2026 · Skor skala 200–1000</div>
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
      <div class="topbar-brand">🎯 SKORIA <span class="topbar-tag">AI UTBK Intelligence · S1 · D4 · D3 · 2025/2026</span></div>
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
        <span class="ticker-item">🎯 SKORIA v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1</span> · <span>D4</span> · <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Data Estimasi Historis 2022–2024</span>
        <span class="ticker-item">📚 <span>60+</span> Prodi S1 · <span>D3/D4</span> dari database xlsx</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📊 4 Kategori Skor: <span>Tidak Aman</span> · <span>Berisiko</span> · <span>Aman</span> · <span>Sangat Aman</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
        <span class="ticker-item">🎯 SKORIA v5.0 — AI UTBK Intelligence</span>
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
      <h1>SKORIA — Analisis Kesiapan<br><span>UTBK</span> Berbasis AI</h1>
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
         "Jika peluang masih kurang, SKORIA menampilkan prodi lain di kampus yang sama dan prodi serupa di kampus berbeda yang lebih sesuai skormu."),
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
        f'<div class="fitur-panel-title">&#128269; Apa Saja yang Bisa Kamu Dapatkan dari SKORIA AI?</div>'
        f'<div class="fitur-grid-3">{items_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Legenda 4 kategori
    st.markdown("""<div style="background:#fff;border:1px solid #e0e8f4;border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.2rem;box-shadow:0 2px 12px rgba(30,60,140,.08)">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:.9rem;font-weight:700;color:#12203f;margin-bottom:.7rem">📊 4 Kategori Rentang Skor SKORIA</div>
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
        if st.button("🎯  Lihat Hasil Analisis SKORIA", type="primary"):
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
      <p>Hasil analisis <strong style="color:#ffd166">SKORIA AI</strong> berdasarkan skor TPS, psikologis, dan kebiasaan belajarmu</p>
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
          <h4>🤖 Rekomendasi Strategi SKORIA AI — {det.get('icon','')} {h['strategi']}
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
            fn   = f"skoria_{r.get('nama','').replace(' ','_')}.html"
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
        🎯 SKORIA v5.0 — AI UTBK Intelligence · Data xlsx SNPMB 2022–2024 · S1/D4/D3 · 4 Kategori Skor
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
