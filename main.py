import requests
import time
import os

# --- YAPILANDIRMA ---
# RapidAPI Key'inizi buraya yazın veya Render Env Var olarak ekleyin
K = "YOUR_RAPIDAPI_KEY_HERE" 
HOST = "api-football-v1.p.rapidapi.com"
URL = "https://rapidapi.com"

# Hafıza: Maç ID ve Skor kombinasyonunu saklar (Sadece gol olunca sinyal atar)
hafiza = set()

def gonder(mesaj):
    # Buraya bildirim (Telegram vb.) kodunu ekleyebilirsin
    print(f"BİLDİRİM GÖNDERİLDİ: {mesaj}")

def tara():
    print(f"--- Tarama Yapılıyor: {time.strftime('%H:%M:%S')} ---")
    headers = {
        "x-rapidapi-key": K,
        "x-rapidapi-host": HOST
    }
    params = {"live": "all"} # Canlı maçlar için v3 standardı
    
    try:
        response = requests.get(URL, headers=headers, params=params, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            # API-Football v3'te veriler 'response' anahtarı altındadır
            matches = data.get("response", [])
            print(f"Bulunan Canlı Maç: {len(matches)}")
            
            for m in matches:
                f_id = m["fixture"]["id"]
                dakika = m["fixture"]["status"]["elapsed"]
                h_team = m["teams"]["home"]["name"]
                a_team = m["teams"]["away"]["name"]
                h_goal = m["goals"]["home"]
                a_goal = m["goals"]["away"]
                skor = f"{h_goal}-{a_goal}"
                
                # Hem maç ID'si hem skor değişmişse yeni sinyaldir
                key = f"{f_id}_{skor}"
                
                if key not in hafiza:
                    msg = f"⚽ {h_team} {skor} {a_team} ({dakika}. dk)"
                    gonder(msg)
                    hafiza.add(key)
        else:
            print(f"API Hatası: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")

# --- ANA DÖNGÜ ---
if __name__ == "__main__":
    print("Sistem Başlatıldı...")
    while True:
        tara()
        # Ücretsiz plan limitleri için 60 saniye bekleme idealdir
        time.sleep(60) 
