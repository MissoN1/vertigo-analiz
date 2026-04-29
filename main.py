import requests, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- AYARLARIN ---
T, U, K = "8609069597:AAHih02l6YvPZudU6fET6LLQx9LOSIGjdaw", "5152977214", "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
hafiza = set()

# --- RENDER İÇİN UYKU ENGELLEYİCİ ---
class S(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

def g(m): requests.post(f"https://telegram.org{T}/sendMessage", json={"chat_id":U,"text":m,"parse_mode":"Markdown"})

def tara():
    try:
        res = requests.get("https://rapidapi.com", headers={"x-rapidapi-key":K,"x-rapidapi-host":"://rapidapi.com"}, params={"live":"all"}).json()
        for f in res.get("response", []):
            dak = f["fixture"]["status"]["elapsed"]
            if dak and ((15<=dak<=35) or (65<=dak<=80)):
                h, a, skor = f["teams"]["home"]["name"], f["teams"]["away"]["name"], f"{f['goals']['home']}-{f['goals']['away']}"
                if f"{f['fixture']['id']}_{skor}" not in hafiza:
                    g(f"🔥 *Sinyal:* {h} {skor} {a} ({dak}')"); hafiza.add(f"{f['fixture']['id']}_{skor}")
    except: pass

if __name__ == "__main__":
    # Port açarak Render'ı uyanık tutuyoruz
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), S).serve_forever(), daemon=True).start()
    g("✅ *Vertigo AI Yayına Girdi!*"); 
    while True: tara(); time.sleep(300)
