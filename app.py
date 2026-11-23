import streamlit as st
import pandas as pd
import numpy as np
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

/* Bütün düymələr (Sol panel və əsas ekran) - heç vaxt ağ qalmasın */
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

/* Input və Select sahələri */
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
    background: #0a140e;
    border-top: 1px solid rgba(57, 255, 20, 0.45);
    border-radius: 10px;
    padding: 14px;
    margin-top: 24px;
    text-align: center;
    color: #39ff14 !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

REGIONS = {
    "Oğuz": {
        "lat": 41.0714, "lon": 47.4653, "zone": "Şimal-Qərb dağətəyi zona (Xalxal / Baş Daşağıl istiqaməti)",
        "ph": 6.2, "n": 48, "ndvi": 0.74, "moisture": 35,
        "prev_ph": 6.0, "prev_yield": 4.2, "curr_yield": 4.8
    },
    "Şəki": {
        "lat": 41.1919, "lon": 47.1706, "zone": "Şəki düzənliyi və dağətəyi aqro-monitorinq zonası",
        "ph": 6.5, "n": 52, "ndvi": 0.71, "moisture": 32,
        "prev_ph": 6.4, "prev_yield": 4.0, "curr_yield": 4.5
    },
    "Qəbələ": {
        "lat": 40.9814, "lon": 47.8458, "zone": "Yüksək rütubətli meyvə-tərəvəz monitorinq zonası",
        "ph": 6.1, "n": 55, "ndvi": 0.78, "moisture": 39,
        "prev_ph": 5.9, "prev_yield": 4.6, "curr_yield": 5.1
    },
    "Sabirabad": {
        "lat": 40.0087, "lon": 48.4770, "zone": "Muğan-Mil düzü suvarma və duzluluq nəzarət zonası",
        "ph": 7.6, "n": 34, "ndvi": 0.56, "moisture": 22,
        "prev_ph": 7.8, "prev_yield": 3.1, "curr_yield": 3.4
    },
    "Gəncə-Göygöl": {
        "lat": 40.5855, "lon": 46.3189, "zone": "Gəncə-Qazax əkinçilik və rütubət nəzarət zonası",
        "ph": 6.8, "n": 45, "ndvi": 0.68, "moisture": 30,
        "prev_ph": 6.7, "prev_yield": 3.9, "curr_yield": 4.3
    },
    "Lənkəran": {
        "lat": 38.7543, "lon": 48.8506, "zone": "Lənkəran subtropik və tərəvəzçilik zonası",
        "ph": 5.8, "n": 60, "ndvi": 0.81, "moisture": 44,
        "prev_ph": 5.7, "prev_yield": 4.9, "curr_yield": 5.4
    },
}

CROPS = {
    "Pomidor": {
        "opt_ph": (6.0, 6.8), "cost_ha": 2400, "rev_ha": 5200, "conf": 91.4,
        "history": [28, 30, 29, 32, 34, 33, 36, 38, 37, 41],
        "advice": "Bu il Pomidor əkini məsləhətdir — torpaq pH və rütubət balansı əlverişlidir.",
        "steps": [
            "1. Damcı suvarma ilə rütubəti 35–40% aralığında saxlayın (+14% məhsul).",
            "2. Çiçəkləmə dövründə Kalium-fosfat gübrəsi tətbiq edin (+9% məhsul).",
            "3. Peyk xəritəsində zəif görünən zonalara lokal azot verin (+6% qənaət)."
        ]
    },
    "Pambıq": {
        "opt_ph": (6.5, 7.8), "cost_ha": 1650, "rev_ha": 3450, "conf": 87.8,
        "history": [2.4, 2.5, 2.7, 2.6, 2.9, 3.1, 3.0, 3.3, 3.4, 3.6],
        "advice": "İsti və balanslı sahələrdə bu il Pambıq əkini məsləhətdir.",
        "steps": [
            "1. Səpinqabağı duzluluğu nəzarətdə saxlayın.",
            "2. Qönçələmə fazasında azot gübrəsini iki hissəyə bölün (+12% məhsul).",
            "3. Yığım zamanı məhsul itkisini minimuma endirin."
        ]
    },
    "Turp": {
        "opt_ph": (5.8, 6.8), "cost_ha": 950, "rev_ha": 2350, "conf": 93.2,
        "history": [16, 17, 16.5, 18, 19, 18.5, 20, 21, 21.5, 23],
        "advice": "Qısa müddətdə stabil dövriyyə üçün bu il Turp əkini məsləhətdir.",
        "steps": [
            "1. Yumşaq və daşsız torpaq hazırlayın.",
            "2. Həddindən artıq azotdan çəkinin.",
            "3. Müntəzəm səhər suvarması ilə keyfiyyəti artırın (+15% gəlir)."
        ]
    },
    "Buğda": {
        "opt_ph": (6.0, 7.5), "cost_ha": 780, "rev_ha": 1680, "conf": 89.5,
        "history": [3.1, 3.2, 3.0, 3.4, 3.5, 3.3, 3.7, 3.8, 3.9, 4.2],
        "advice": "Geniş sahələrdə sabit və etibarlı nəticə üçün bu il Buğda əkini məsləhətdir.",
        "steps": [
            "1. Kollanma dövründə rütubətə uyğun azot verin.",
            "2. Alaq otlarına qarşı erkən mübarizə aparın (+11% məhsul).",
            "3. Dən dolma fazasında mikroelement çiləməsi edin."
        ]
    },
    "Kartof": {
        "opt_ph": (5.5, 6.5), "cost_ha": 2700, "rev_ha": 5800, "conf": 90.1,
        "history": [19, 20, 21, 20.5, 22, 23, 24, 23.5, 25, 27],
        "advice": "Zəif turşulu və mülayim torpaqlarda bu il Kartof əkini məsləhətdir.",
        "steps": [
            "1. Keyfiyyətli toxumluq yumrulardan istifadə edin.",
            "2. Dibdoldurma işini vaxtında görün (+13% məhsul).",
            "3. Kalium gübrəsi ilə saxlanma müddətini artırın."
        ]
    },
    "Qarğıdalı": {
        "opt_ph": (5.8, 7.0), "cost_ha": 1350, "rev_ha": 3100, "conf": 88.6,
        "history": [5.8, 6.0, 6.2, 6.1, 6.5, 6.8, 6.7, 7.1, 7.3, 7.6],
        "advice": "Suvarma imkanı olan sahələrdə bu il Qarğıdalı əkini məsləhətdir.",
        "steps": [
            "1. 6–8 yarpaq mərhələsində cərgəarası becərmə edin.",
            "2. Saçaqlama dövründə su stresinə yol verməyin.",
            "3. Bitki sıxlığını optimal saxlayın."
        ]
    }
}

        "opt_ph": (6.0, 6.8), "cost_ha": 2400, "rev_ha": 5200, "conf": 91.4,
        "history": [28, 30, 29, 32, 34, 33, 36, 38, 37, 41],
        "advice": "Bu il Pomidor əkini məsləhətdir — torpaq pH və rütubət balansı əlverişlidir.",
        "steps": 
        "1. Damcı suvarma ilə rütubəti 35–40% aralığında saxlayın (+14% məhsul).",

