import requests, time, threading, os
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- AYARLAR ---
T = "8603872966:AAEdfu11dx-_-edpywbFKT2yqA7IRg5cO3o"
U = "5152977214"
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
hafiza = set()

class S(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def do_HEAD(self): self.send_response(200); self.end_headers()

def gonder(mesaj):
    url = f"https://telegram.org{T}/sendMessage"
    try: requests.post(url, json={"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def tara():
    try:
        url = "https://rapidapi.com"
        headers = {"x-rapidapi-key": K, "x-rapidapi-host": "://rapidapi.com"}
        res = requests.get(url, headers=headers, params={"live": "all"}, timeout=15).json()
        for f in res.get("response", []):
            dak = f["fixture"]["status"]["elapsed"]
            if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                h, a, skor = f["teams"]["home"]["name"], f["teams"]["away"]["name"], f"{f['goals']['home']}-{f['goals']['away']}"
                if f"{f['fixture']['id']}_{skor}" not in hafiza:
                    gonder(f"🎯 *SİNYAL:* {h} {skor} {a} ({dak}')")
                    hafiza.add(f"{f['fixture']['id']}_{skor}")
    except: pass

if __name__ == "__main__":
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), S).serve_forever(), daemon=True).start()
    gonder("✅ *Sistem Baslatildi!*")
    while True:
        tara()
        time.sleep(300)
