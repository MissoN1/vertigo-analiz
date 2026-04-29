
import requests
import time
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- AYARLAR ---
T = "8609069597:AAHih02l6YvPZudU6fET6LLQx9LOSIGjdaw"
U = "5152977214"
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
HOST = "://rapidapi.com"

hafiza = set()

# --- RENDER'IN BEKLEDİĞİ PORTU AÇAN KISIM ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Aktif")

def run_server():
    # Render'ın otomatik atadığı portu alıyoruz
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def gonder(mesaj):
    url = f"https://telegram.org{T}/sendMessage"
    payload = {"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=10)
    except: pass

def tara():
    url = f"https://{HOST}/v3/fixtures"
    headers = {"x-rapidapi-key": K, "x-rapidapi-host": HOST}
    params = {"live": "all"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        fixtures = response.json().get("response", [])
        for f in fixtures:
            f_id = f["fixture"]["id"]
            dak = f["fixture"]["status"]["elapsed"]
            # Senin Stratejin: 15-35 ve 65-80 arası
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h, a, skor = f["teams"]["home"]["name"], f["teams"]["away"]["name"], f"{f['goals']['home']}-{f['goals']['away']}"
                if f"{f_id}_{skor}" not in hafiza:
                    gonder(f"🎯 *Sinyal:* {h} {skor} {a} (Dakika: {dak}')")
                    hafiza.add(f"{f_id}_{skor}")
    except: pass

if __name__ == "__main__":
    # Render'ın "uykuya dalmasını" engelleyen sunucuyu başlat
    threading.Thread(target=run_server, daemon=True).start()
    
    print("🚀 Sistem Başlatıldı!")
    gonder("✅ *Vertigo AI Analiz Yayında!* Sistem başarıyla kuruldu.")
    
    while True:
        tara()
        time.sleep(300)
