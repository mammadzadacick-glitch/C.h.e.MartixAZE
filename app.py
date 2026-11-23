import streamlit as st
import streamlit.components.v1 as components
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
    --card-bg: #0c1510;
    --neon-green: #39ff14;
    --neon-cyan: #00d4ff;
    --border-glow: rgba(57, 255, 20, 0.42);
    --text-main: #eefaf0;
    --text-muted: #a6bfab;
}

.stApp {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'Space Grotesk', sans-serif;
}

h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--neon-green) !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

.brand-nowrap {
    white-space: nowrap !important;
    display: inline-block;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070e0a 0%, #0b1811 100%);
    border-right: 1px solid var(--border-glow);
}

.cyber-card {
    background: var(--card-bg);
    border: 1px solid var(--border-glow);
    border-left: 5px solid var(--neon-green);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}

.badge-neon {
    display: inline-block;
    background: rgba(57, 255, 20, 0.15);
    color: var(--neon-green);
    border: 1px solid var(--neon-green);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: var(--neon-green) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* Sol paneldəki göy aktiv düymələr */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(90deg, #003566, #0077b6) !important;
    color: #ffffff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    text-align: left !important;
    width: 100% !important;
    padding: 8px 12px !important;
    box-shadow: 0 0 10px rgba(0, 180, 216, 0.25);
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(90deg, #0077b6, #00b4d8) !important;
    border-color: #39ff14 !important;
    color: #39ff14 !important;
}

/* Əsas səhifədəki düymələr */
.main .stButton > button {
    background: #102418 !important;
    color: #39ff14 !important;
    border: 1px solid #39ff14 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.main .stButton > button:hover {
    background: #39ff14 !important;
    color: #050806 !important;
}

.nino-box {
    background: #08150d;
    border: 1.5px solid #39ff14;
    border-radius: 12px;
    padding: 14px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

REGIONS = {
    "Oğuz": {"lat": 41.0714, "lon": 47.4653, "ph": 6.2, "n": 48, "ndvi": 0.74, "moisture": 35, "prev_ph": 6.0, "prev_yield": 4.2, "curr_yield": 4.8},
    "Şəki": {"lat": 41.1919, "lon": 47.1706, "ph": 6.5, "n": 52, "ndvi": 0.71, "moisture": 32, "prev_ph": 6.4, "prev_yield": 4.0, "curr_yield": 4.5},
    "Qəbələ": {"lat": 40.9814, "lon": 47.8458, "ph": 6.1, "n": 55, "ndvi": 0.78, "moisture": 39, "prev_ph": 5.9, "prev_yield": 4.6, "curr_yield": 5.1},
    "Sabirabad": {"lat": 40.0087, "lon": 48.4770, "ph": 7.6, "n": 34, "ndvi": 0.56, "moisture": 22, "prev_ph": 7.8, "prev_yield": 3.1, "curr_yield": 3.4},
    "Gəncə-Göygöl": {"lat": 40.5855, "lon": 46.3189, "ph": 6.8, "n": 45, "ndvi": 0.68, "moisture": 30, "prev_ph": 6.7, "prev_yield": 3.9, "curr_yield": 4.3},
    "Lənkəran": {"lat": 38.7543, "lon": 48.8506, "ph": 5.8, "n": 60, "ndvi": 0.81, "moisture": 44, "prev_ph": 5.7, "prev_yield": 4.9, "curr_yield": 5.4},
}

CROPS = {
    "Pomidor": {
        "opt_ph": (6.0, 6.8), "cost_ha": 2400, "rev_ha": 5200, "conf": 91.4,
        "history": [28, 30, 29, 32, 34, 33, 36, 38, 37, 41],
        "advice": "Bu il Pomidor əkini məsləhətdir — torpaq pH və rütubət göstəriciləri uyğundur.",
        "steps": [
            "1. Damcı suvarma ilə rütubəti 35–40% aralığında saxlayın (+14% məhsul).",
            "2. Çiçəkləmə mərhələsində Kalium-fosfat gübrəsi tətbiq edin (+9% məhsul).",
            "3. NASA NDVI xəritəsində zəif zonalara lokal azot verin (+6% qənaət)."
        ]
    },
    "Pambıq": {
        "opt_ph": (6.5, 7.8), "cost_ha": 1650, "rev_ha": 3450, "conf": 87.8,
        "history": [2.4, 2.5, 2.7, 2.6, 2.9, 3.1, 3.0, 3.3, 3.4, 3.6],
        "advice": "İsti və balanslı sahələrdə bu il Pambıq əkini məsləhətdir.",
        "steps": [
            "1. Səpinqabağı duzluluğu nəzarətdə saxlayın.",
            "2. Qönçələmə fazasında azot tətbiqini iki mərhələdə aparın (+12% məhsul).",
            "3. Yığım zamanı məhsul itkisini minimuma endirin."
        ]
    },
    "Turp": {
        "opt_ph": (5.8, 6.8), "cost_ha": 950, "rev_ha": 2350, "conf": 93.2,
        "history": [16, 17, 16.5, 18, 19, 18.5, 20, 21, 21.5, 23],
        "advice": "Qısa müddətdə stabil dövriyyə üçün bu il Turp əkini məsləhətdir.",
        "steps": [
            "1. Yumşaq və daşsız torpaq hazırlayın.",
            "2. Artıq azotdan çəkinin (yarpaq çoxalıb kök kiçik qalmasın).",
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

# ---------------------------------------------------------
# SOL PANEL: AXTARIŞ + İŞLƏK GÖY QUTUCUQLAR + PARAMETRLƏR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌱 <span class='brand-nowrap'>C.h.e.MartixAZE</span>", unsafe_allow_html=True)
    st.caption("NASA Peyk + Aqrokimya Sİ")

    search_txt = st.text_input("🔍 Bölmə axtar:", placeholder="pH, video, bitki, gəlir, nino...")

    st.markdown("### 🟦 Sürətli Keçid Qutucuqları")
    blue_boxes = [
        "Bütün Bölmələr",
        "🎬 45 san. Video Çarx",
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

# ---------------------------------------------------------
# YUXARI BAŞLIQ
# ---------------------------------------------------------
st.markdown(f"""
<div class="cyber-card">
    <span class="badge-neon">CYBER-AGRO AI PLATFORM</span>
    <h1 style="margin:6px 0 4px 0;"><span class="brand-nowrap">C.h.e.MartixAZE</span></h1>
    <p style="color:#a6bfab; margin:0; font-size:14px;">
        Aktiv bölmə: <b style="color:#39ff14;">{st.session_state.selected_section}</b> | Rayon: <b style="color:#00d4ff;">{selected_region}</b>
    </p>
</div>
""", unsafe_allow_html=True)

sec = st.session_state.selected_section
all_mode = (sec == "Bütün Bölmələr")
years_10 = [str(y) for y in range(2017, 2027)]

# ---------------------------------------------------------
# 1. 45 SANİYƏLİK TƏLİMAT VİDEO ÇARXI
# ---------------------------------------------------------
if all_mode or sec == "🎬 45 san. Video Çarx":
    st.subheader("🎬 45 Saniyəlik Təlimat Video Çarxı: Sayt Nə İşə Yarayır və Hara Nə Yazılır?")
    if os.path.exists("chemartix_guide.mp4"):
        st.video("chemartix_guide.mp4", autoplay=True)
    else:
        components.html("""
        <div style="background:#07110c; border:1.5px solid #39ff14; border-radius:12px; padding:12px; color:#eefaf0; font-family:sans-serif;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div>
                    <button onclick="togglePlay()" id="pBtn" style="background:#39ff14; color:#050806; border:none; padding:6px 12px; border-radius:6px; font-weight:700; cursor:pointer;">▶ Başlat / Pauza</button>
                    <button onclick="restartVid()" style="background:#12261a; color:#39ff14; border:1px solid #39ff14; padding:6px 12px; border-radius:6px; font-weight:700; cursor:pointer; margin-left:6px;">↺ 00:00</button>
                </div>
                <span id="tDisp" style="color:#00d4ff; font-weight:700;">00s / 45s</span>
            </div>
            <canvas id="c1" width="760" height="220" style="width:100%; border-radius:8px; background:#030704; border:1px solid #1e4d30;"></canvas>
            <div style="width:100%; height:7px; background:#122419; border-radius:6px; margin-top:8px; overflow:hidden;">
                <div id="bar1" style="width:0%; height:100%; background:#39ff14;"></div>
            </div>
        </div>
        <script>
            const cv = document.getElementById("c1");
            const cx = cv.getContext("2d");
            let s = 0, run = true;
            const parts = [
                {a:0, b:15, h:"00:00 - 00:15 | SAYT NE ISE YARAYIR?", l1:"Torpagin pH, Azot (N), Rutubet ve NASA NDVI deyerlerini analiz edir.", l2:"Oten 10 ilin mehsuldarliq qrafikini ve kecen ille muqayiseni gosterir.", l3:"Fermer ucun qazanc plani, addim-addim tovsiyeler ve Nino AI verir."},
                {a:15, b:30, h:"00:15 - 00:30 | HARA NE DAXIL EDILMELIDIR?", l1:"Sol panelden Rayonu secin ve ya Manual rejimde pH, Azot, Rutubet yazin.", l2:"Sol paneldeki goy qutucuqlara basib istediyiniz bolmeni acin.", l3:"Bitki secimi qutusundan Pomidor, Pambiq, Turp, Bugda, Kartof, Qargidali secin."},
                {a:30, b:45, h:"00:30 - 00:45 | QAZANC PLANI VE NINO AI", l1:"Hektar sayini daxil edib xerc, gelir, xalis qazanc ve SI etibarliligina baxin.", l2:"Daha cox qazanc ucun gosterilen addimlari ardicil tetbiq edin.", l3:"Nino AI suallarina toxunub her addimda qisa cavab alin."}
            ];
            function render() {
                cx.fillStyle="#040805"; cx.fillRect(0,0,cv.width,cv.height);
                const p = parts.find(x => s >= x.a && s < x.b) || parts[2];
                cx.strokeStyle="#39ff14"; cx.lineWidth=2; cx.strokeRect(12,12,cv.width-24,cv.height-24);
                cx.fillStyle="#00d4ff"; cx.font="bold 16px sans-serif"; cx.fillText(p.h, 28, 42);
                cx.fillStyle="#eefaf0"; cx.font="14px sans-serif";
                cx.fillText("• " + p.l1, 28, 82);
                cx.fillText("• " + p.l2, 28, 122);
                cx.fillText("• " + p.l3, 28, 162);
                document.getElementById("tDisp").innerText = String(s).padStart(2,"0") + "s / 45s";
                document.getElementById("bar1").style.width = ((s/45)*100) + "%";
            }
            function togglePlay(){ run=!run; document.getElementById("pBtn").innerText = run ? "⏸ Pauza" : "▶ Davam Et"; }
            function restartVid(){ s=0; run=true; render(); }
            render();
            setInterval(()=>{ if(run){ s=(s+1)%46; render(); } }, 1000);
        </script>
        """, height=295)

# ---------------------------------------------------------
# 2. pH VƏ TORPAQ KİMYASI QRAFİKİ
# ---------------------------------------------------------
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
    fig_ph.add_trace(go.Scatter(x=ph_labels, y=ph_series, mode="lines+markers", line=dict(color="#00d4ff", width=3), marker=dict(size=9, color="#39ff14"), name="Torpaq pH"))
    fig_ph.update_layout(paper_bgcolor="#0c1510", plot_bgcolor="#070e0a", font=dict(color="#eefaf0"), height=260, yaxis_title="pH səviyyəsi")
    st.plotly_chart(fig_ph, use_container_width=True)

# ---------------------------------------------------------
# 3. NASA PEYK XƏRİTƏSİ
# ---------------------------------------------------------
if all_mode or sec == "🛰️ NASA Peyk Xəritəsi":
    st.markdown("---")
    st.subheader(f"🛰️ {selected_region} — NASA Peyk və Monitorinq Xəritəsi")
    m = folium.Map(location=[reg["lat"], reg["lon"]], zoom_start=11, tiles="CartoDB dark_matter")
    folium.CircleMarker(
        location=[reg["lat"], reg["lon"]],
        radius=16, color="#39ff14", fill=True, fill_color="#39ff14", fill_opacity=0.45,
        popup=f"{selected_region} | pH: {ph_val} | NDVI: {ndvi_val}"
    ).add_to(m)
    st_folium(m, width=740, height=270)

# ---------------------------------------------------------
# 4. ÖTƏN 10 İLİN TORPAQ MƏHSULDARLIĞI (ARTMA-AZALMA ARALIĞI)
# ---------------------------------------------------------
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
    fig_10s.update_layout(paper_bgcolor="#0c1510", plot_bgcolor="#070e0a", font=dict(color="#eefaf0"), height=290)
    st.plotly_chart(fig_10s, use_container_width=True)

# ---------------------------------------------------------
# 5. BİTKİ SEÇİMİ + 10 İLLİK BİTKİ QRAFİKİ + TÖVSİYƏ
# ---------------------------------------------------------
selected_crop = st.selectbox("🌾 Yetişdirmək istədiyiniz bitkini seçin:", list(CROPS.keys()))
crop_info = CROPS[selected_crop]
ph_min, ph_max = crop_info["opt_ph"]
is_suitable = ph_min <= ph_val <= ph_max

if all_mode or sec == "🌾 Bitki Seçimi & 10 İl":
    st.markdown("---")
    st.subheader(f"🌾 {selected_crop} — Son 10 İlin Məhsuldarlıq Qrafiki")
    fig_c = go.Figure()
    fig_c.add_trace(go.Bar(x=years_10, y=crop_info["history"], marker_color="#39ff14", marker_line_color="#00d4ff", marker_line_width=1.5, name=selected_crop))
    fig_c.update_layout(paper_bgcolor="#0c1510", plot_bgcolor="#070e0a", font=dict(color="#eefaf0"), height=280, yaxis_title="ton/ha")
    st.plotly_chart(fig_c, use_container_width=True)

    if is_suitable:
        st.success(f"✅ **Əkin Tövsiyəsi:** {crop_info['advice']} (pH {ph_val} bu bitki üçün [{ph_min}–{ph_max}] aralığına uyğundur.)")
    else:
        st.warning(f"⚠️ **Əkin Tövsiyəsi:** {selected_crop} üçün ideal pH [{ph_min}–{ph_max}]-dir. Hazırkı pH ({ph_val}) ilə əkməzdən əvvəl torpağı tənzimləmək məsləhətdir.")

# ---------------------------------------------------------
# 6. GƏLİR, XƏRC, QAZANC, Sİ ETİBARLILIĞI VƏ ADDIMLAR
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 7. KEÇƏN İLLƏ MÜQAYİSƏ (CƏDVƏL + QRAFİK)
# ---------------------------------------------------------
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
    fig_cmp.update_layout(barmode="group", paper_bgcolor="#0c1510", plot_bgcolor="#070e0a", font=dict(color="#eefaf0"), height=280)
    st.plotly_chart(fig_cmp, use_container_width=True)

# ---------------------------------------------------------
# 8. NİNO AI KÖMƏKÇİ (ŞABLON SUALLARLA)
# ---------------------------------------------------------
if all_mode or sec == "🤖 Nino AI Köməkçi":
    st.markdown("---")
    st.subheader("🤖 Nino AI — Köməkçi")
    if "nino_reply" not in st.session_state:
        st.session_state.nino_reply = f"Salam! Mən **Nino**. **{selected_region}** və **{selected_crop}** üzrə suallarını qısa cavablandırıram."

    b1, b2, b3, b4 = st.columns(4)
    if b1.button("Hara nə yazılır?"):
        st.session_state.nino_reply = "Sol paneldən rayon/pH/Azot seçin, bitki seçin və hektar sayını yazın."
    if b2.button("Bitki uyğundurmu?"):
        st.session_state.nino_reply = f"{selected_region} (pH {ph_val}) üçün {selected_crop} ideal pH aralığı [{ph_min}–{ph_max}]-dir. " + ("Uyğundur." if is_suitable else "pH tənzimlənməsi lazımdır.")
    if b3.button("Qazancı necə artırım?"):
        st.session_state.nino_reply = f"Sİ etibarlılığı {crop_info['conf']}%. İlk addım: {crop_info['steps'][0]}"
    if b4.button("Keçən illə fərq?"):
        st.session_state.nino_reply = f"Məhsuldarlıq keçən il {reg['prev_yield']} ton/ha idi, bu il {reg['curr_yield']} ton/ha-dır."

    ask_nino = st.text_input("Nino-ya qısa sual yaz:", placeholder="Sualını yaz...")
    if ask_nino:
        st.session_state.nino_reply = f"**Nino:** '{ask_nino}' üzrə {selected_region} pH={ph_val}, {selected_crop} təxmini xalis qazanc {net_profit:,} AZN."

    st.markdown(f'<div class="nino-box">{st.session_state.nino_reply}</div>', unsafe_allow_html=True)

st.markdown("<br><center style='color:#7d9984; font-size:12px;'>C.h.e.MartixAZE © 2026</center>", unsafe_allow_html=True)
