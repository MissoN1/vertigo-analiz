import requests, time, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- AYARLARIN ---
T = "8609069597:AAHih02l6YvPZudU6fET6LLQx9LOSIGjdaw"
U = "5152977214"
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
hafiza = set()

# --- RENDER ONAY SİSTEMİ ---
class S(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def do_HEAD(self): self.send_response(200); self.end_headers()

def gonder(mesaj):
    url = f"https://telegram.org{T}/sendMessage"
    try: requests.post(url, json={"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def tara():
    try:
        res = requests.get("https://rapidapi.com", 
                           headers={"x-rapidapi-key": K, "x-rapidapi-host": "://rapidapi.com"}, 
                           params={"live": "all"}).json()
        for f in res.get("response", []):
            dak = f["fixture"]["status"]["elapsed"]
            # Senin Stratejin: 15-35 ve 65-80 arası analiz
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h, a, skor = f["teams"]["home"]["name"], f["teams"]["away"]["name"], f"{f['goals']['home']}-{f['goals']['away']}"
                key = f"{f['fixture']['id']}_{skor}"
                if key not in hafiza:
                    # TAMAMEN TÜRKÇE MESAJ FORMATI
                    msg = (f"🔥 *VERTIGO ANALİZ SİNYALİ*\n\n"
                           f"🏟 *Maç:* {h} - {a}\n"
                           f"⏱ *Dakika:* {dak}' | *Skor:* {skor}\n"
                           f"💡 *Öneri:* Gol Baskısı Arttı, ÜST Kovala!")
                    gonder(msg)
                    hafiza.add(key)
    except: pass

if __name__ == "__main__":
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), S).serve_forever(), daemon=True).start()
    print("🚀 Vertigo AI Aktif!")
    gonder("✅ *Vertigo AI Yayına Girdi!* Sistem artık Türkçe ve 7/24 pusuya yattı.")
    while True: tara(); time.sleep(300)
