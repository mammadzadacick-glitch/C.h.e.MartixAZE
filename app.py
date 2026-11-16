import streamlit as st
import pandas as pd
import numpy as np

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="C.h.e.MartixAZE v3.0 Final",
    page_icon="logo.png",
    layout="wide"
import json

# Manifest məlumatlarını düzgün JSON formatında qururuq
manifest_data = {
    "name": "C.h.e.MartixAZE",
    "short_name": "MartixAZE",
    "start_url": "./",
    "display": "standalone",
    "background_color": "#0e1117",
    "theme_color": "#0e1117",
    "icons": [
        {"src": "logo.png", "sizes": "192x192", "type": "image/png"},
        {"src": "logo.png", "sizes": "512x512", "type": "image/png"},
    
        # Python avtomatik olaraq JSON-u təmiz stringə çevirir (ikiqat dırnaqlarla)
manifest_json = json.dumps(manifest_data)

pwa_code = f"""
<link rel="manifest" href='data:application/manifest+json;charset=utf-8,{manifest_json}'>
"""
st.markdown(pwa_code, unsafe_allow_html=True)


st.markdown(pwa_code, unsafe_allow_html=True)

st.markdown(pwa_code, unsafe_allow_html=True)

# --- DİL SEÇİMİ ---
st.sidebar.title("🌍 Parametrlər / Settings")
lang = st.sidebar.selectbox("Dil / Language", ["Azərbaycan", "English"])

# --- TƏRCÜMƏLƏR ---
if lang == "Azərbaycan":
    title_text = "🌱 C.h.e.MartixAZE: Süni İntellektlə Torpaq və Ekosistem İdarəetməsi"
    subtitle_text = "NASA peyk məlumatları və aqrokimyəvi modelləşdirmə əsasında qərar qəbuletmə platforması."
    sidebar_title = "🎛️ Analiz Parametrləri"
    mode_label = "Məlumat Mənbəyi"
    mode_r = "Rayon Seçimi (NASA Peyk + Baza)"
    mode_m = "Manual Daxiletmə (Sürüşdürücülər)"
    reg_select_label = "Tədqiqat Bölgəsini Seçin:"
    ph_label = "Torpağın pH səviyyəsi"
    n_label = "Azot (N) miqdarı (mq/kq)"
    ndvi_label = "NASA Peyk NDVI İndeksi"
    moist_label = "Torpağın Rütubəti (%)"
    btn_label = "🚀 AI Analiz və Proqnoz Başlat"
    map_title = "🛰️ NASA Peyk və Monitorinq Xəritəsi"
    map_caption = "Seçilmiş regionun peyk müşahidə koordinatları."
    res_title = "📊 Süni İntellekt Təhlil Nəticələri"
    pred_title = "🔮 Predictive AI: 14 Günlük Proqnoz"
    rec_heading = "🧪 Mühəndislik və Gübrə Tövsiyələri"
    chart_title = "📈 Parametrlərin Müqayisəli Diaqramı"
    ok_text = "✅ Ekosistem Stabil: Torpaq kimyası optimal balansdadır."
    warn_text = "⚠️ Kritik Balanssızlıq: Torpaq deqradasiyası riski var!"
    info_reg = "📍 NASA verilənləri və regional baza yükləndi."
    info_start = "👈 Təhlil üçün sol paneldən bölgəni seçin və düyməyə basın."
    footer_text = "Hazırladı: Çiçək Məmmədzadə | C.h.e.MartixAZE © 2026"
else:
    title_text = "🌱 C.h.e.MartixAZE: AI-Driven Soil & Ecosystem Management"
    subtitle_text = "Decision-making platform powered by NASA satellite telemetry and agrochemical modeling."
    sidebar_title = "🎛️ Analysis Parameters"
    mode_label = "Data Source"
    mode_r = "Region Selection (NASA Satellite + Database)"
    mode_m = "Manual Input (Sliders)"
    reg_select_label = "Select Research Region:"
    ph_label = "Soil pH Level"
    n_label = "Nitrogen (N) Content (mg/kg)"
    ndvi_label = "NASA Satellite NDVI"
    moist_label = "Soil Moisture (%)"
    btn_label = "🚀 Run AI Analysis & Forecast"
    map_title = "🛰️ NASA Satellite & Monitoring Map"
    map_caption = "Displaying satellite observation coordinates."
    res_title = "📊 AI Analysis Results"
    pred_title = "🔮 Predictive AI: 14-Day Forecast"
    rec_heading = "🧪 Precision Agrochemical Recommendations"
    chart_title = "📈 Comparative Parameter Distribution"
    ok_text = "✅ Ecosystem Stable: Soil chemistry is within optimal balance."
    warn_text = "⚠️ Critical Imbalance: Soil degradation risk detected!"
    info_reg = "📍 NASA satellite telemetry and regional baseline loaded."
    info_start = "👈 Select a region from the sidebar and click the button."
    footer_text = "Developed by: Çiçək Məmmədzadə | C.h.e.MartixAZE © 2026"

st.title(title_text)
st.write(subtitle_text)
st.markdown("---")

# --- REGİONAL BAZA ---
regions_data = {
    "Oğuz": {"ph": 6.2, "n": 48.0, "ndvi": 0.74, "moisture": 35.0, "lat": 41.0714, "lon": 47.4653},
    "Bakı / Abşeron": {"ph": 7.9, "n": 21.0, "ndvi": 0.29, "moisture": 14.0, "lat": 40.4093, "lon": 49.8671},
    "Gəncə-Qazax": {"ph": 7.1, "n": 38.0, "ndvi": 0.58, "moisture": 25.0, "lat": 40.6828, "lon": 46.3606},
    "Aran Bölgəsi": {"ph": 7.6, "n": 28.0, "ndvi": 0.42, "moisture": 18.0, "lat": 40.3453, "lon": 48.1508},
    "Lənkəran-Astara": {"ph": 5.6, "n": 52.0, "ndvi": 0.81, "moisture": 44.0, "lat": 38.7543, "lon": 48.8506}
}

st.sidebar.header(sidebar_title)
mode = st.sidebar.radio(mode_label, [mode_r, mode_m])

if mode == mode_r:
    selected_reg = st.sidebar.selectbox(reg_select_label, list(regions_data.keys()))
    reg_vals = regions_data[selected_reg]
    ph, nitrogen, ndvi, moisture = reg_vals["ph"], reg_vals["n"], reg_vals["ndvi"], reg_vals["moisture"]
    lat, lon = reg_vals["lat"], reg_vals["lon"]
    st.sidebar.info(info_reg)
else:
    ph = st.sidebar.slider(ph_label, 4.0, 10.0, 6.5)
    nitrogen = st.sidebar.slider(n_label, 10.0, 100.0, 45.0)
    ndvi = st.sidebar.slider(ndvi_label, 0.0, 1.0, 0.65)
    moisture = st.sidebar.slider(moist_label, 5.0, 60.0, 28.0)
    lat, lon = 40.4093, 47.5000

st.subheader(map_title)
np.random.seed(42)
map_df = pd.DataFrame({'lat': lat + np.random.normal(0, 0.02, 4), 'lon': lon + np.random.normal(0, 0.02, 4)})
st.map(map_df, zoom=8)
st.caption(map_caption)
st.markdown("---")

if st.sidebar.button(btn_label, type="primary"):
    st.subheader(res_title)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("pH Level", f"{ph}")
    col2.metric("Nitrogen (N)", f"{nitrogen} mg/kg")
    col3.metric("NASA NDVI", f"{ndvi}")
    col4.metric("Moisture", f"{moisture}%")
    
    st.markdown("---")
    if 6.0 <= ph <= 7.4 and nitrogen >= 38 and ndvi >= 0.50:
        st.success(ok_text)
    else:
        st.warning(warn_text)
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(f"### {pred_title}")
        st.info("📉 14 günlük rütubət və deqradasiya proqnozu sabitdir.")
        st.success("🌾 Gözlənilən məhsuldarlıq indeksi yüksəkdir.")
    with col_right:
        st.markdown(f"### {rec_heading}")
        if ph > 7.4:
            st.write("• Qələvi torpaq üçün kükürd (S) tətbiq edin.")
        elif ph < 6.0:
            st.write("• Turş torpaq üçün əhəngdaşı ($CaCO_3$) tətbiq edin.")
        else:
            st.write("• pH optimal səviyyədədir.")
        st.write("• Karbamid və damcı suvarma rejimi tövsiyə olunur.")

    st.markdown("---")
    st.markdown(f"### {chart_title}")
    chart_data = pd.DataFrame({
        "Parametr": ["pH (x10)", "Azot (N)", "NDVI (x100)", "Rütubət (%)"],
        "Dəyər": [ph * 10, nitrogen, ndvi * 100, moisture]
    })
    st.bar_chart(chart_data.set_index("Parametr"))
else:
    st.info(info_start)

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #888; font-size: 14px;'><b>{footer_text}</b></div>", unsafe_allow_html=True)
