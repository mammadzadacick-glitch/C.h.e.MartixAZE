import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import os

# ---------------------------------------------------------
# 1. SƏHİFƏ KONFİQURASİYASI
# ---------------------------------------------------------
st.set_page_config(
    page_title="C.h.e.MartixAZE | Cyber-Agro AI Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. QARA VƏ FOSFOR YAŞILI (CYBER-AGRO) DİZAYN + ŞRİFTLƏR
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
    --bg-dark: #050806;
    --card-bg: #0c140f;
    --neon-green: #39ff14;
    --neon-cyan: #00d4ff;
    --border-glow: rgba(57, 255, 20, 0.35);
    --text-main: #e8f5e9;
    --text-muted: #9eb3a2;
}

.stApp {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'Space Grotesk', sans-serif;
}

h1, h2, h3, .cyber-title {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--neon-green) !important;
    text-shadow: 0 0 12px rgba(57, 255, 20, 0.45);
    letter-spacing: 0.6px;
}

/* Sol Panel (Sidebar) */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070d09 0%, #0b1610 100%);
    border-right: 1px solid var(--border-glow);
}

/* Göy rəngli direkt giriş düymələri (Sol paneldə) */
.nav-box {
    display: block;
    background: linear-gradient(90deg, #003566, #0077b6);
    color: #ffffff !important;
    padding: 9px 12px;
    margin-bottom: 7px;
    border-radius: 8px;
    text-decoration: none !important;
    font-weight: 700;
    font-size: 13.5px;
    border: 1px solid #00b4d8;
    box-shadow: 0 0 10px rgba(0, 180, 216, 0.3);
    transition: all 0.2s ease;
}
.nav-box:hover {
    background: #0096c7;
    transform: translateX(4px);
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.7);
}

/* Kartlar və Bölmə Ayırıcıları */
.cyber-card {
    background: var(--card-bg);
    border: 1px solid var(--border-glow);
    border-left: 4px solid var(--neon-green);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.65);
}

.badge-neon {
    display: inline-block;
    background: rgba(57, 255, 20, 0.14);
    color: var(--neon-green);
    border: 1px solid var(--neon-green);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

/* Metrik rəqəmlərinin kəsilməməsi üçün */
[data-testid="stMetricValue"] {
    color: var(--neon-green) !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 24px !important;
    white-space: nowrap !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 13px !important;
}

/* Düymələr */
.stButton > button {
    background: linear-gradient(90deg, #1b4332, #2d6a4f);
    color: #39ff14 !important;
    border: 1px solid #39ff14 !important;
    font-weight: 700;
    border-radius: 8px;
    width: 100%;
}
.stButton > button:hover {
    background: #39ff14 !important;
    color: #050806 !important;
}

/* Nino AI sağ panel stili */
.nino-box {
    background: #08120c;
    border: 1.5px solid #39ff14;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 0 18px rgba(57, 255, 20, 0.25);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. BAZA MƏLUMATLARI (RAYONLAR VƏ BİTKİLƏR)
# ---------------------------------------------------------
REGIONS = {
    "Oğuz": {"lat": 41.0714, "lon": 47.4653, "ph": 6.2, "n": 48, "ndvi": 0.74, "moisture": 35, "ec": 1.5, "prev_ph": 6.0, "prev_yield": 4.2, "curr_yield": 4.8},
    "Şəki": {"lat": 41.1919, "lon": 47.1706, "ph": 6.5, "n": 52, "ndvi": 0.71, "moisture": 32, "ec": 1.4, "prev_ph": 6.4, "prev_yield": 4.0, "curr_yield": 4.5},
    "Qəbələ": {"lat": 40.9814, "lon": 47.8458, "ph": 6.1, "n": 55, "ndvi": 0.78, "moisture": 39, "ec": 1.3, "prev_ph": 5.9, "prev_yield": 4.6, "curr_yield": 5.1},
    "Sabirabad": {"lat": 40.0087, "lon": 48.4770, "ph": 7.6, "n": 34, "ndvi": 0.56, "moisture": 22, "ec": 2.8, "prev_ph": 7.8, "prev_yield": 3.1, "curr_yield": 3.4},
    "Gəncə-Göygöl": {"lat": 40.5855, "lon": 46.3189, "ph": 6.8, "n": 45, "ndvi": 0.68, "moisture": 30, "ec": 1.7, "prev_ph": 6.7, "prev_yield": 3.9, "curr_yield": 4.3},
    "Lənkəran": {"lat": 38.7543, "lon": 48.8506, "ph": 5.8, "n": 60, "ndvi": 0.81, "moisture": 44, "ec": 1.2, "prev_ph": 5.7, "prev_yield": 4.9, "curr_yield": 5.4},
}

CROPS = {
    "Pomidor (Tomato)": {
        "opt_ph": (6.0, 6.8), "cost_ha": 2400, "rev_ha": 5200, "conf": 91.4,
        "history": [28, 30, 29, 32, 34, 33, 36, 38, 37, 41],
        "advice": "Bu il torpağın pH və rütubət balansı Pomidor əkini üçün çox əlverişlidir.",
        "steps": [
            "1. Damcı suvarma ilə rütubəti 35–40% aralığında sabit saxlayın (+14% məhsul).",
            "2. Çiçəkləmə dövründə Kalium-fosfat gübrəsi tətbiq edin (+9% məhsul).",
            "3. NASA NDVI xəritəsində zəif görünən kənar cərgələrə lokal azot verin (+6% qənaət)."
        ]
    },
    "Pambıq (Cotton)": {
        "opt_ph": (6.5, 7.8), "cost_ha": 1650, "rev_ha": 3450, "conf": 87.8,
        "history": [2.4, 2.5, 2.7, 2.6, 2.9, 3.1, 3.0, 3.3, 3.4, 3.6],
        "advice": "Orta-isti və neytral/zəif qələvi torpaqlarda Pambıq əkini yüksək gəlir vəd edir.",
        "steps": [
            "1. Səpinqabağı torpaq duzluluğunu (EC) yuyulma ilə 2.0 dS/m-dən aşağı salın.",
            "2. Qönçələmə mərhələsində Karbamid dozalarını 2 mərhələyə bölün (+12% məhsul).",
            "3. Məhsul yığımından 15 gün əvvəl defoliasiya tətbiq edərək itkini azaldın."
        ]
    },
    "Turp (Radish)": {
        "opt_ph": (5.8, 6.8), "cost_ha": 950, "rev_ha": 2350, "conf": 93.2,
        "history": [16, 17, 16.5, 18, 19, 18.5, 20, 21, 21.5, 23],
        "advice": "Qısa vegetasiya dövrü və sürətli dövriyyə üçün Turp əkini bu il tövsiyə olunur.",
        "steps": [
            "1. Yumşaq və daşsız şum qatı hazırlayın ki, kökümeyvələr deformasiya olmasın.",
            "2. Həddindən artıq azotdan qaçın (yarpaq böyüyər, kök kiçik qalar).",
            "3. Müntəzəm səhər suvarması ilə acılaşmanın qarşısını alın (+15% bazar dəyəri)."
        ]
    },
    "Buğda (Wheat)": {
        "opt_ph": (6.0, 7.5), "cost_ha": 780, "rev_ha": 1680, "conf": 89.5,
        "history": [3.1, 3.2, 3.0, 3.4, 3.5, 3.3, 3.7, 3.8, 3.9, 4.2],
        "advice": "Geniş sahələrdə stabil və az riskli gəlir üçün payızlıq/yazlıq Buğda məsləhətdir.",
        "steps": [
            "1. Kollanma fazasında ammonium-nitrat tətbiqini peyk rütubət proqnozuna uyğunlaşdırın.",
            "2. Alaq otlarına qarşı erkən herbisid müdaxiləsi məhsuldarlığı +11% artırır.",
            "3. Dən dolma dövründə yarpaqdan mikroelement çiləməsi aparın."
        ]
    },
    "Kartof (Potato)": {
        "opt_ph": (5.5, 6.5), "cost_ha": 2700, "rev_ha": 5800, "conf": 90.1,
        "history": [19, 20, 21, 20.5, 22, 23, 24, 23.5, 25, 27],
        "advice": "Zəif turşulu (pH 5.8–6.4) dağətəyi torpaqlarda Kartof maksimum gəlir verir.",
        "steps": [
            "1. Sertifikatlı toxumluq yumrulardan istifadə edərək xəstəlik riskini 40% azaldın.",
            "2. Doldurma (dibdoldurma) əməliyyatını vaxtında aparın (+13% məhsul).",
            "3. Kalium sulfat gübrəsi ilə nişasta faizini və saxlanma müddətini artırın."
        ]
    },
    "Qarğıdalı (Corn)": {
        "opt_ph": (5.8, 7.0), "cost_ha": 1350, "rev_ha": 3100, "conf": 88.6,
        "history": [5.8, 6.0, 6.2, 6.1, 6.5, 6.8, 6.7, 7.1, 7.3, 7.6],
        "advice": "Suvarma imkanı olan sahələrdə Qarğıdalı yüksək rentabellik göstərir.",
        "steps": [
            "1. 6–8 yarpaq fazasında cərgəarası kultivasiya və azot yemləməsi edin.",
            "2. Saçaqlama dövründə su stresinə yol verməyin (bu mərhələdə məhsulun 50%-i formalaşır).",
            "3. Sıxlığı hektara 65–70 min bitki səviyyəsində tənzimləyin."
        ]
    }
}

# ---------------------------------------------------------
# 4. SOL TƏRƏF: İSTİFADƏ PANELİ, AXTARIŞ VƏ GÖY DİREKT QUTUCUQLAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌱 C.h.e.MartixAZE")
    st.caption("NASA Peyk + Aqrokimya Sİ Platforması")

    search_query = st.text_input("🔍 Bölmə və ya funksiya axtar...", placeholder="Məs: pH, Nino, Gəlir, Bitki...")

    st.markdown("### 🧭 Sürətli Keçid (Direkt Giriş)")
    nav_items = [
        ("🎬 45 san. Təlimat Video Çarxı", "#video-guide"),
        ("🛰️ NASA Peyk Xəritəsi", "#satellite-map"),
        ("🧪 pH və Torpaq Kimyası Analizi", "#soil-metrics"),
        ("📈 10 İllik Torpaq Məhsuldarlığı", "#soil-10yr"),
        ("🌾 Bitki Seçimi & 10 İllik Qrafik", "#crop-selector"),
        ("💰 Gəlir, Xərc və Qazanc Planı", "#profit-calc"),
        ("⚖️ Keçən İllə Müqayisə", "#year-compare"),
        ("🤖 Nino AI Köməkçi", "#nino-ai"),
    ]

    for label, anchor in nav_items:
        if not search_query or search_query.lower() in label.lower():
            st.markdown(f'<a class="nav-box" href="{anchor}">{label}</a>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### ⚙️ Analiz Parametrləri")
    data_mode = st.radio("Məlumat Mənbəyi:", ["Rayon Seçimi (NASA Peyk + Baza)", "Manual Daxiletmə (Sürüşdürücülər)"])
    selected_region = st.selectbox("Tədqiqat Bölgəsi:", list(REGIONS.keys()))

    reg = REGIONS[selected_region]
    if data_mode == "Manual Daxiletmə (Sürüşdürücülər)":
        ph_val = st.slider("Torpaq pH", 4.5, 9.0, float(reg["ph"]), 0.1)
        n_val = st.slider("Azot (N) mq/kq", 10, 100, int(reg["n"]))
        ndvi_val = st.slider("NASA NDVI İndeksi", 0.10, 0.95, float(reg["ndvi"]), 0.01)
        moist_val = st.slider("Torpaq Rütubəti (%)", 5, 80, int(reg["moisture"]))
    else:
        ph_val, n_val, ndvi_val, moist_val = reg["ph"], reg["n"], reg["ndvi"], reg["moisture"]

    st.success(f"🛰️ {selected_region} üzrə NASA peyk datası aktivdir.")

# ---------------------------------------------------------
# 5. ƏSAS EKRAN + SAĞ KÜNCDƏ NİNO AI PANELİ
# ---------------------------------------------------------
main_col, nino_col = st.columns([3.1, 1.25], gap="large")

with main_col:
    st.markdown("""
    <div class="cyber-card">
        <span class="badge-neon">NASA SATELLITE + AGRO-CHEMISTRY AI</span>
        <h1 style="margin-top:8px; margin-bottom:4px;">C.h.e.MartixAZE</h1>
        <p style="color:#9eb3a2; font-size:15px; margin:0;">
            Süni İntellekt və peyk verilənləri əsasında torpaq kimyası, 10 illik məhsuldarlıq dinamikası və gəlir optimallaşdırma platforması.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # BÖLMƏ 1: 45 SANİYƏLİK TƏLİMAT VİDEO ÇARXI
    st.markdown('<div id="video-guide"></div>', unsafe_allow_html=True)
    with st.expander("🎬 Bələdçi Video Çarx (45 saniyə): Sayt nə işə yarayır və hara nə daxil edilməlidir?", expanded=True):
        if os.path.exists("chemartix_guide.mp4"):
            st.video("chemartix_guide.mp4", autoplay=True)
        st.markdown("""
        <div style="background:#030604; border:1px solid #39ff14; border-radius:12px; padding:16px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="color:#39ff14; font-weight:700;">▶ C.h.e.MartixAZE — Sürətli İstifadə Bələdçisi (00:45)</span>
                <span style="background:#39ff14; color:#050806; padding:2px 8px; border-radius:6px; font-size:12px; font-weight:700;">HD • 45 SAN</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-top:8px;">
                <div style="background:#0c1811; border:1px solid #1f4d32; padding:10px; border-radius:8px;">
                    <b style="color:#00d4ff;">0:00 – 0:15 | 1-ci Addım</b><br>
                    <span style="font-size:13px; color:#d8f3dc;">Sol paneldən <b>Rayonunuzu</b> seçin və ya <b>Manual</b> rejimdə pH, Azot və Rütubət rəqəmlərini daxil edin.</span>
                </div>
                <div style="background:#0c1811; border:1px solid #1f4d32; padding:10px; border-radius:8px;">
                    <b style="color:#39ff14;">0:15 – 0:30 | 2-ci Addım</b><br>
                    <span style="font-size:13px; color:#d8f3dc;"><b>Bitki Seçimi</b> qutusundan əkmək istədiyiniz bitkini (Pomidor, Pambıq, Turp və s.) seçin və 10 illik qrafikə baxın.</span>
                </div>
                <div style="background:#0c1811; border:1px solid #1f4d32; padding:10px; border-radius:8px;">
                    <b style="color:#ffd166;">0:30 – 0:45 | 3-cü Addım</b><br>
                    <span style="font-size:13px; color:#d8f3dc;"><b>Gəlir-Xərc</b> hesablamasını yoxlayın və sağ küncdəki <b>Nino AI</b>-dan suallarınıza dərhal cavab alın.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # BÖLMƏ 2: TORPAQ KİMYASI METRİKLƏRİ VƏ NASA XƏRİTƏSİ
    st.markdown('<div id="soil-metrics"></div>', unsafe_allow_html=True)
    st.subheader(f"🧪 {selected_region} — Torpaq Kimyası və Peyk Göstəriciləri")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Torpaq pH", f"{ph_val:.1f}", f"{ph_val - reg['prev_ph']:+.1f} keçən ilə görə")
    m2.metric("Azot (N)", f"{n_val} mq/kq", "Optimal" if n_val >= 40 else "Aşağı")
    m3.metric("NASA NDVI", f"{ndvi_val:.2f}", "Sağlam örtük" if ndvi_val >= 0.65 else "Zəif örtük")
    m4.metric("Rütubət", f"{moist_val}%", "Normal" if moist_val >= 28 else "Suvarma lazımdır")

    st.markdown('<div id="satellite-map"></div>', unsafe_allow_html=True)
    with st.expander("🛰️ NASA Peyk və Monitorinq Xəritəsini Aç / Bağla", expanded=False):
        m = folium.Map(location=[reg["lat"], reg["lon"]], zoom_start=11, tiles="CartoDB dark_matter")
        folium.CircleMarker(
            location=[reg["lat"], reg["lon"]],
            radius=16,
            color="#39ff14",
            fill=True,
            fill_color="#39ff14",
            fill_opacity=0.45,
            popup=f"{selected_region} | pH: {ph_val} | NDVI: {ndvi_val}"
        ).add_to(m)
        st_folium(m, width=750, height=280)

    # BÖLMƏ 3: ÖTƏN 10 İLİN TORPAQ MƏHSULDARLIĞI
    st.markdown('<div id="soil-10yr"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📈 Ötən 10 İlin Torpaq Məhsuldarlığı və Artma-Azalma Aralığı (2017–2026)")

    years_10 = [str(y) for y in range(2017, 2027)]
    base_index = [72, 74, 71, 76, 79, 77, 82, 85, 84, round(ndvi_val * 115, 1)]
    upper_band = [round(v + 4.5, 1) for v in base_index]
    lower_band = [round(v - 4.5, 1) for v in base_index]


