import streamlit as st
import pandas as pd
import numpy as np
import requests

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="C.h.e.MartixAZE v2.0",
    page_icon="🌱",
    layout="wide"
)

# --- DİL SEÇİMİ VƏ TƏRCÜMƏLƏR ---
st.sidebar.title("🌍 Parametrlər / Settings")
lang = st.sidebar.selectbox("Dil / Language", ["Azərbaycan", "English"])

t = {
    "AZ": {
        "title": "🌱 C.h.e.MartixAZE: Süni İntellektlə Torpaq və Ekosistem İdarəetməsi",
        "subtitle": "NASA peyk məlumatları və aqrokimyəvi analiz əsasında qərar qətnetmə paneli.",
        "sidebar_header": "🎛️ Daxil Edilən Parametrlər",
        "mode": "Rejim Seçimi",
        "mode_manual": "Manual Daxiletmə (Sürüşdürücülər)",
        "mode_region": "Rayon / Region Seçimi (Avtomatik NASA/Aqrokimya)",
        "region_select": "Rayon seçin:",
        "ph": "Torpağın pH səviyyəsi",
        "nitrogen": "Azot (N) miqdarı (mq/kg)",
        "ndvi": "NASA Peyk NDVI (Bitki Sağlamlıq İndeksi)",
        "moisture": "Torpağın Rütubəti (%)",
        "btn": " экоsistem Analiz Et və Qərar Çıxar",
        "results": "📊 Süni İntellekt və Aqrokimyəvi Təhlil Nəticələri",
        "status_ok": "✅ Torpaq və ekosistem parametrləri normal səviyyədədir.",
        "status_warn": "⚠️ Diqqət! Torpaqda balanssızlıq aşkar edildi.",
        "rec_title": "💡 Mühəndislik və Gübrələmə Tövsiyələri:",
        "rec_ph": "• pH Tənzimlənməsi: Torpağın turşuluğunu normallaşdırmaq üçün tədbir görülməlidir.",
        "rec_n": "• Azot Təminatı: Bitkinin inkişafı üçün uyğun miqdarda azot gübrəsi (karbamid/ammonium nitrat) əlavə edilməlidir.",
        "rec_water": "• Suvarma Rejimi: NASA peyk rütubət göstəricilərinə əsasən suvarma cədvəli optimallaşdırılmalıdır."
    },
    "EN": {
        "title": "🌱 C.h.e.MartixAZE: AI-Driven Soil & Ecosystem Management",
        "subtitle": "Decision-making dashboard based on NASA satellite data and agrochemical analysis.",
        "sidebar_header": "🎛️ Input Parameters",
        "mode": "Select Mode",
        "mode_manual": "Manual Input (Sliders)",
        "mode_region": "Region Selection (Auto NASA/Agrochemical)",
        "region_select": "Select Region:",
        "ph": "Soil pH Level",
        "nitrogen": "Nitrogen (N) Content (mg/kg)",
        "ndvi": "NASA Satellite NDVI (Vegetation Health Index)",
        "moisture": "Soil Moisture (%)",
        "btn": "🔍 Analyze Ecosystem & Decision",
        "results": "📊 AI & Agrochemical Analysis Results",
        "status_ok": "✅ Soil and ecosystem parameters are at normal levels.",
        "status_warn": "⚠️ Warning! Imbalance detected in the soil.",
        "rec_title": "💡 Engineering & Fertilization Recommendations:",
        "rec_ph": "• pH Adjustment: Measures should be taken to normalize soil acidity.",
        "rec_n": "• Nitrogen Supply: Appropriate amount of nitrogen fertilizer should be applied.",
        "rec_water": "• Irrigation Regime: Irrigation schedule should be optimized based on NASA satellite moisture metrics."
    }
}

# Seçilmiş dilə uyğun lüğət
d = t[lang]

# Əsas başlıqlar
st.title(d["title"])
st.write(d["subtitle"])
st.markdown("---")

# --- SOL PANEL (Daxiletmələr) ---
st.sidebar.header(d["sidebar_header"])
mode = st.sidebar.radio(d["mode"], [d["mode_manual"], d["mode_region"]])

# Rayonlar üzrə bazalar (Ön təyinli dəyərlər)
regions_data = {
    "Oğuz (Dağ-meşə qəhvəyi torpaqlar)": {"ph": 6.2, "n": 48.0, "ndvi": 0.74, "moisture": 35.0},
    "Baku / Abşeron (Boz-qonur torpaqlar)": {"ph": 7.8, "n": 22.0, "ndvi": 0.31, "moisture": 15.0},
    "Gəncə-Qazax (Şabalıdı torpaqlar)": {"ph": 7.1, "n": 38.0, "ndvi": 0.58, "moisture": 25.0},
    "Aran Bölgəsi / Mərkəz (Çəmən-boz torpaqlar)": {"ph": 7.5, "n": 30.0, "ndvi": 0.45, "moisture": 20.0}
}

if mode == d["mode_region"]:
    selected_reg = st.sidebar.selectbox(d["region_select"], list(regions_data.keys()))
    reg_vals = regions_data[selected_reg]
    
    ph = reg_vals["ph"]
    nitrogen = reg_vals["n"]
    ndvi = reg_vals["ndvi"]
    moisture = reg_vals["moisture"]
    
    st.sidebar.info(f"📍 Seçilən bölgə üçün avtomatik yüklənən baza dəyərləri tətbiq olundu.")
else:
    ph = st.sidebar.slider(d["ph"], 4.0, 10.0, 6.5)
    nitrogen = st.sidebar.slider(d["nitrogen"], 10.0, 100.0, 45.0)
    ndvi = st.sidebar.slider(d["ndvi"], 0.0, 1.0, 0.65)
    moisture = st.sidebar.slider(d["moisture"], 5.0, 60.0, 28.0)

# Analiz düyməsi
if st.sidebar.button(d["btn"], type="primary"):
    st.subheader(d["results"])
    
    # Metriklər panel şəklində
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("pH Level", f"{ph}")
    col2.metric("Nitrogen (N)", f"{nitrogen} mg/kg")
    col3.metric("NDVI", f"{ndvi}")
    col4.metric("Moisture", f"{moisture}%")
    
    st.markdown("---")
    
    # Süni intellekt qərar mühərriki məntiqi
    if 6.0 <= ph <= 7.5 and nitrogen >= 40 and ndvi >= 0.5:
        st.success(d["status_ok"])
    else:
        st.warning(d["status_warn"])
        
    st.markdown(f"### {d['rec_title']}")
    st.write(d["rec_ph"])
    st.write(d["rec_n"])
    st.write(d["rec_water"])
    
    # Kiçik vizual qrafik əlavəsi
    chart_data = pd.DataFrame({
        "Parametr": ["pH (x10)", "Azot (N)", "NDVI (x100)", "Rütubət"],
        "Dəyər": [ph * 10, nitrogen, ndvi * 100, moisture]
    })
    st.bar_chart(chart_data.set_index("Parametr"))
else:
    st.info("👈 Zəhmət olmasa parametrləri təyin edib **'Analiz Et və Qərar Çıxar'** düyməsinə basın.")
