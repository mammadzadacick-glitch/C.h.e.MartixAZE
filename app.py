import streamlit as st
import pandas as pd

# Səhifənin başlığı və dizaynı
st.title("🌱 C.h.e.MartixAZE: Süni İntellektlə Torpaq və Ekosistem İdarəetməsi")
st.write("NASA peyk məlumatları və torpaq kimyası analizi əsasında qərar qəbuletmə paneli.")

st.sidebar.header("🎛️ Daxil Edilən Parametrlər")

# İstifadəçinin daxil edəcəyi göstəricilər (Simulyasiya üçün sürgülər)
ph_level = st.sidebar.slider("Torpağın pH səviyyəsi", 3.0, 10.0, 6.5)
nitrogen = st.sidebar.slider("Azot (N) miqdarı (mq/kg)", 0, 100, 45)
ndvi_score = st.sidebar.slider("NASA Peyk NDVI (Bitki Sağlamlıq İndeksi)", 0.0, 1.0, 0.6)
moisture = st.sidebar.slider("Torpağın Rütubəti (%)", 0, 100, 30)

st.divider()

# Analiz düyməsi
if st.button("🚀 Ekosistemi Analiz Et və Qərar Çıxar"):
    st.subheader("📊 Analiz Nəticələri və Süni İntellekt Tövsiyələri")

    # Suvarmaq lazımdırmı?
    if moisture < 35:
        water_needed = (35 - moisture) * 12  # litr/kv.m
        st.error(f"⚠️ **Suvarma Xəbərdarlığı:** Torpaq qurudur! Təcili olaraq hər kvadrat metrə təqribən **{water_needed:.1f} litr** su verilməlidir.")
    else:
        st.success("✅ **Su Səviyyəsi:** Optimaldır. Əlavə suvarmaya ehtiyac yoxdur.")

    # Torpaq kimyası və Gübrə analizi
    if ph_level < 5.5:
        st.warning("⚠️ **Torpaq Turşuluğu yüksəkdir (Turş torpaq):** pH səviyyəsini tənzimləmək üçün əhəngləmə tövsiyə olunur.")
    elif ph_level > 7.5:
        st.warning("⚠️ **Torpaq Qələvidir:** pH səviyyəsini aşağı salmaq üçün müvafiq üzvi əlavələr lazımdır.")
    else:
        st.info("✅ **pH Balansı:** Normal diapazondadır.")

    # Azot və Bitki sağlamlığı (NASA NDVI əlaqəsi)
    if nitrogen < 40 or ndvi_score < 0.4:
        st.error("🧪 **Qida Çatışmazlığı:** Peyk görüntüləri (NDVI) və torpaq analizi bitki inkişafının zəiflədiyini göstərir. **Azot tərkibli gübrə** tətbiqi vacibdir.")
    else:
        st.success("🌿 **Bitki Örtüyü Sağlamlığı:** NASA peyk datalarına əsasən sahənin vegetasiya indeksi stabildir.")

    # Yekun xülasə cədvəli
    summary_data = {
        "Parametr": ["pH Səviyyəsi", "Azot (mq/kg)", "NASA NDVI", "Rütubət (%)"],
        "Göstərici": [ph_level, nitrogen, ndvi_score, moisture],
        "Status": [
            "Normal" if 5.5 <= ph_level <= 7.5 else "Diqqət",
            "Normal" if nitrogen >= 40 else "Aşağı",
            "Yaxşı" if ndvi_score >= 0.4 else "Zəif",
            "Stabil" if moisture >= 35 else "Kritik"
        ]
    }

    st.table(pd.DataFrame(summary_data))
else:
    st.info("💡 Parametrləri tənzimlədikdən sonra **'Ekosistemi Analiz Et və Qərar Çıxar'** düyməsini sıxın.")
