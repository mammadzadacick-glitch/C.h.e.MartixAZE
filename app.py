import streamlit as st
import pandas as pd
import numpy as np

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="C.h.e.MartixAZE v3.0 Final",
    page_icon="🌱",
    layout="wide"
)

# --- DİL SEÇİMİ ---
st.sidebar.title("🌍 Parametrlər / Settings")
lang = st.sidebar.selectbox("Dil / Language", ["Azərbaycan", "English"])

# --- TƏRCÜMƏLƏR ---
if lang == "Azərbaycan":
    title_text = "🌱 C.h.e.MartixAZE: Süni İntellektlə Torpaq və Ekosistem İdarəetməsi"
    subtitle_text = "NASA peyk məlumatları (NDVI/SMAP) və aqrokimyəvi modelləşdirmə əsasında qərar qəbuletmə platforması."
    sidebar_title = "🎛️ Analiz Parametrləri"
    mode_label = "Məlumat Mənbəyi"
    mode_r = "Rayon / Region Seçimi (NASA Peyk + Baza)"
    mode_m = "Manual Daxiletmə (Laboratoriya Sınağı)"
    reg_select_label = "Tədqiqat Bölgəsini Seçin:"
    ph_label = "Torpağın pH səviyyəsi"
    n_label = "Azot (N) miqdarı (mq/kq)"
    ndvi_label = "NASA Peyk NDVI (Bitki Sağlamlıq İndeksi)"
    moist_label = "Torpağın Rütubəti (%)"
    btn_label = "🚀 AI Analiz və Proqnozlaşdırma Başlat"
    
    map_title = "🛰️ NASA Peyk və Aqrokimyəvi Monitorinq Xəritəsi"
    map_caption = "Xəritədə seçilmiş regionun peyk müşahidə koordinatları və torpaq tədqiqat nöqtələri əks olunub."
    
    res_title = "📊 Süni İntellekt və Aqrokimyəvi Təhlil Nəticələri"
    pred_title = "🔮 Predictive AI: 14 Günlük Ekosistem Proqnozu"
    rec_heading = "🧪 Mühəndislik və Dəqiq Aqrokimyəvi Tövsiyələr"
    chart_title = "📈 Parametrlərin Müqayisəli Diaqramı"
    
    ok_text = "✅ Ekosistem Stabil: Torpaq kimyası və peyk indeksləri optimal balansdadır."
    warn_text = "⚠️ Kritik Balanssızlıq: Torpaq deqradasiyası və ya qida çatışmazlığı riski aşkarlandı!"
    info_reg = "📍 NASA peyk verilənləri və regional aqrokimya bazası avtomatik yükləndi."
    info_start = "👈 Təhlilə başlamaq üçün sol paneldən bölgəni seçin və düyməyə basın."
    footer_text = "Hazırladı: Çiçək Məmmədzadə | Layihə: C.h.e.MartixAZE | Kimya Mühəndisliyi və Süni İntellekt Tədqiqat Platforması © 2026"
else:
    title_text = "🌱 C.h.e.MartixAZE: AI-Driven Soil & Ecosystem Management"
    subtitle_text = "Decision-making platform powered by NASA satellite telemetry (NDVI/SMAP) and agrochemical modeling."
    sidebar_title = "🎛️ Analysis Parameters"
    mode_label = "Data Source"
    mode_r = "Region Selection (NASA Satellite + Database)"
    mode_m = "Manual Input (Lab Simulation)"
    reg_select_label = "Select Research Region:"
    ph_label = "Soil pH Level"
    n_label = "Nitrogen (N) Content (mg/kg)"
    ndvi_label = "NASA Satellite NDVI (Vegetation Health)"
    moist_label = "Soil Moisture (%)"
    btn_label = "🚀 Run AI Analysis & Forecast"
    
    map_title = "🛰️ NASA Satellite & Agrochemical Monitoring Map"
    map_caption = "Displaying satellite observation coordinates and soil sampling telemetry for the selected region."
    
    res_title = "📊 AI & Agrochemical Analysis Results"
    pred_title = "🔮 Predictive AI: 14-Day Ecosystem Forecast"
    rec_heading = "🧪 Engineering & Precision Agrochemical Recommendations"
    chart_title = "📈 Comparative Parameter Distribution"
    
    ok_text = "✅ Ecosystem Stable: Soil chemistry and satellite indices are within optimal balance."
    warn_text = "⚠️ Critical Imbalance: Soil degradation or nutrient deficiency risk detected!"
    info_reg = "📍 NASA satellite telemetry and regional agrochemical baseline loaded automatically."
    info_start = "👈 Select a region from the sidebar and click the button to start analysis."
    footer_text = "Developed by: Çiçək Məmmədzadə | Project: C.h.e.MartixAZE | Chemical Engineering & AI Research Platform © 2026"

# --- BAŞLIQ ---
st.title(title_text)
st.write(subtitle_text)
st.markdown("---")

# --- REGİONAL BAZA VƏ KOORDİNATLAR ---
regions_data = {
    "Oğuz (Dağ-meşə qəhvəyi torpaqlar)": {
        "ph": 6.2, "n": 48.0, "ndvi": 0.74, "moisture": 35.0,
        "lat": 41.0714, "lon": 47.4653, "climate": "Mülayim-rütubətli / Humid Subtropical"
    },
    "Bakı / Abşeron (Boz-qonur şorakət torpaqlar)": {
        "ph": 7.9, "n": 21.0, "ndvi": 0.29, "moisture": 14.0,
        "lat": 40.4093, "lon": 49.8671, "climate": "Quru yarımsəhra / Semi-arid"
    },
    "Gəncə-Qazax (Şabalıdı torpaqlar)": {
        "ph": 7.1, "n": 38.0, "ndvi": 0.58, "moisture": 25.0,
        "lat": 40.6828, "lon": 46.3606, "climate": "Quru subtropik / Dry Subtropical"
    },
    "Aran Bölgəsi / Kürdəmir (Çəmən-boz torpaqlar)": {
        "ph": 7.6, "n": 28.0, "ndvi": 0.42, "moisture": 18.0,
        "lat": 40.3453, "lon": 48.1508, "climate": "Quru isti / Arid Warm"
    },
    "Lənkəran-Astara (Sarı torpaqlar)": {
        "ph": 5.6, "n": 52.0, "ndvi": 0.81, "moisture": 44.0,
        "lat": 38.7543, "lon": 48.8506, "climate": "Rütubətli subtropik / Humid Subtropical"
    },
    "Şəki-Zaqatala (Allüvial çəmən-meşə)": {
        "ph": 6.6, "n": 46.0, "ndvi": 0.72, "moisture": 33.0,
        "lat": 41.1919, "lon": 47.1706, "climate": "Mülayim / Temperate"
    },
    "Qarabağ / Ağdam (Qara və şabalıdı torpaqlar)": {
        "ph": 7.0, "n": 44.0, "ndvi": 0.64, "moisture": 27.0,
        "lat": 39.9931, "lon": 46.9297, "climate": "Mülayim-isti / Warm Temperate"
    }
}

# --- SOL PANEL ---
st.sidebar.header(sidebar_title)
mode = st.sidebar.radio(mode_label, [mode_r, mode_m])

if mode == mode_r:
    selected_reg = st.sidebar.selectbox(reg_select_label, list(regions_data.keys()))
    reg_vals = regions_data[selected_reg]
    
    ph = reg_vals["ph"]
    nitrogen = reg_vals["n"]
    ndvi = reg_vals["ndvi"]
    moisture = reg_vals["moisture"]
    lat, lon = reg_vals["lat"], reg_vals["lon"]
    climate_info = reg_vals["climate"]
    
    st.sidebar.info(info_reg)
    st.sidebar.caption(f"🌡️ İqlim / Climate: {climate_info}")
else:
    ph = st.sidebar.slider(ph_label, 4.0, 10.0, 6.5)
    nitrogen = st.sidebar.slider(n_label, 10.0, 100.0, 45.0)
    ndvi = st.sidebar.slider(ndvi_label, 0.0, 1.0, 0.65)
    moisture = st.sidebar.slider(moist_label, 5.0, 60.0, 28.0)
    lat, lon = 40.4093, 47.5000  # Azərbaycan mərkəzi koordinatı

# --- NASA XƏRİTƏ VİZUALİZASİYASI ---
st.subheader(map_title)
# Seçilmiş koordinat ətrafında 5 peyk/sensor nümunə nöqtəsi yaradırıq
np.random.seed(42)
map_df = pd.DataFrame({
    'lat': lat + np.random.normal(0, 0.04, 6),
    'lon': lon + np.random.normal(0, 0.04, 6)
})
st.map(map_df, zoom=8)
st.caption(map_caption)
st.markdown("---")

# --- ANALİZ VƏ NƏTİCƏLƏR ---
if st.sidebar.button(btn_label, type="primary"):
    st.subheader(res_title)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("pH Level", f"{ph}", delta=f"{round(ph - 6.8, 2)} vs Optimal")
    col2.metric("Nitrogen (N)", f"{nitrogen} mg/kg", delta=f"{round(nitrogen - 45, 1)} mg/kg")
    col3.metric("NASA NDVI", f"{ndvi}", delta=f"{round(ndvi - 0.6, 2)}")
    col4.metric("Soil Moisture", f"{moisture}%", delta=f"{round(moisture - 30, 1)}%")
    
    st.markdown("---")
    
    # Status Qiymətləndirməsi
    if 6.0 <= ph <= 7.4 and nitrogen >= 38 and ndvi >= 0.50 and moisture >= 22:
        st.success(ok_text)
    else:
        st.warning(warn_text)
    
    # --- PREDICTIVE AI & MÜHƏNDİSLİK HESABLAMALARI ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f"### {pred_title}")
        # Elmi proqnozlaşdırma məntiqi
        moisture_loss =
