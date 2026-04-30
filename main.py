
import requests, time, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- AYARLAR ---
T = "8603872966:AAEdfu11dx-_-edpywbFKT2yqA7IRg5cO3o"
U = "5152977214"
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
hafiza = set()

class S(BaseHTTPRequestHandler):
    def do_GET(self): 
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Sistem Aktif")

def gonder(mesaj):
    url = f"https://telegram.org{T}/sendMessage"
    try: 
        requests.post(url, json={"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e: 
        print(f"Telegram Hatası: {e}")

def tara():
    try:
        url = "https://rapidapi.com"
        headers = {
            "x-rapidapi-key": K, 
            "x-rapidapi-host": "://rapidapi.com"
        }
        # TEST İÇİN: 120 saniyede bir (2 dakika) kontrol uygundur
        res = requests.get(url, headers=headers, params={"live": "all"}, timeout=15).json()
        
        if "response" not in res or not res["response"]:
            print("Canlı maç bulunamadı veya API boş döndü.")
            return

        for f in res["response"]:
            status = f.get("fixture", {}).get("status", {})
            dak = status.get("elapsed")
            fid = f["fixture"]["id"]
            
            # Sinyal Kriteri: 15-35 veya 65-80 arası
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h = f["teams"]["home"]["name"]
                a = f["teams"]["away"]["name"]
                skor = f"{f['goals']['home']}-{f['goals']['away']}"
                lig = f["league"]["name"]
                
                key = f"{fid}_{skor}"
                if key not in hafiza:
                    msg = f"⚽ *SİNYAL BULUNDU*\n🏆 {lig}\n🏟️ {h} {skor} {a}\n⏰ Dakika: {dak}'"
                    gonder(msg)
                    hafiza.add(key)
                    
                    if len(hafiza) > 500: hafiza.clear()
    except Exception as e: 
        print(f"Tarama Hatası: {e}")

if __name__ == "__main__":
    # Render port ayarı
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', port), S).serve_forever(), daemon=True).start()
    
    gonder("✅ *Sistem Hatalardan Arındırıldı ve Başlatıldı!*")
    while True:
        tara()
        time.sleep(120) 
