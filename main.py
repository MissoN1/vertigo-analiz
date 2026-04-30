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
        self.wfile.write(b"Sistem Calisiyor")

def gonder(mesaj):
    # DÜZELTME: Doğru Telegram API URL yapısı
    url = f"https://api.telegram.org/bot{T}/sendMessage"
    try: 
        requests.post(url, json={"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e: 
        print(f"Telegram Hatası: {e}")

def tara():
    try:
        # DÜZELTME: Doğru API uç noktası ve host ayarı
        url = "https://rapidapi.com"
        headers = {
            "x-rapidapi-key": K, 
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
        }
        # 'live': 'all' parametresi ile canlı maçları çekiyoruz
        res = requests.get(url, headers=headers, params={"live": "all"}, timeout=15).json()
        
        if "response" not in res:
            print("API'den beklenen yanıt alınamadı.")
            return

        for f in res.get("response", []):
            dak = f["fixture"]["status"]["elapsed"]
            # Belirlediğin dakika aralıkları (15-35 veya 65-80 arası)
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h = f["teams"]["home"]["name"]
                a = f["teams"]["away"]["name"]
                skor = f"{f['goals']['home']}-{f['goals']['away']}"
                fid = f["fixture"]["id"]
                
                # Sinyalin daha önce gönderilip gönderilmediğini kontrol et
                if f"{fid}_{skor}" not in hafiza:
                    gonder(f"🎯 *SİNYAL:* {h} {skor} {a} ({dak}')")
                    hafiza.add(f"{fid}_{skor}")
    except Exception as e: 
        print(f"Tarama Hatası: {e}")

if __name__ == "__main__":
    # Sağlık kontrolü (Health Check) için basit HTTP sunucusu
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', port), S).serve_forever(), daemon=True).start()
    
    gonder("✅ *Sistem Baslatildi!*")
    while True:
        tara()
        # API limitlerini zorlamamak için 5 dakikada bir çalışır
        time.sleep(300)
