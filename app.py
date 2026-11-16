import streamlit as st
import pandas as pd
import numpy as np

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="C.h.e.MartixAZE v2.0",
    page_icon="🌱",
    layout="wide"
)

# --- DİL SEÇİMİ ---
st.sidebar.title("🌍 Parametrlər / Settings")
lang = st.sidebar.selectbox("Dil / Language", ["Azərbaycan", "English"])

# --- TƏRCÜMƏLƏR ---
if lang == "Azərbaycan":
    title_text = "🌱 C.h.e.MartixAZE: Süni İntellektlə Torpaq və Ekosistem İdarəetməsi"
    subtitle_text = "NASA peyk məlumatları və aqrokimyəvi analiz əsasında qərar qəbuletmə paneli."
    sidebar_title = "🎛️ Daxil Edilən Parametrlər"
    mode_label = "Rejim Seçimi"
    mode_m = "Manual Daxiletmə (Sürüşdürücülər)"
    mode_r = "Rayon / Region Seçimi (Avtomatik)"
    reg_select_label = "Rayon seçin:"
    ph_label = "Torpağın pH səviyyəsi"
    n_label = "Azot (N) miqdarı (mq/kg)"
    ndvi_label = "NASA Peyk NDVI (Bitki Sağlamlıq İndeksi)"
    moist_label = "Torpağın Rütubəti (%)"
    btn_label = "🔍 Ekosistem Analiz Et və Qərar Çıxar"
    res_title = "📊 Süni İntellekt və Aqrokimyəvi Təhlil Nəticələri"
    ok_text = "✅ Torpaq və ekosistem parametrləri normal səviyyədədir."
    warn_text = "⚠️ Diqqət! Torpaqda balanssızlıq aşkar edildi."
    rec_heading = "💡 Mühəndislik və Gübrələmə Tövsiyələri:"
    rec_p = "• pH Tənzimlənməsi: Torpağın turşuluğunu normallaşdırmaq üçün tədbir görülməlidir."
    rec_nitrogen = "• Azot Təminatı: Bitkinin inkişafı üçün uyğun miqdarda azot gübrəsi əlavə edilməlidir."
    rec_w = "• Suvarma Rejimi: NASA peyk rütubət göstəricilərinə əsasən suvarma cədvəli optimallaşdırılmalıdır."
    info_reg = "📍 Seçilən bölgə üçün avtomatik yüklənən baza dəyərləri tətbiq olundu."
    info_start = "👈 Zəhmət olmasa parametrləri təyin edib düyməyə basın."
else:
    title_text = "🌱 C.h.e.MartixAZE: AI-Driven Soil & Ecosystem Management"
    subtitle_text = "Decision-making dashboard based on NASA satellite data and agrochemical analysis."
    sidebar_title = "🎛️ Input Parameters"
    mode_label = "Select Mode"
    mode_m = "Manual Input (Sliders)"
    mode_r = "Region Selection (Auto NASA/Agrochemical)"
    reg_select_label = "Select Region:"
    ph_label = "Soil pH Level"
    n_label = "Nitrogen (N) Content (mg/kg)"
    ndvi_label = "NASA Satellite NDVI (Vegetation Health Index)"
    moist_label = "Soil Moisture (%)"
    btn_label = "🔍 Analyze Ecosystem & Decision"
    res_title = "📊 AI & Agrochemical Analysis Results"
    ok_text = "✅ Soil and ecosystem parameters are at normal levels."
    warn_text = "⚠️ Warning! Imbalance detected in the soil."
    rec_heading = "💡 Engineering & Fertilization Recommendations:"
    rec_p = "• pH Adjustment: Measures should be taken to normalize soil acidity."
    rec_nitrogen = "• Nitrogen Supply: Appropriate amount of nitrogen fertilizer should be applied."
    rec_w = "• Irrigation Regime: Irrigation schedule should be optimized based on NASA satellite moisture metrics."
    info_reg = "📍 Automatic baseline values loaded for the selected region."
    info_start = "👈 Please set the parameters and click the button."

st.title(title_text)
st.write(subtitle_text)
st.markdown("---")

st.sidebar.header(sidebar_title)
mode = st.sidebar.radio(mode_label, [mode_m, mode_r])

regions_data = {
    "Oğuz (Dağ-meşə qəhvəyi torpaqlar)": {"ph": 6.2, "n": 48.0, "ndvi": 0.74, "moisture": 35.0},
    "Baku / Abşeron (Boz-qonur torpaqlar)": {"ph": 7.8, "n": 22.0, "ndvi": 0.31, "moisture": 15.0},
    "Gəncə-Qazax (Şabalıdı torpaqlar)": {"ph": 7.1, "n": 38.0, "ndvi": 0.58, "moisture": 25.0},
    "Aran Bölgəsi / Mərkəz (Çəmən-boz torpaqlar)": {"ph": 7.5, "n": 30.0, "ndvi": 0.45, "moisture": 20.0}
}

if mode == mode_r:
    selected_reg = st.sidebar.selectbox(reg_select_label, list(regions_data.keys()))
    reg_vals = regions_data[selected_reg]
    
    ph = reg_vals["ph"]
    nitrogen = reg_vals["n"]
    ndvi = reg_vals["ndvi"]
    moisture = reg_vals["moisture"]
    
    st.sidebar.info(info_reg)
else:
    ph = st.sidebar.slider(ph_label, 4.0, 10.0, 6.5)
    nitrogen = st.sidebar.slider(n_label, 10.0, 100.0, 45.0)
    ndvi = st.sidebar.slider(ndvi_label, 0.0, 1.0, 0.65)
    moisture = st.sidebar.slider(moist_label, 5.0, 60.0, 28.0)

if st.sidebar.button(btn_label, type="primary"):
    st.subheader(res_title)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("pH Level", f"{ph}")
    col2.metric("Nitrogen (N)", f"{nitrogen} mg/kg")
    col3.metric("NDVI", f"{ndvi}")
    col4.metric("Moisture", f"{moisture}%")
    
    st.markdown("---")
    
    if 6.0 <= ph <= 7.5 and nitrogen >= 40 and ndvi >= 0.5:
        st.success(ok_text)
    else:
        st.warning(warn_text)
        
    st.markdown(f"### {rec_heading}")
    st.write(rec_p)
    st.write(rec_nitrogen)
    st.write(rec_w)
    
    chart_data = pd.DataFrame({
        "Parametr": ["pH (x10)", "Azot (N)", "NDVI (x100)", "Rütubət"],
        "Dəyər": [ph * 10, nitrogen, ndvi * 100, moisture]
    })
    st.bar_chart(chart_data.set_index("Parametr"))
else:
    st.info(info_start)
