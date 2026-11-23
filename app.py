import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(
    page_title="C.h.e.MartixAZE | Cyber-Agro AI Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
    --bg-dark: #050806;
    --card-bg: #0c1610;
    --neon-green: #39ff14;
    --neon-cyan: #00d4ff;
    --border-glow: rgba(57, 255, 20, 0.45);
    --text-main: #f2fbf4;
    --text-muted: #b7d1bd;
}

.stApp, [data-testid="stAppViewContainer"], .main {
    background-color: #050806 !important;
    color: #f2fbf4 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

p, span, label, div, li, caption {
    color: #f2fbf4;
}

h1, h2, h3, h4 {
    font-family: 'Rajdhani', sans-serif !important;
    color: #39ff14 !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

.brand-nowrap {
    white-space: nowrap !important;
    display: inline-block;
}

[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background: #070f0a !important;
    border-right: 1px solid rgba(57, 255, 20, 0.4) !important;
}

.cyber-card {
    background: #0c1610 !important;
    border: 1px solid rgba(57, 255, 20, 0.45) !important;
    border-left: 5px solid #39ff14 !important;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}

.badge-neon {
    display: inline-block;
    background: rgba(57, 255, 20, 0.16);
    color: #39ff14 !important;
    border: 1px solid #39ff14;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #39ff14 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #b7d1bd !important;
}

button[kind="secondary"], button[kind="primary"], .stButton > button, div.stButton > button {
    background: linear-gradient(90deg, #003b73, #0077b6) !important;
    color: #ffffff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 42px !important;
    padding: 8px 12px !important;
    line-height: 1.25 !important;
}

button[kind="secondary"] *, button[kind="primary"] *, .stButton > button *, div.stButton > button * {
    color: #ffffff !important;
}

button[kind="secondary"]:hover, button[kind="primary"]:hover, .stButton > button:hover, div.stButton > button:hover {
    background: #0e2a1a !important;
    color: #39ff14 !important;
    border-color: #39ff14 !important;
}

button[kind="secondary"]:hover *, button[kind="primary"]:hover *, .stButton > button:hover *, div.stButton > button:hover * {
    color: #39ff14 !important;
}

.stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
    background-color: #0e1d14 !important;
    color: #ffffff !important;
    border: 1px solid #39ff14 !important;
    border-radius: 8px !important;
}

.nino-box {
    background: #08160e !important;
    border: 1.5px solid #39ff14 !important;
    border-radius: 12px;
    padding: 14px;
    margin-top: 10px;
    color: #f2fbf4 !important;
}

.footer-box {
