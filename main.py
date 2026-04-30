import requests
import time
import os

# --- AYARLAR ---
# API Key'inizi Render Dashboard -> Environment Variables kısmına eklemeniz güvenli olandır.
# Veya direkt buraya tırnak içine yazabilirsiniz.
K = os.getenv("RAPIDAPI_KEY", "BURAYA_API_KEY_YAZIN") 
HOST = "api-football-v1.p.rapidapi.com"
URL = "https://rapidapi.com"

# Hafıza: Fonksiyon dışında olmalı ki her döngüde sıfırlanmasın
hafiza = set()

def gonder(mesaj):
    """Buraya kendi bildirim/Telegram fonksiyonunuzu ekleyin"""
    print(f"BİLDİRİM: {mesaj}")

def tara():
    print(f"--- Tarama Başlatıldı ({time.strftime('%H:%M:%S')}) ---")
    try:
        headers = {
            "x-rapidapi-key": K,
            "x-rapidapi-host": HOST
        }
        # API-Football v3 için canlı maç parametresi 'live=all'
        params = {"live": "all"}
        
        response = requests.get(URL, headers=headers, params=params, timeout=15)
        
        if response.status_code != 200:
            print(f"API Hatası ({response.status_code}): {response.text}")
            return

        res = response.json()
        # API-Football v3 yapısında veriler 'response' listesi içindedir
        matches = res.get("response", [])
        print(f"Canlı Maç Sayısı: {len(matches)}")

        for f in matches:
            fixture_id = f["fixture"]["id"]
            dakika = f["fixture"]["status"].get("elapsed")
            
            # Dakika bilgisinin varlığını kontrol et (0. dakika dahil)
            if dakika is not None:
                h_name = f["teams"]["home"]["name"]
                a_name = f["teams"]["away"]["name"]
                h_goal = f["goals"]["home"]
                a_goal = f["goals"]["away"]
                skor = f"{h_goal}-{a_goal}"
                
                # Benzersiz anahtar: Maç ID + Skor (Gol olduğunda yeni sinyal üretir)
                key = f"{fixture_id}_{skor}"
                
                if key not in hafiza:
                    msg = f"🎯 *MAÇ YAKALANDI:* {h_name} {skor} {a_name} ({dakika}')"
                    gonder(msg)
                    hafiza.add(key)
                    
    except Exception as e:
        print(f"Tarama sırasında bir hata oluştu: {e}")

# --- ANA DÖNGÜ (Render Kapanmaması İçin Şart) ---
if __name__ == "__main__":
    print("Bot aktif. Döngü başlatılıyor...")
    while True:
        tara()
        # Her günün sonunda hafızayı temizlemek isterseniz buraya mantık ekleyebilirsiniz.
        # RapidAPI ücretsiz plan limitlerine takılmamak için 60-120 saniye idealdir.
        print("60 saniye bekleniyor...")
        time.sleep(60) 
