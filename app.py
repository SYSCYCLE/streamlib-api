import streamlit as st
import requests
import time

try:
    BASE_URL = st.secrets["C2ME_API_URL"]
    USERNAME = st.secrets["C2ME_USER"]
except KeyError:
    st.error("Lütfen Streamlit panelinden 'Secrets' kısmına değişkenleri ekleyin!")
    st.stop()

url = f"{BASE_URL}{USERNAME}"
headers = {}

st.write(f"Test başlatılıyor... Hedef kullanıcı: {USERNAME}")
placeholder = st.empty()

with requests.Session() as session:
    while True:
        try:
            response = session.get(url, headers=headers)
            
            if "ETag" in response.headers:
                headers["If-None-Match"] = response.headers["ETag"]
            
            if response.status_code == 200:
                msg = f"Durum 200: Veri güncel. Yanıt: {response.json()}"
            elif response.status_code == 304:
                msg = "Durum 304: ETag çalışıyor! Veri aynı."
            else:
                msg = f"Beklenmedik durum kodu: {response.status_code}"
            
            placeholder.text(msg)
                
        except Exception as e:
            placeholder.text(f"Bir hata oluştu: {e}")

        time.sleep(5)
