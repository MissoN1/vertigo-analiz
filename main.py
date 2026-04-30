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
    url = f"https://api.telegram.org/bot{T}/sendMessage"
    payload = {"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}
    try: 
        r = requests.post(url, json=payload, timeout=10)
        print(f"Telegram Yanıtı: {r.status_code}")
    except Exception as e: 
        print(f"Telegram Hatası: {e}")

def tara():
    print("Maçlar taranıyor...")
    try:
        url = "https://rapidapi.com"
        headers = {"x-rapidapi-key": K, "x-rapidapi-host": "://rapidapi.com"}
        res = requests.get(url, headers=headers, params={"live": "all"}, timeout=15).json()
        
        matches = res.get("response", [])
        print(f"Bulunan canlı maç sayısı: {len(matches)}")

        for f in matches:
            try:
                dak = f["fixture"]["status"]["elapsed"]
                fid = f["fixture"]["id"]
                
                # Eğer o an kriterlere uygun maç varsa:
                if dak and ((15 <= dak <= 35) or (65 <= dak <= 80)):
                    h = f["teams"]["home"]["name"]
                    a = f["teams"]["away"]["name"]
                    skor = f"{f['goals']['home']}-{f['goals']['away']}"
                    
                    # Sadece daha önce göndermediğimiz maç/skor kombinasyonunu gönder
                    key = f"{fid}_{skor}"
                    if key not in hafiza:
                        msg = f"🎯 *YENİ SİNYAL*\n🏟️ {h} {skor} {a}\n⏰ Dakika: {dak}'"
                        gonder(msg)
                        hafiza.add(key)
            except KeyError:
                continue # Bazı veriler eksikse o maçı atla

        # Hafıza yönetimi: Çok şişerse temizle (Günde bir kez gibi düşünebilirsin)
        if len(hafiza) > 1000: hafiza.clear()

    except Exception as e: 
        print(f"Tarama sırasında hata oluştu: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', port), S).serve_forever(), daemon=True).start()
    
    gonder("✅ *Bot Aktif Edildi. Maçlar Bekleniyor...*")
    while True:
        tara()
        time.sleep(120) # 2 dakikada bir kontrol idealdir






