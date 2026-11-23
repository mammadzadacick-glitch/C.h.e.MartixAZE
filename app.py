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
    "Abşeron": {
        "lat": 40.4614, "lon": 49.7364, "zone": "Abşeron yarımadası və zeytun/badam-tərəvəz monitorinq zonası",
        "ph": 7.7, "n": 32, "ndvi": 0.48, "moisture": 19,
        "prev_ph": 7.8, "prev_yield": 2.6, "curr_yield": 2.9
    },
    "Ağcabədi": {
        "lat": 40.0500, "lon": 47.4500, "zone": "Mil düzü pambıq, taxıl və yem bitkiləri zonası",
        "ph": 7.5, "n": 38, "ndvi": 0.61, "moisture": 24,
        "prev_ph": 7.6, "prev_yield": 3.4, "curr_yield": 3.7
    },
    "Ağdam": {
        "lat": 39.9911, "lon": 46.9297, "zone": "Qarabağ düzənliyi və dağətəyi əkinçilik zonası",
        "ph": 7.3, "n": 42, "ndvi": 0.64, "moisture": 27,
        "prev_ph": 7.3, "prev_yield": 3.6, "curr_yield": 3.9
    },
    "Ağdaş": {
        "lat": 40.6467, "lon": 47.4744, "zone": "Şirvan düzünün mərkəzi meyvə və taxıl zonası",
        "ph": 7.2, "n": 43, "ndvi": 0.66, "moisture": 28,
        "prev_ph": 7.2, "prev_yield": 3.7, "curr_yield": 4.0
    },
    "Ağstafa": {
        "lat": 41.1189, "lon": 45.4539, "zone": "Kür çayı vadisi və Qazax-Tovuz əkinçilik zonası",
        "ph": 7.1, "n": 44, "ndvi": 0.65, "moisture": 27,
        "prev_ph": 7.1, "prev_yield": 3.6, "curr_yield": 3.9
    },
    "Ağsu": {
        "lat": 40.5703, "lon": 48.3653, "zone": "Şirvan dağətəyi üzümçülük və taxıl zonası",
        "ph": 7.0, "n": 45, "ndvi": 0.67, "moisture": 29,
        "prev_ph": 7.0, "prev_yield": 3.8, "curr_yield": 4.1
    },
    "Astara": {
        "lat": 38.4558, "lon": 48.8750, "zone": "Cənub subtropik sitrus, çay və tərəvəz zonası",
        "ph": 5.7, "n": 62, "ndvi": 0.82, "moisture": 46,
        "prev_ph": 5.6, "prev_yield": 5.0, "curr_yield": 5.5
    },
    "Babək": {
        "lat": 39.1508, "lon": 45.4444, "zone": "Naxçıvan düzənliyi və dağətəyi aqro-monitorinq zonası",
        "ph": 7.4, "n": 39, "ndvi": 0.59, "moisture": 23,
        "prev_ph": 7.4, "prev_yield": 3.3, "curr_yield": 3.6
    },
    "Balakən": {
        "lat": 41.7256, "lon": 46.4044, "zone": "Şimal-Qərb yüksək rütubətli fındıq və tərəvəz zonası",
        "ph": 6.2, "n": 54, "ndvi": 0.77, "moisture": 38,
        "prev_ph": 6.1, "prev_yield": 4.4, "curr_yield": 4.9
    },
    "Bərdə": {
        "lat": 40.3758, "lon": 47.1267, "zone": "Mərkəzi Aran pambıq və taxılçılıq zonası",
        "ph": 7.4, "n": 40, "ndvi": 0.63, "moisture": 26,
        "prev_ph": 7.5, "prev_yield": 3.5, "curr_yield": 3.8
    },
    "Beyləqan": {
        "lat": 39.7756, "lon": 47.6186, "zone": "Mil düzü pambıq, yonca və taxıl zonası",
        "ph": 7.6, "n": 36, "ndvi": 0.58, "moisture": 23,
        "prev_ph": 7.7, "prev_yield": 3.2, "curr_yield": 3.5
    },
    "Biləsuvar": {
        "lat": 39.4589, "lon": 48.5450, "zone": "Muğan düzü pambıq və taxıl monitorinq zonası",
        "ph": 7.7, "n": 35, "ndvi": 0.55, "moisture": 21,
        "prev_ph": 7.8, "prev_yield": 3.1, "curr_yield": 3.4
    },
    "Cəbrayıl": {
        "lat": 39.3989, "lon": 47.0244, "zone": "Cənub-Qərb dağətəyi və düzənlik əkinçilik zonası",
        "ph": 7.2, "n": 41, "ndvi": 0.62, "moisture": 25,
        "prev_ph": 7.2, "prev_yield": 3.4, "curr_yield": 3.7
    },
    "Cəlilabad": {
        "lat": 39.2097, "lon": 48.5100, "zone": "Lənkəran-Muğan keçid kartof və taxıl zonası",
        "ph": 6.9, "n": 46, "ndvi": 0.69, "moisture": 30,
        "prev_ph": 6.8, "prev_yield": 4.0, "curr_yield": 4.4
    },
    "Culfa": {
        "lat": 38.9556, "lon": 45.6297, "zone": "Arazboyu və dağətəyi meyvə-tərəvəz zonası",
        "ph": 7.4, "n": 37, "ndvi": 0.54, "moisture": 22,
        "prev_ph": 7.5, "prev_yield": 3.1, "curr_yield": 3.4
    },
    "Daşkəsən": {
        "lat": 40.5203, "lon": 46.0819, "zone": "Kiçik Qafqaz yüksək dağlıq otlaq və kartof zonası",
        "ph": 5.9, "n": 51, "ndvi": 0.73, "moisture": 37,
        "prev_ph": 5.8, "prev_yield": 3.8, "curr_yield": 4.2
    },
    "Füzuli": {
        "lat": 39.6008, "lon": 47.1431, "zone": "Qarabağın cənub-şərq düzənlik və üzüm-taxıl zonası",
        "ph": 7.3, "n": 41, "ndvi": 0.62, "moisture": 25,
        "prev_ph": 7.4, "prev_yield": 3.4, "curr_yield": 3.7
    },
    "Gədəbəy": {
        "lat": 40.5683, "lon": 45.8169, "zone": "Yüksək dağlıq kartof və otlaq monitorinq zonası",
        "ph": 5.8, "n": 53, "ndvi": 0.74, "moisture": 36,
        "prev_ph": 5.7, "prev_yield": 3.9, "curr_yield": 4.3
    },
    "Goranboy": {
        "lat": 40.6103, "lon": 46.7897, "zone": "Gəncə-Qazax düzənliyi və dağətəyi əkinçilik zonası",
        "ph": 7.1, "n": 44, "ndvi": 0.66, "moisture": 28,
        "prev_ph": 7.1, "prev_yield": 3.8, "curr_yield": 4.1
    },
    "Göyçay": {
        "lat": 40.6236, "lon": 47.7400, "zone": "Şirvan düzü nar və bağçılıq monitorinq zonası",
        "ph": 7.0, "n": 47, "ndvi": 0.70, "moisture": 30,
        "prev_ph": 7.0, "prev_yield": 4.1, "curr_yield": 4.5
    },
    "Göygöl": {
        "lat": 40.5858, "lon": 46.3189, "zone": "Dağətəyi üzüm, meyvə və tərəvəz zonası",
        "ph": 6.7, "n": 48, "ndvi": 0.72, "moisture": 32,
        "prev_ph": 6.6, "prev_yield": 4.1, "curr_yield": 4.5
    },
    "Hacıqabul": {
        "lat": 40.0389, "lon": 48.9414, "zone": "Şirvan-Muğan quraq-mülayim əkinçilik zonası",
        "ph": 7.7, "n": 33, "ndvi": 0.52, "moisture": 20,
        "prev_ph": 7.8, "prev_yield": 2.9, "curr_yield": 3.2
    },
    "Xaçmaz": {
        "lat": 41.4592, "lon": 48.8022, "zone": "Şimal-Şərq tərəvəz, bağçılıq və yaşıl örtük zonası",
        "ph": 6.6, "n": 53, "ndvi": 0.77, "moisture": 36,
        "prev_ph": 6.5, "prev_yield": 4.5, "curr_yield": 5.0
    },
    "Xızı": {
        "lat": 40.9108, "lon": 49.0728, "zone": "Böyük Qafqazın cənub-şərq yamac monitorinq zonası",
        "ph": 7.2, "n": 38, "ndvi": 0.57, "moisture": 24,
        "prev_ph": 7.2, "prev_yield": 3.2, "curr_yield": 3.5
    },
    "Xocalı": {
        "lat": 39.9131, "lon": 46.7903, "zone": "Qarabağ dağətəyi əkinçilik və meyvəçilik zonası",
        "ph": 6.8, "n": 46, "ndvi": 0.68, "moisture": 31,
        "prev_ph": 6.8, "prev_yield": 3.9, "curr_yield": 4.2
    },
    "Xocavənd": {
        "lat": 39.7917, "lon": 47.1103, "zone": "Qarabağ dağətəyi və düzənlik monitorinq zonası",
        "ph": 7.1, "n": 43, "ndvi": 0.65, "moisture": 27,
        "prev_ph": 7.1, "prev_yield": 3.6, "curr_yield": 3.9
    },
    "İmişli": {
        "lat": 39.8708, "lon": 48.0600, "zone": "Mil-Muğan pambıq, şəkər çuğunduru və taxıl zonası",
        "ph": 7.6, "n": 37, "ndvi": 0.59, "moisture": 23,
        "prev_ph": 7.7, "prev_yield": 3.3, "curr_yield": 3.6
    },
    "İsmayıllı": {
        "lat": 40.7850, "lon": 48.1519, "zone": "Böyük Qafqaz cənub yamacı bağ və taxıl zonası",
        "ph": 6.4, "n": 50, "ndvi": 0.74, "moisture": 34,
        "prev_ph": 6.3, "prev_yield": 4.2, "curr_yield": 4.6
    },
    "Kəlbəcər": {
        "lat": 40.1025, "lon": 46.0364, "zone": "Yüksək dağlıq yaylaq, otlaq və aqro-ekoloji zona",
        "ph": 5.9, "n": 52, "ndvi": 0.72, "moisture": 36,
        "prev_ph": 5.8, "prev_yield": 3.7, "curr_yield": 4.1
    },
    "Kəngərli": {
        "lat": 39.3875, "lon": 45.1636, "zone": "Naxçıvan Arazboyu tərəvəz və bostan zonası",
        "ph": 7.4, "n": 40, "ndvi": 0.60, "moisture": 24,
        "prev_ph": 7.4, "prev_yield": 3.4, "curr_yield": 3.7
    },
    "Kürdəmir": {
        "lat": 40.3425, "lon": 48.1561, "zone": "Şirvan düzü üzüm, taxıl və pambıq zonası",
        "ph": 7.5, "n": 37, "ndvi": 0.57, "moisture": 22,
        "prev_ph": 7.6, "prev_yield": 3.2, "curr_yield": 3.5
    },
    "Laçın": {
        "lat": 39.6383, "lon": 46.5461, "zone": "Kiçik Qafqaz dağətəyi və yaylaq monitorinq zonası",
        "ph": 6.1, "n": 49, "ndvi": 0.70, "moisture": 33,
        "prev_ph": 6.0, "prev_yield": 3.7, "curr_yield": 4.0
    },
    "Lerik": {
        "lat": 38.7736, "lon": 48.4150, "zone": "Talış dağları kartof, paxlalı və dağətəyi zona",
        "ph": 6.0, "n": 50, "ndvi": 0.73, "moisture": 35,
        "prev_ph": 5.9, "prev_yield": 3.9, "curr_yield": 4.3
    },
    "Lənkəran": {
        "lat": 38.7543, "lon": 48.8506, "zone": "Lənkəran subtropik və tərəvəzçilik zonası",
        "ph": 5.8, "n": 60, "ndvi": 0.81, "moisture": 44,
        "prev_ph": 5.7, "prev_yield": 4.9, "curr_yield": 5.4
    },
    "Masallı": {
        "lat": 39.0342, "lon": 48.6656, "zone": "Cənub düzənliyi və dağətəyi tərəvəz-çəltik zonası",
        "ph": 6.1, "n": 56, "ndvi": 0.78, "moisture": 40,
        "prev_ph": 6.0, "prev_yield": 4.6, "curr_yield": 5.1
    },
    "Neftçala": {
        "lat": 39.3589, "lon": 49.2469, "zone": "Kür-Araz mənsəbi və Xəzərsahili əkinçilik zonası",
        "ph": 7.8, "n": 33, "ndvi": 0.51, "moisture": 21,
        "prev_ph": 7.9, "prev_yield": 2.8, "curr_yield": 3.1
    },
    "Oğuz": {
        "lat": 41.0714, "lon": 47.4653, "zone": "Şimal-Qərb dağətəyi zona (Xalxal / Baş Daşağıl istiqaməti)",
        "ph": 6.2, "n": 48, "ndvi": 0.74, "moisture": 35,
        "prev_ph": 6.0, "prev_yield": 4.2, "curr_yield": 4.8
    },
    "Ordubad": {
        "lat": 38.9036, "lon": 46.0231, "zone": "Naxçıvanın cənub-şərq bağçılıq və subtropik zonası",
        "ph": 7.2, "n": 44, "ndvi": 0.64, "moisture": 27,
        "prev_ph": 7.2, "prev_yield": 3.7, "curr_yield": 4.0
    },
    "Qax": {
        "lat": 41.4183, "lon": 46.9206, "zone": "Şimal-Qərb fındıq, tütün və tərəvəz monitorinq zonası",
        "ph": 6.3, "n": 52, "ndvi": 0.76, "moisture": 36,
        "prev_ph": 6.2, "prev_yield": 4.3, "curr_yield": 4.8
    },
    "Qazax": {
        "lat": 41.0925, "lon": 45.3656, "zone": "Qazax-Tovuz düzənliyi və dağətəyi əkinçilik zonası",
        "ph": 7.1, "n": 45, "ndvi": 0.67, "moisture": 28,
        "prev_ph": 7.1, "prev_yield": 3.8, "curr_yield": 4.1
    },
    "Qəbələ": {
        "lat": 40.9814, "lon": 47.8458, "zone": "Yüksək rütubətli meyvə-tərəvəz monitorinq zonası",
        "ph": 6.1, "n": 55, "ndvi": 0.78, "moisture": 39,
        "prev_ph": 5.9, "prev_yield": 4.6, "curr_yield": 5.1
    },
    "Qobustan": {
        "lat": 40.5317, "lon": 48.9289, "zone": "Şamaxı-Qobustan taxıl və dəmyə əkinçilik zonası",
        "ph": 7.4, "n": 36, "ndvi": 0.54, "moisture": 22,
        "prev_ph": 7.5, "prev_yield": 3.0, "curr_yield": 3.3
    },
    "Quba": {
        "lat": 41.3611, "lon": 48.5131, "zone": "Şimal meyvəçilik və dağətəyi monitorinq zonası",
        "ph": 6.4, "n": 50, "ndvi": 0.75, "moisture": 34,
        "prev_ph": 6.3, "prev_yield": 4.3, "curr_yield": 4.7
    },
    "Qubadlı": {
        "lat": 39.3442, "lon": 46.5819, "zone": "Həkəri çayı vadisi və dağətəyi əkinçilik zonası",
        "ph": 6.9, "n": 44, "ndvi": 0.66, "moisture": 29,
        "prev_ph": 6.9, "prev_yield": 3.7, "curr_yield": 4.0
    },
    "Qusar": {
        "lat": 41.4275, "lon": 48.4361, "zone": "Şahdağ ətəyi meyvə, kartof və tərəvəz zonası",
        "ph": 6.3, "n": 51, "ndvi": 0.75, "moisture": 35,
        "prev_ph": 6.2, "prev_yield": 4.2, "curr_yield": 4.6
    },
    "Saatlı": {
        "lat": 39.9317, "lon": 48.3689, "zone": "Muğan düzü pambıq, bostan və taxıl zonası",
        "ph": 7.6, "n": 36, "ndvi": 0.57, "moisture": 22,
        "prev_ph": 7.7, "prev_yield": 3.2, "curr_yield": 3.5
    },
    "Sabirabad": {
        "lat": 40.0087, "lon": 48.4770, "zone": "Muğan-Mil düzü suvarma və duzluluq nəzarət zonası",
        "ph": 7.6, "n": 34, "ndvi": 0.56, "moisture": 22,
        "prev_ph": 7.8, "prev_yield": 3.1, "curr_yield": 3.4
    },
    "Salyan": {
        "lat": 39.5961, "lon": 48.9847, "zone": "Cənub-Şərq Muğan əkinçilik və suvarma zonası",
        "ph": 7.7, "n": 34, "ndvi": 0.54, "moisture": 21,
        "prev_ph": 7.8, "prev_yield": 3.0, "curr_yield": 3.3
    },
    "Samux": {
        "lat": 40.7611, "lon": 46.4056, "zone": "Kürboyu bağçılıq və taxıl monitorinq zonası",
        "ph": 7.2, "n": 43, "ndvi": 0.65, "moisture": 27,
        "prev_ph": 7.2, "prev_yield": 3.7, "curr_yield": 4.0
    },
    "Siyəzən": {
        "lat": 41.0783, "lon": 49.1114, "zone": "Şimal-Şərq sahil və dağətəyi monitorinq zonası",
        "ph": 7.3, "n": 39, "ndvi": 0.58, "moisture": 24,
        "prev_ph": 7.3, "prev_yield": 3.3, "curr_yield": 3.6
    },
    "Şabran": {
        "lat": 41.2000, "lon": 48.8833, "zone": "Şimal-Şərq tərəvəz və taxıl monitorinq zonası",
        "ph": 7.0, "n": 45, "ndvi": 0.66, "moisture": 28,
        "prev_ph": 7.0, "prev_yield": 3.8, "curr_yield": 4.1
    },
    "Şamaxı": {
        "lat": 40.6314, "lon": 48.6414, "zone": "Dağlıq Şirvan üzüm, taxıl və meyvə zonası",
        "ph": 7.1, "n": 44, "ndvi": 0.65, "moisture": 28,
        "prev_ph": 7.1, "prev_yield": 3.7, "curr_yield": 4.0
    },
    "Şəki": {
        "lat": 41.1919, "lon": 47.1706, "zone": "Şəki düzənliyi və dağətəyi aqro-monitorinq zonası",
        "ph": 6.5, "n": 52, "ndvi": 0.71, "moisture": 32,
        "prev_ph": 6.4, "prev_yield": 4.0, "curr_yield": 4.5
    },
    "Şəmkir": {
        "lat": 40.8297, "lon": 46.0189, "zone": "Qərb tərəvəzçilik və istixana-tarla zonası",
        "ph": 7.0, "n": 49, "ndvi": 0.72, "moisture": 31,
        "prev_ph": 6.9, "prev_yield": 4.1, "curr_yield": 4.5
    },
    "Şərur": {
        "lat": 39.5536, "lon": 44.9844, "zone": "Şərur düzü tütün, üzüm və tərəvəz zonası",
        "ph": 7.3, "n": 45, "ndvi": 0.66, "moisture": 28,
        "prev_ph": 7.3, "prev_yield": 3.8, "curr_yield": 4.1
    },
    "Şuşa": {
        "lat": 39.7600, "lon": 46.7464, "zone": "Qarabağ yüksək dağətəyi ekoloji və yaşıl zona",
        "ph": 6.4, "n": 48, "ndvi": 0.73, "moisture": 34,
        "prev_ph": 6.3, "prev_yield": 3.8, "curr_yield": 4.1
    },
    "Tərtər": {
        "lat": 40.3419, "lon": 46.9375, "zone": "Tərtər çayı vadisi və Qarabağ düzənliyi zonası",
        "ph": 7.2, "n": 44, "ndvi": 0.67, "moisture": 29,
        "prev_ph": 7.2, "prev_yield": 3.9, "curr_yield": 4.2
    },
    "Tovuz": {
        "lat": 40.9925, "lon": 45.6267, "zone": "Qərb kartof, üzüm və tərəvəz monitorinq zonası",
        "ph": 6.9, "n": 47, "ndvi": 0.70, "moisture": 30,
        "prev_ph": 6.8, "prev_yield": 4.0, "curr_yield": 4.4
    },
    "Ucar": {
        "lat": 40.5172, "lon": 47.6547, "zone": "Şirvan düzü pambıq, yonca və meyvə zonası",
        "ph": 7.5, "n": 38, "ndvi": 0.60, "moisture": 24,
        "prev_ph": 7.5, "prev_yield": 3.4, "curr_yield": 3.7
    },
    "Yardımlı": {
        "lat": 38.9061, "lon": 48.2411, "zone": "Talış dağətəyi və yüksək əkinçilik zonası",
        "ph": 6.1, "n": 47, "ndvi": 0.68, "moisture": 32,
        "prev_ph": 6.0, "prev_yield": 3.6, "curr_yield": 3.9
    },
    "Yevlax": {
        "lat": 40.6183, "lon": 47.1500, "zone": "Kür-Şirvan pambıq, taxıl və bostan zonası",
        "ph": 7.4, "n": 39, "ndvi": 0.62, "moisture": 25,
        "prev_ph": 7.5, "prev_yield": 3.5, "curr_yield": 3.8
    },
    "Zaqatala": {
        "lat": 41.6308, "lon": 46.6442, "zone": "Şimal-Qərb fındıq, qarğıdalı və tərəvəz zonası",
        "ph": 6.2, "n": 53, "ndvi": 0.76, "moisture": 37,
        "prev_ph": 6.1, "prev_yield": 4.4, "curr_yield": 4.9
    },
    "Zəngilan": {
        "lat": 39.0836, "lon": 46.6525, "zone": "Arazboyu və Həkəri qovşağı əkinçilik zonası",
        "ph": 7.2, "n": 42, "ndvi": 0.63, "moisture": 26,
        "prev_ph": 7.2, "prev_yield": 3.5, "curr_yield": 3.8
    },
    "Zərdab": {
        "lat": 40.2178, "lon": 47.7131, "zone": "Kür-Araz düzənliyi taxıl, yonca və pambıq zonası",
        "ph": 7.6, "n": 36, "ndvi": 0.58, "moisture": 23,
        "prev_ph": 7.7, "prev_yield": 3.2, "curr_yield": 3.5
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

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Bütün Bölmələr"

if "nino_history" not in st.session_state:
    st.session_state.nino_history = [
        ("Nino", "Salam! Mən Nino AI. Rayon, bitki və torpaq göstəricilərinə əsasən suallarını cavablandırıram. Şablon suallara basa və ya öz sualını aşağıda yaza bilərsən.")
    ]

with st.sidebar:
    st.markdown("## 🌱 <span class='brand-nowrap'>C.h.e.MartixAZE</span>", unsafe_allow_html=True)
    st.caption("NASA Peyk + Aqrokimya Sİ")

    search_txt = st.text_input("🔍 Bölmə axtar:", placeholder="pH, xəritə, bitki, gəlir, nino...")

    st.markdown("### 🟦 Sürətli Keçid Qutucuqları")
    blue_boxes = [
        "Bütün Bölmələr",
        "🎬 Bələdçi Bölməsi",
        "🧪 pH & Torpaq Qrafiki",
        "🛰️ NASA Peyk Xəritəsi",
        "📈 10 İllik Torpaq Məhsuldarlığı",
        "🌾 Bitki Seçimi & 10 İl",
        "💰 Gəlir, Xərc & Qazanc",
        "⚖️ Keçən İllə Müqayisə",
        "🤖 Nino AI Köməkçi"
    ]

    for box_name in blue_boxes:
        if not search_txt or search_txt.lower() in box_name.lower():
            if st.button(box_name, key=f"blue_btn_{box_name}"):
                st.session_state.selected_section = box_name

    st.divider()
    mode = st.radio("Məlumat Mənbəyi:", ["Rayon Seçimi", "Manual Daxiletmə"])
    selected_region = st.selectbox("Rayon:", list(REGIONS.keys()))
    reg = REGIONS[selected_region]

    if mode == "Manual Daxiletmə":
        ph_val = st.slider("Torpaq pH", 4.5, 9.0, float(reg["ph"]), 0.1)
        n_val = st.slider("Azot (mq/kq)", 10, 100, int(reg["n"]))
        ndvi_val = st.slider("NASA NDVI", 0.10, 0.95, float(reg["ndvi"]), 0.01)
        moist_val = st.slider("Rütubət (%)", 5, 80, int(reg["moisture"]))
    else:
        ph_val, n_val, ndvi_val, moist_val = reg["ph"], reg["n"], reg["ndvi"], reg["moisture"]

st.markdown(f"""
<div class="cyber-card">
    <span class="badge-neon">CYBER-AGRO AI PLATFORM</span>
    <h1 style="margin:6px 0 4px 0;"><span class="brand-nowrap">C.h.e.MartixAZE</span></h1>
    <p style="color:#b7d1bd; margin:0; font-size:14px;">
        Aktiv bölmə: <b style="color:#39ff14;">{st.session_state.selected_section}</b> | Rayon: <b style="color:#00d4ff;">{selected_region}</b>
    </p>
</div>
""", unsafe_allow_html=True)

sec = st.session_state.selected_section
all_mode = (sec == "Bütün Bölmələr")
years_10 = [str(y) for y in range(2017, 2027)]

if all_mode or sec == "🎬 Bələdçi Bölməsi":
    st.subheader("🎬 İstifadə Bələdçisi: Sayt Nə İşə Yarayır və Hara Nə Yazılır?")
    if os.path.exists("chemartix_guide.mp4"):
        st.video("chemartix_guide.mp4")
    else:
        st.markdown("""
        <div class="cyber-card">
            <p style="margin:0 0 8px 0;"><b>1. Hara nə daxil edilir?</b> Sol paneldən rayonu seçin (və ya Manual rejimdə pH, Azot, Rütubət daxil edin), aşağıda əkmək istədiyiniz bitkini və hektar sayını seçin.</p>
            <p style="margin:0 0 8px 0;"><b>2. Sayt nə işə yarayır?</b> Torpağın pH/Azot/NDVI göstəricilərini, 10 illik məhsuldarlıq dinamikasını, əkin tövsiyəsini, gəlir-xərc hesabını və keçən illə müqayisəni göstərir.</p>
            <p style="margin:0; color:#00d4ff;"><i>Öz yığdığın <code>chemartix_guide.mp4</code> faylını reponun əsas qovluğuna yükləyəndə video pleyer avtomatik burada görünəcək.</i></p>
        </div>
        """, unsafe_allow_html=True)

if all_mode or sec == "🧪 pH & Torpaq Qrafiki":
    st.markdown("---")
    st.subheader(f"🧪 {selected_region} — pH və Torpaq Kimyası Analizi")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Torpaq pH", f"{ph_val:.1f}", f"{ph_val - reg['prev_ph']:+.1f} keçən ilə görə")
    m2.metric("Azot (N)", f"{n_val} mq/kq", "Optimal" if n_val >= 40 else "Aşağı")
    m3.metric("NASA NDVI", f"{ndvi_val:.2f}", "Sağlam" if ndvi_val >= 0.65 else "Zəif")
    m4.metric("Rütubət", f"{moist_val}%", "Normal" if moist_val >= 28 else "Quru")

    ph_series = [round(ph_val - 0.3, 1), round(ph_val - 0.2, 1), round(ph_val - 0.1, 1), round(reg["prev_ph"], 1), round(ph_val, 1)]
    ph_labels = ["2022", "2023", "2024", "2025", "2026"]
    fig_ph = go.Figure()
    fig_ph.add_trace(go.Scatter(
        x=ph_labels, y=ph_series, mode="lines+markers",
        line=dict(color="#00d4ff", width=3),
        marker=dict(size=9, color="#39ff14"),
        name="Torpaq pH"
    ))
    fig_ph.update_layout(
        paper_bgcolor="#0c1610", plot_bgcolor="#070f0a",
        font=dict(color="#f2fbf4"), height=260, yaxis_title="pH səviyyəsi"
    )
    st.plotly_chart(fig_ph, use_container_width=True)

if all_mode or sec == "🛰️ NASA Peyk Xəritəsi":
    st.markdown("---")
    st.subheader(f"🛰️ {selected_region} — NASA Peyk və Monitorinq Xəritəsi")
    st.info(
        f"📍 **Dəqiq Koordinat və Zona Göstərişi:** {selected_region} | "
        f"Enlik (Lat): `{reg['lat']}` | Uzunluq (Lon): `{reg['lon']}` | "
        f"Zona: {reg['zone']} | NDVI: `{ndvi_val}` | pH: `{ph_val}`"
    )
    m = folium.Map(
        location=[reg["lat"], reg["lon"]],
        zoom_start=11,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery"
    )
    folium.Circle(
        location=[reg["lat"], reg["lon"]],
        radius=3500,
        color="#39ff14",
        fill=True,
        fill_color="#39ff14",
        fill_opacity=0.22,
        popup=f"{selected_region} Monitorinq Zonası (3.5 km radius)"
    ).add_to(m)
    folium.Marker(
        location=[reg["lat"], reg["lon"]],
        popup=f"{selected_region} | Lat: {reg['lat']}, Lon: {reg['lon']} | pH: {ph_val} | NDVI: {ndvi_val}",
        tooltip=f"{selected_region} — Dəqiq Mərkəz Nöqtəsi"
    ).add_to(m)
    st_folium(m, width=760, height=300)


if all_mode or sec == "📈 10 İllik Torpaq Məhsuldarlığı":
    st.markdown("---")
    st.subheader("📈 Ötən 10 İlin Torpaq Məhsuldarlığı (Artma-Azalma Aralığı)")
    soil_vals = [72, 74, 71, 76, 79, 77, 82, 85, 84, round(ndvi_val * 115, 1)]
    upper_v = [round(x + 4.5, 1) for x in soil_vals]
    lower_v = [round(x - 4.5, 1) for x in soil_vals]

    fig_10s = go.Figure()
    fig_10s.add_trace(go.Scatter(
        x=years_10 + years_10[::-1],
        y=upper_v + lower_v[::-1],
        fill="toself", fillcolor="rgba(57, 255, 20, 0.16)",
        line=dict(color="rgba(0,0,0,0)"), name="Artma-Azalma Aralığı"
    ))
    fig_10s.add_trace(go.Scatter(
        x=years_10, y=soil_vals, mode="lines+markers",
        line=dict(color="#39ff14", width=3), marker=dict(size=8, color="#00d4ff"),
        name="Torpaq Məhsuldarlıq İndeksi"
    ))
    fig_10s.update_layout(
        paper_bgcolor="#0c1610", plot_bgcolor="#070f0a",
        font=dict(color="#f2fbf4"), height=290
    )
    st.plotly_chart(fig_10s, use_container_width=True)

selected_crop = st.selectbox("🌾 Yetişdirmək istədiyiniz bitkini seçin:", list(CROPS.keys()))
crop_info = CROPS[selected_crop]
ph_min, ph_max = crop_info["opt_ph"]
is_suitable = ph_min <= ph_val <= ph_max

if all_mode or sec == "🌾 Bitki Seçimi & 10 İl":
    st.markdown("---")
    st.subheader(f"🌾 {selected_crop} — Son 10 İlin Məhsuldarlıq Qrafiki")
    fig_c = go.Figure()
    fig_c.add_trace(go.Bar(
        x=years_10, y=crop_info["history"],
        marker_color="#39ff14", marker_line_color="#00d4ff", marker_line_width=1.5,
        name=selected_crop
    ))
    fig_c.update_layout(
        paper_bgcolor="#0c1610", plot_bgcolor="#070f0a",
        font=dict(color="#f2fbf4"), height=280, yaxis_title="ton/ha"
    )
    st.plotly_chart(fig_c, use_container_width=True)

    if is_suitable:
        st.success(f"✅ **Əkin Tövsiyəsi:** {crop_info['advice']} (pH {ph_val} bu bitki üçün [{ph_min}–{ph_max}] aralığına uyğundur.)")
    else:
        st.warning(f"⚠️ **Əkin Tövsiyəsi:** {selected_crop} üçün ideal pH [{ph_min}–{ph_max}]-dir. Hazırkı pH ({ph_val}) ilə əkməzdən əvvəl torpağı tənzimləmək məsləhətdir.")

area_ha = st.number_input("Əkin sahəsi (hektar):", min_value=0.5, max_value=500.0, value=2.0, step=0.5)
total_cost = round(crop_info["cost_ha"] * area_ha)
total_rev = round(crop_info["rev_ha"] * area_ha)
net_profit = total_rev - total_cost

if all_mode or sec == "💰 Gəlir, Xərc & Qazanc":
    st.markdown("---")
    st.subheader("💰 Gəlir, Xərc və Qazanc Planı")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Təxmini Xərc", f"{total_cost:,} AZN")
    g2.metric("Gözlənilən Gəlir", f"{total_rev:,} AZN")
    g3.metric("Xalis Qazanc", f"{net_profit:,} AZN")
    g4.metric("Sİ Etibarlılığı", f"{crop_info['conf']}%")

    st.markdown("**Daha çox qazanc gətirəcək addımlar:**")
    for stp in crop_info["steps"]:
        st.info(stp)

if all_mode or sec == "⚖️ Keçən İllə Müqayisə":
    st.markdown("---")
    st.subheader("⚖️ Bu İlki Torpaq Dəyərləri və Məhsuldarlığın Keçən İllə Müqayisəsi")
    cmp_df = pd.DataFrame({
        "Göstərici": ["Torpaq pH", "Məhsuldarlıq (ton/ha)", "Rütubət (%)", "Azot (mq/kq)"],
        "Keçən İl": [reg["prev_ph"], reg["prev_yield"], max(15, moist_val - 4), max(20, n_val - 5)],
        "Bu İl": [ph_val, reg["curr_yield"], moist_val, n_val]
    })
    st.dataframe(cmp_df, use_container_width=True, hide_index=True)

    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(x=cmp_df["Göstərici"], y=cmp_df["Keçən İl"], name="Keçən İl", marker_color="#0077b6"))
    fig_cmp.add_trace(go.Bar(x=cmp_df["Göstərici"], y=cmp_df["Bu İl"], name="Bu İl", marker_color="#39ff14"))
    fig_cmp.update_layout(
        barmode="group", paper_bgcolor="#0c1610", plot_bgcolor="#070f0a",
        font=dict(color="#f2fbf4"), height=280
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

if all_mode or sec == "🤖 Nino AI Köməkçi":
    st.markdown("---")
    st.subheader("🤖 Nino AI — Fermer Köməkçisi")

    preset_questions = [
        ("Hara nə daxil edilməlidir?", f"Sol paneldən rayon ({selected_region}) və ya manual pH/Azot/Rütubət seçin, sonra bitki ({selected_crop}) və hektar ({area_ha} ha) daxil edin."),
        ("Seçdiyim bitki uyğundurmu?", f"{selected_region} torpağında pH {ph_val}-dir. {selected_crop} üçün ideal aralıq [{ph_min}–{ph_max}]-dir. " + ("Uyğundur." if is_suitable else "Əkindən əvvəl pH tənzimlənməsi lazımdır.")),
        ("Qazancı necə artıra bilərəm?", f"Sİ etibarlılığı {crop_info['conf']}%. Əsas addım: {crop_info['steps'][0]}"),
        ("Keçən illə nə fərq var?", f"Məhsuldarlıq keçən il {reg['prev_yield']} ton/ha idi, bu il {reg['curr_yield']} ton/ha-dır (pH fərqi: {ph_val - reg['prev_ph']:+.1f})."),
        ("Suvarma rejimi necə olmalıdır?", f"Hazırkı rütubət {moist_val}%-dir. " + ("Rütubət normaldır, damcı suvarma ilə balansı saxlayın." if moist_val >= 28 else "Rütubət aşağıdır, suvarma tezliyini artırın.")),
        ("Gübrə verilişi nə vaxt edilməlidir?", f"Azot səviyyəsi {n_val} mq/kq-dır. Əsas yemləməni aktiv böyümə və çiçəkləmə/qönçələmə mərhələsində lokal dozada verin."),
        ("Xəritədə hansı nöqtə göstərilir?", f"{selected_region} üzrə Lat: {reg['lat']}, Lon: {reg['lon']} koordinatları və {reg['zone']} əhatə olunur."),
        ("Təxmini xalis qazanc nə qədərdir?", f"{area_ha} hektar {selected_crop} üçün təxmini xərc {total_cost:,} AZN, gəlir {total_rev:,} AZN, xalis qazanc {net_profit:,} AZN-dir.")
    ]

    for row_start in range(0, len(preset_questions), 2):
        c_left, c_right = st.columns(2)
        for col_widget, (q_label, q_ans) in zip([c_left, c_right], preset_questions[row_start:row_start + 2]):
            if col_widget.button(f"❓ {q_label}", key=f"nino_q_{q_label}"):
                st.session_state.nino_history.append(("Fermer", q_label))
                st.session_state.nino_history.append(("Nino", q_ans))

    import re

    with st.form("nino_custom_form", clear_on_submit=True):
        custom_q = st.text_input("Öz şəxsi sualını yaz:", placeholder="Məs: 5 hektara turp əksəm nə qədər qazanaram?")
        submitted = st.form_submit_button("Nino-ya Göndər")
        if submitted and custom_q.strip():
            q_raw = custom_q.strip()
            q_low = q_raw.lower()

            # 1. Sualda xüsusi bitki adı varmı yoxlayırıq
            mentioned_crop = None
            for c_name in CROPS.keys():
                if c_name.lower() in q_low:
                    mentioned_crop = c_name
                    break

            target_crop_name = mentioned_crop if mentioned_crop else selected_crop
            t_info = CROPS[target_crop_name]
            t_min, t_max = t_info["opt_ph"]
            t_suitable = t_min <= ph_val <= t_max

            # 2. Sualda hektar rəqəmi yazılıbsa tuturuq
            ha_match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:hektar|ha)\b", q_low)
            target_ha = float(ha_match.group(1).replace(",", ".")) if ha_match else area_ha

            t_cost = round(t_info["cost_ha"] * target_ha)
            t_rev = round(t_info["rev_ha"] * target_ha)
            t_profit = t_rev - t_cost

            # 3. Sualın mövzusuna görə dəqiq cavab qururuq
            if any(k in q_low for k in ["qazanc", "xərc", "gəlir", "pul", "nə qədər", "neçə"]):
                suit_txt = "uyğundur" if t_suitable else f"ideal pH [{t_min}–{t_max}] olduğu üçün əvvəl torpaq pH ({ph_val}) tənzimlənməlidir"
                reply = (
                    f"{selected_region} ({ph_val} pH) üçün {target_ha} ha **{target_crop_name}** hesabı: "
                    f"xərc ~{t_cost:,} AZN, gəlir ~{t_rev:,} AZN, xalis qazanc ~{t_profit:,} AZN "
                    f"(Sİ etibarlılığı: {t_info['conf']}%). Torpaq uyğunluğu: {suit_txt}."
                )
            elif any(k in q_low for k in ["suvar", "rütubət", "su"]):
                reply = (
                    f"{selected_region} üzrə hazırkı rütubət {moist_val}%-dir. "
                    + ("Rütubət normaldır; damcı suvarma ilə sabit saxlamaq məsləhətdir. " if moist_val >= 28 else "Rütubət aşağıdır; suvarma tezliyini artırmaq lazımdır. ")
                    + f"{target_crop_name} üçün tövsiyə: {t_info['steps'][0]}"
                )
            elif any(k in q_low for k in ["gübrə", "azot", "yemləmə"]):
                reply = (
                    f"{selected_region} üzrə Azot səviyyəsi {n_val} mq/kq-dır. "
                    f"{target_crop_name} üçün əsas aqrokimyəvi addım: {t_info['steps'][1]}"
                )
            elif any(k in q_low for k in ["xəritə", "koordinat", "harada", "zona"]):
                reply = f"{selected_region} koordinatları: Lat {reg['lat']}, Lon {reg['lon']} — {reg['zone']}."
            elif any(k in q_low for k in ["uyğun", "olar", "əkmək", "ph"]):
                reply = (
                    f"{selected_region} torpağında pH {ph_val}-dir. **{target_crop_name}** üçün optimal pH [{t_min}–{t_max}]-dir. "
                    + (f"Hazırkı şərait {target_crop_name} üçün uyğundur." if t_suitable else f"Hazırkı pH ({ph_val}) optimal aralıqdan kənardadır, əvvəl torpağı tənzimləmək lazımdır.")
                )
            else:
                reply = (
                    f"{selected_region} (pH {ph_val}, Azot {n_val} mq/kq, Rütubət {moist_val}%, NDVI {ndvi_val}) və "
                    f"{target_ha} ha **{target_crop_name}** (xalis qazanc ~{t_profit:,} AZN) əsasında cavab: {t_info['steps'][0]}"
                )

            st.session_state.nino_history.append(("Fermer", q_raw))
            st.session_state.nino_history.append(("Nino", reply))


    chat_html = ""
    for sender, msg in st.session_state.nino_history[-8:]:
        tag_color = "#00d4ff" if sender == "Fermer" else "#39ff14"
        chat_html += f"<p style='margin:6px 0;'><b style='color:{tag_color};'>{sender}:</b> {msg}</p>"

    st.markdown(f'<div class="nino-box">{chat_html}</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    Hazırladı: Çiçək Məmmədzadə &nbsp;|&nbsp; C.h.e.MartixAZE © 2026
</div>
""", unsafe_allow_html=True)
