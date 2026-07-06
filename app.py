import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("C2ME_API_URL")
USERNAME = os.getenv("C2ME_USER")

if BASE_URL and USERNAME:
    url = f"{BASE_URL}{USERNAME}"
else:
    print("Hata: C2ME_API_URL veya C2ME_USER environment değişkenleri tanımlanmamış!")
    exit(1)

headers = {}

print(f"Test başlatılıyor... Hedef kullanıcı: {USERNAME}\n")

with requests.Session() as session:
    while True:
        try:
            response = session.get(url, headers=headers)
            
            if "ETag" in response.headers:
                headers["If-None-Match"] = response.headers["ETag"]
            
            if response.status_code == 200:
                print(f"Durum 200: Veri güncel. Yanıt: {response.json()}")
                
            elif response.status_code == 304:
                print("Durum 304: ETag çalışıyor! Veri aynı, trafik tasarrufu yapıldı.")
                
            else:
                print(f"Beklenmedik durum kodu: {response.status_code}")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

        time.sleep(5)
