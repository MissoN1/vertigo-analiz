import requests, time, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- GÜNCEL AYARLARIN ---
T = "8603872966:AAEdfu11dx-_-edpywbFKT2yqA7IRg5cO3o" # Yeni Tertemiz Botun
U = "5152977214" # Senin Chat ID'n
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424" # API Anahtarın
hafiza = set()

# --- RENDER ONAY SİSTEMİ (PORT HATASINI ÇÖZER) ---
class S(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def do_HEAD(self): self.send_response(200); self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), S).serve_forever()

def gonder(mesaj):
    # Telegram adresi en doğru haliyle düzeltildi
    url = f"https://telegram.org{T}/sendMessage"
    payload = {"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=10)
    except: pass

def tara():
    url = "https://rapidapi.com"
    headers = {"x-rapidapi-key": K, "x-rapidapi-host": "://rapidapi.com"}
    try:
        res = requests.get(url, headers=headers, params={"live": "all"}, timeout=15).json()
        for f in res.get("response", []):
            dak = f["fixture"]["status"]["elapsed"]
            # Analiz Dakikaları: 15-35 ve 65-80
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h, a, skor = f["teams"]["home"]["name"], f["teams"]["away"]["name"], f"{f['goals']['home']}-{f['goals']['away']}"
                key = f"{f['fixture']['id']}_{skor}"
                if key not in hafiza:
                    msg = (f"🔥 *VERTIGO ANALİZ SİNYALİ*\n\n"
                           f"🏟 Maç: {h} - {a}\n"
                           f"⏱ Dakika: {dak}' | Skor: {skor}\n"
                           f"💡 Öneri: Baskı yüksek, Gol Yakın!")
                    gonder(msg)
                    hafiza.add(key)
    except: pass

if __name__ == "__main__":
    # Render'ı uyanık tutan sunucuyu başlat
    threading.Thread(target=run_server, daemon=True).start()
    print("🚀 Vertigo AI Yayında!")
    gonder("✅ *Vertigo AI Yayına Girdi!* Sistem şu an 7/24 pusuya yattı.")
    while True:
