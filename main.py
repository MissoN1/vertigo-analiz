
import requests, time, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- AYARLAR ---
T = "8609069597:AAHih02l6YvPZudU6fET6LLQx9LOSIGjdaw"
U = "5152977214"
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
hafiza = set()

# --- RENDER UYKU ENGELLEYİCİ ---
class S(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def do_HEAD(self): self.send_response(200); self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), S)
    server.serve_forever()

def gonder(mesaj):
    # BURASI ÇOK KRİTİK: api. ve /bot/ kısmı mutlaka olmalı
    url = f"https://telegram.org{T}/sendMessage"
    payload = {"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=10)
    except: pass

def tara():
    url = "https://rapidapi.com"
    headers = {"x-rapidapi-key": K, "x-rapidapi-host": "://rapidapi.com"}
    params = {"live": "all"}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=15).json()
        for f in res.get("response", []):
            dak = f["fixture"]["status"]["elapsed"]
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h, a, skor = f["teams"]["home"]["name"], f["teams"]["away"]["name"], f"{f['goals']['home']}-{f['goals']['away']}"
                key = f"{f['fixture']['id']}_{skor}"
                if key not in hafiza:
                    gonder(f"🎯 *Sinyal:* {h} {skor} {a} ({dak}')")
                    hafiza.add(key)
    except: pass

if __name__ == "__main__":
    # Render'ı kandıran sunucuyu başlat
    threading.Thread(target=run_server, daemon=True).start()
    print("🚀 Vertigo AI Yayında!")
    gonder("✅ *Vertigo AI Yayına Girdi!*")
    while True:
        tara()
        time.sleep(300)
        
