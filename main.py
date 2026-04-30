import requests
import time
import os

# --- YAPILANDIRMA ---
# Render'da 'Environment Variables' kısmına RAPIDAPI_KEY eklemeniz en sağlıklısıdır.
K = os.getenv("RAPIDAPI_KEY", "BURAYA_KEY_YAZIN")
HOST = "api-football-v1.p.rapidapi.com"
URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

# Hafıza: Aynı maçı tekrar bildirmemek için ID + Skor saklar
hafiza = set()

def tara():
    print(f"--- Canlı Tarama: {time.strftime('%H:%M:%S')} ---")
    headers = {
        "x-rapidapi-key": K,
        "x-rapidapi-host": HOST
    }
    # Canlı maçları getiren standart parametre
    params = {"live": "all"}
    
    try:
        response = requests.get(URL, headers=headers, params=params, timeout=20)
        
        if response.status_code == 200:
            res_data = response.json()
            matches = res_data.get("response", [])
            print(f"Aktif Maç Sayısı: {len(matches)}")
            
            for m in matches:
                f_id = m["fixture"]["id"]
                # Maç süresi (elapsed) bazen None dönebilir, güvenli çekim yapalım
                dakika = m["fixture"]["status"].get("elapsed", "?")
                h_name = m["teams"]["home"]["name"]
                a_name = m["teams"]["away"]["name"]
                h_goal = m["goals"]["home"]
                a_goal = m["goals"]["away"]
                
                skor = f"{h_goal}-{a_goal}"
                # Gol olduğunda skor değişeceği için key de değişir ve yeni bildirim gider
                key = f"{f_id}_{skor}"
                
                if key not in h_name: # Bu kısım hafiza kontrolü için düzeltildi
                    if key not in hafiza:
                        print(f"Sinyal Gönderildi: {h_name} {skor} {a_name}")
                        # gonder_fonksiyonu(f"⚽ {h_name} {skor} {a_name} ({dakika}')")
                        hafiza.add(key)
        else:
            print(f"API Hatası: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")

# --- ANA ÇALIŞTIRICI ---
if __name__ == "__main__":
    print("Bot başlatıldı. Background Worker modunda çalışıyor...")
    while True:
        tara()
        # Ücretsiz planlarda limitlere takılmamak için 60 saniye idealdir
        time.sleep(60)
        
