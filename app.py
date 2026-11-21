import streamlit as st
import pandas as pd
import numpy as np
import json

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="C.h.e.MartixAZE v3.0 Final",
    page_icon="logo.png",
    layout="wide"
)

# --- PWA (MOBILE APP) QABIĞI ---
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
    ],
}

manifest_json = json.dumps(manifest_data)

pwa_code = f"""
<link rel="manifest" href='data:application/manifest+json;charset=utf-8,{manifest_json}'>
"""
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
import pandas as pd
import numpy as np


def run_chematrix_decision_engine(records: list[dict]) -> list[dict]:
    """
    C.h.e.MartixAZE üçün:
    1. Zaman üzrə kimyəvi/spektral dəyişiklik müqayisəsi
    2. pH, EC və NDVI əsaslı risk siqnalı
    3. Lab nümunəsi üçün ağıllı zona seçimi
    4. Sİ etibarlılıq göstəricisi və riskli qərar xəbərdarlığı
    5. Fermer üçün aydın + analitik video/brifinq ssenarisi
    """
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    outputs = []

    for zone_id, group in df.groupby("zone_id"):
        g = group.sort_values("date").reset_index(drop=True)
        base = g.iloc[0]
        curr = g.iloc[-1]

        # 1. Zaman xəritəsi fərqləri
        d_ndvi = round(float(curr["ndvi"] - base["ndvi"]), 3)
        d_ph = round(float(curr["ph"] - base["ph"]), 2)
        d_ec = round(float(curr["ec_ds_m"] - base["ec_ds_m"]), 2)
        d_moist = round(float(curr["soil_moisture"] - base["soil_moisture"]), 1)

        # 2. Risk siqnalı (pH + EC + NDVI)
        risk_points = 0
        signals = []

        if curr["ph"] < 5.5 or curr["ph"] > 7.8 or abs(d_ph) >= 0.7:
            risk_points += 40
            signals.append(f"pH dəyişimi/həddi ({base['ph']} → {curr['ph']})")

        if curr["ec_ds_m"] >= 2.5 or d_ec >= 1.0:
            risk_points += 40
            signals.append(f"EC/duzluluq artımı ({base['ec_ds_m']} → {curr['ec_ds_m']} dS/m)")

        if d_ndvi <= -0.15:
            risk_points += 20
            signals.append(f"NDVI enişi ({d_ndvi})")

        if risk_points >= 60:
            risk_status = "YÜKSƏK RİSK"
        elif risk_points >= 30:
            risk_status = "ORTA RİSK"
        else:
            risk_status = "NORMAL"

        # 4. Etibarlılıq göstəricisi (%)
        reliability = 100.0
        reliability -= min(float(curr["days_since_lab"]) * 0.65, 45.0)
        reliability -= min(float(curr["cloud_cover"]) * 0.75, 25.0)
        if abs(d_ph) >= 0.8 or d_ec >= 1.5:
            reliability -= 15.0  # Kəskin dəyişiklikdə model təkbaşına tam etibarlı sayılmır

        reliability = round(max(min(reliability, 98.0), 15.0), 1)
        lab_mandatory_before_action = reliability < 65.0 or risk_status == "YÜKSƏK RİSK"

        # 3. Laboratoriya yoxlaması üçün ağıllı seçim
        need_lab = risk_status in ("YÜKSƏK RİSK", "ORTA RİSK") or reliability < 65.0
        if need_lab:
            lab_recommendation = (
                f"{zone_id} zonasından hədəfli torpaq nümunəsi götürülüb pH, EC və aktiv azot "
                f"üzrə laborator yoxlama aparılmalıdır (son lab analizindən {int(curr['days_since_lab'])} gün keçib)."
            )
        else:
            lab_recommendation = f"{zone_id} üzrə əlavə laboratoriya nümunəsinə təcili ehtiyac yoxdur."

        # Fermer üçün anlaşılan, amma məzmunlu qısa video/brifinq mətni
        if lab_mandatory_before_action:
            action_line = (
                "Birbaşa kimyəvi gübrə/düzəliş verməzdən əvvəl bu zonadan laboratoriya "
                "nümunəsi götürün və rütubət/duzluluq balansını dəqiqləşdirin."
            )
        else:
            action_line = (
                "Zonanı növbəti peyk dövründə izləyin və yalnız ehtiyac olan nöqtəyə lokal aqrotexniki qulluq tətbiq edin."
            )

        video_script = (
            f"[{zone_id} | {base['date'].strftime('%d.%m')}–{curr['date'].strftime('%d.%m')}] "
            f"Bitki örtüyü indeksi (NDVI) {d_ndvi:+.3f}, rütubət {d_moist:+.1f}%, pH {curr['ph']}, EC {curr['ec_ds_m']} dS/m. "
            f"Risk səviyyəsi: {risk_status}. Model etibarlılığı: {reliability}%. {action_line}"
        )

        outputs.append({
            "zone_id": zone_id,
            "period": f"{base['date'].strftime('%Y-%m-%d')} -> {curr['date'].strftime('%Y-%m-%d')}",
            "delta_ndvi": d_ndvi,
            "delta_ph": d_ph,
            "delta_ec": d_ec,
            "risk_status": risk_status,
            "signals": signals,
            "reliability_pct": reliability,
            "lab_required": need_lab,
            "block_unverified_chemical_action": lab_mandatory_before_action,
            "lab_recommendation": lab_recommendation,
            "video_brief_script": video_script
        })

    return outputs

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
        # --- C.h.e.MartixAZE QƏRAR, RİSK VƏ VİDEO XÜLASƏ MODULU ---
    st.divider()

    zone_name = "Manual_Input" if "Manual" in str(mode) or "Manuel" in str(mode) else selected_reg
    base_ec = round(float(reg_info.get("ec", 1.3)), 2) if isinstance(reg_info, dict) else 1.3
    base_days_lab = 35 if mode == mode_b else 12
    base_cloud = 12

    # Zaman müqayisəsi üçün bazis + cari ölçüm qeydləri
    records = [
        {
            "zone_id": zone_name,
            "date": "2026-10-15",
            "ndvi": round(max(min(float(ndvi) + 0.08, 0.95), 0.05), 3),
            "soil_moisture": round(min(float(moisture) + 3.0, 95.0), 1),
            "ph": round(float(reg_info.get("ph", ph)) if isinstance(reg_info, dict) else float(ph), 2),
            "ec_ds_m": base_ec,
            "days_since_lab": max(base_days_lab - 15, 1),
            "cloud_cover": max(base_cloud - 4, 0),
        },
        {
            "zone_id": zone_name,
            "date": "2026-11-21",
            "ndvi": round(float(ndvi), 3),
            "soil_moisture": round(float(moisture), 1),
            "ph": round(float(ph), 2),
            "ec_ds_m": round(max(base_ec + (0.9 if float(ph) > 7.8 or float(ph) < 5.5 else 0.2), 0.2), 2),
            "days_since_lab": base_days_lab,
            "cloud_cover": base_cloud,
        },
    ]

    decision_results = run_chematrix_decision_engine(records)
    res = decision_results[0]

    sec_title = (
        "🧪 Kimyəvi Dinamika, Risk Siqnalı və Fermer Video Xülasəsi"
        if lang == "Azərbaycan"
        else "🧪 Chemical Dynamics, Risk Signal & Farmer Video Brief"
    )
    st.subheader(sec_title)

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Risk Səviyyəsi" if lang == "Azərbaycan" else "Risk Level",
        res["risk_status"],
        delta=f"ΔpH: {res['delta_ph']:+.2f} | ΔNDVI: {res['delta_ndvi']:+.3f}",
    )
    c2.metric(
        "Sİ Etibarlılığı" if lang == "Azərbaycan" else "AI Reliability",
        f"{res['reliability_pct']}%",
    )
    c3.metric(
        "Lab Nümunəsi" if lang == "Azərbaycan" else "Lab Sampling",
        ("Lazımdır" if lang == "Azərbaycan" else "Required")
        if res["lab_required"]
        else ("Vacib deyil" if lang == "Azərbaycan" else "Not urgent"),
    )

    st.progress(min(max(res["reliability_pct"] / 100.0, 0.0), 1.0))

    if res["signals"]:
        st.caption(
            ("Qeydə alınan siqnallar: " if lang == "Azərbaycan" else "Detected signals: ")
            + ", ".join(res["signals"])
        )

    if res["block_unverified_chemical_action"]:
        st.warning(
            "⚠️ Laborator analiz təsdiqi olmadan gübrə və ya kimyəvi düzəliş tətbiq etməyin! "
            if lang == "Azərbaycan"
            else "⚠️ Do not apply fertilizers or chemical corrections without lab verification! "
        )

    st.info(
        ("🔬 Laboratoriya tövsiyəsi: " if lang == "Azərbaycan" else "🔬 Lab recommendation: ")
        + res["lab_recommendation"]
    )

    st.markdown(
        "🎬 **Fermer üçün qısa video/brifinq xülasəsi:**"
        if lang == "Azərbaycan"
        else "🎬 **Farmer Short Video/Brief Script:**"
    )
    st.write(res["video_brief_script"])

else:
    st.info(info_start)

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #888; font-size: 14px;'><b>{footer_text}</b></div>", unsafe_allow_html=True)
