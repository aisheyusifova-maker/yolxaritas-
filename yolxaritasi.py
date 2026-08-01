import folium
import streamlit as st
from streamlit_folium import st_folium

st.title("Azərbaycan Xəritəsi və Rayonlar")

# Xəritəni mərkəzləşdiririk
m = folium.Map(location=[40.4093, 49.8671], zoom_start=7)

# İstədiyin rayonları və koordinatlarını bura əlavə edə bilərsən
rayonlar = {
    "Bakı": [40.4093, 49.8671],
    "Gəncə": [40.6828, 46.3606],
    "Sumqayıt": [40.5897, 49.6686],
    "Şəki": [41.1919, 47.1706],
    "Lənkəran": [38.7548, 48.8505],
}

# Xəritəyə markerlər əlavə edirik
for rayon, koordinat in rayonlar.items():
  folium.Marker(
      location=koordinat,
      popup=rayon,
      tooltip=rayon,
      icon=folium.Icon(color="blue", icon="info-sign"),
  ).add_to(m)

# Xəritəni Streamlit-də göstəririk
st_folium(m, width=700, height=500)
