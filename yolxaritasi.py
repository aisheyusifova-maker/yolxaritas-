from datetime import datetime, timedelta
import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Canlı Yol Xəritəsi və Məsafə Təyini", layout="wide"
)

st.title("🚗 İnteraktiv Yol Xəritəsi Planlayıcısı")
st.markdown("Xoş gəlmisiniz! Səfərinizi planlaşdırmaq üçün məlumatları daxil edin.")

# 1. İstifadəçidən ad və soyad istəyirik
ad_soyad = st.text_input("Zəhmət olmasa, Ad və Soyadınızı daxil edin:")

if ad_soyad:
  st.success(
      f"Xoş gəldiniz, **{ad_soyad}**! Zəhmət olmasa səfər məlumatlarını qeyd"
      " edin."
  )

  # Rayonlar və təxmini koordinatları ilə Bakıdan məsafələr (km) və orta sürət (saat) üçün baza
  rayon_verilenleri = {
      "Gəncə": {"lat": 40.6828, "lon": 46.3606, "km": 365, "suret": 4.5},
      "Sumqayıt": {"lat": 40.5897, "lon": 49.6686, "km": 40, "suret": 0.8},
      "Şəki": {"lat": 41.1919, "lon": 47.1706, "km": 300, "suret": 4.0},
      "Lənkəran": {"lat": 38.7548, "lon": 48.8505, "km": 270, "suret": 3.5},
      "Quba": {"lat": 41.3617, "lon": 48.5121, "km": 168, "suret": 2.2},
      "Mingəçevir": {"lat": 40.7652, "lon": 47.0503, "km": 280, "suret": 3.5},
      "Naxçıvan": {"lat": 39.2088, "lon": 45.4122, "km": 450, "suret": 1.0},  # təyyarə/şərti
  }

  col1, col2 = st.columns(2)

  with col1:
    secilen_yer = st.selectbox(
        "Getmək istədiyiniz Şəhər / Rayon:", list(rayon_verilenleri.keys())
    )

  with col2:
    yola_cixis_saati = st.time_input(
        "Yola çıxacağınız saat:", datetime.now().time()
    )

  if st.button("Davam et (Hesabla)"):
    info = rayon_verilenleri[secilen_yer]

    # Hesablamalar
    mesafe_km = info["km"]
    tahmini_sure_saat = info["suret"]

    # Çatma saatını hesablamaq
    bugun = datetime.now().date()
    cixis_dt = datetime.combine(bugun, yola_cixis_saati)
    varis_dt = cixis_dt + timedelta(hours=tahmini_sure_saat)
    varis_saati_str = varis_dt.strftime("%H:%M")

    # Nəticələrin ekranda göstərilməsi
    st.markdown("---")
    st.subheader(f"📍 Səfər Təfərrüatları: {secilen_yer}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Məsafə", f"{mesafe_km} km")
    m2.metric("Təxmini Müddət", f"{tahmini_sure_saat} saat")
    m3.metric("Çatma Saatı", f"{varis_saati_str}")

    # Canlı Xəritə (Folium)
    st.markdown("### 🗺️ Canlı Xəritə Görüntüsü")
    m = folium.Map(location=[info["lat"], info["lon"]], zoom_start=8)

    # Başlanğıc nöqtəsi (Bakı)
    folium.Marker(
        [40.4093, 49.8671],
        popup="Başlanğıc: Bakı",
        tooltip="Bakı",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(m)

    # Təyinat nöqtəsi
    folium.Marker(
        [info["lat"], info["lon"]],
        popup=f"Təyinat: {secilen_yer}\nÇatma saatı: {varis_saati_str}",
        tooltip=secilen_yer,
        icon=folium.Icon(color="red", icon="stop"),
    ).add_to(m)

    # Xətt çəkmək üçün
    folium.PolyLine(
        [[40.4093, 49.8671], [info["lat"], info["lon"]]],
        color="blue",
        weight=2.5,
        opacity=0.8,
    ).add_to(m)

    st_folium(m, width=800, height=450)
