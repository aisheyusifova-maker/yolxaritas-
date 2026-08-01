import streamlit as st
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Yol Xəritəsi", page_icon="🗺️", layout="wide")

st.markdown("## 🗺️ Yol Xəritəsi")
st.divider()

# Yaddaşda adın olub-olmadığını yoxlayırıq (Yalnız bir dəfə istəyir)
if "qeydiyyat" not in st.session_state:
    st.session_state.qeydiyyat = False

if not st.session_state.qeydiyyat:
    st.markdown("### Zəhmət olmasa daxil olun:")
    giris_ad = st.text_input("Ad və Soyad:", "")
    if st.button("Daxil ol"):
        if giris_ad:
            st.session_state.ad_soyad = giris_ad
            st.session_state.qeydiyyat = True
            st.rerun()
        else:
            st.warning("Ad və soyadınızı daxil edin!")
else:
    # Artıq bir dəfə daxil olub, bir daha ad istəmir!
    st.success(f"Xoş gəldiniz, {st.session_state.ad_soyad}! 👋")
    
    # Şəhərlər, koordinatları (En dairəsi, Uzunluq dairəsi) və Bakıdan kilometrləri
    seherler = {
        "Şəki": {"koordinat": [40.1973, 47.1575], "km": 300},
        "Gəncə": {"koordinat": [40.6828, 46.3606], "km": 365},
        "Quba": {"koordinat": [41.3623, 48.5133], "km": 168},
        "Lənkəran": {"koordinat": [38.7529, 48.8505], "km": 268},
        "Qəbələ": {"koordinat": [40.4839, 47.8441], "km": 220},
        "Şamaxı": {"koordinat": [40.6324, 48.6314], "km": 120}
    }
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📍 Səfər Təfərrüatları")
        secilen_seher = st.selectbox("Hara getmək istəyirsiniz?", list(seherler.keys()))
        cixis_saati = st.time_input("Saat neçədə yola çıxırsınız?", value=datetime.strptime("15:30", "%H:%M").time())
        
        if st.button("🚀 Davam et (Hesabla)"):
            st.session_state.hesablandi = True
            st.session_state.secilen = secilen_seher
            st.session_state.saat = cixis_saati

    # Xəritənin yaradılması (Bakı mərkəzli)
    baki_koordinat = [40.4093, 49.8671]
    m_xeri = folium.Map(location=baki_koordinat, zoom_start=7)
    
    # Bakı nöqtəsi
    folium.Marker(
        baki_koordinat,
        popup="Başlanğıc: Bakı",
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m_xeri)

    # Əgər düyməyə basılıbsa, seçilən şəhəri xəritədə göstəririk
    if "hesablandi" in st.session_state and st.session_state.hesablandi:
        hedef = st.session_state.secilen
        hedef_data = seherler[hedef]
        
        # Hedef nöqtəsi
        folium.Marker(
            hedef_data["koordinat"],
            popup=f"İstiqamət: {hedef} ({hedef_data['km']} km)",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(m_xeri)
        
        # Xətt çəkirik Bakıdan həmin şəhərə
        folium.PolyLine(
            [baki_koordinat, hedef_data["koordinat"]],
            color="green",
            weight=4,
            opacity=0.7
        ).add_to(m_xeri)

    with col2:
        st.markdown("### 🗺️ Canlı Xəritə")
        st_folium(m_xeri, width=500, height=400)

    # Hesablama nəticəsi aşağıda görünür
    if "hesablandi" in st.session_state and st.session_state.hesablandi:
        hedef = st.session_state.secilen
        mesafe = seherler[hedef]["km"]
        c_saat = st.session_state.saat
        
        # Orta sürət 80 km/saat
        suret_saat = mesafe / 80
        saat_int = int(suret_saat)
        deqiqe_int = int((suret_saat - saat_int) * 60)
        
        cixis_dt = datetime.combine(datetime.today(), c_saat)
        catilma_dt = cixis_dt + timedelta(hours=saat_int, minutes=deqiqe_int)
        catilma_str = catilma_dt.strftime("%H:%M")
        
        st.divider()
        st.markdown("### 📊 Nəticə və Hesabat")
        st.info(f"📍 **İstiqamət:** Bakı ➔ {hedef}")
        st.info(f"📏 **Məsafə:** {mesafe} kilometr")
        st.info(f"⏰ **Çıxış vaxtı:** {c_saat.strftime('%H:%M')}")
        st.success(f"🏁 **Çatılma vaxtı:** Saat **{catilma_str}**-də orada olacaqsınız! (Təxmini yol müddəti: {saat_int} saat {deqiqe_int} dəqiqə)")