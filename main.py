import requests
import time

# --- AYARLAR ---
T = "8609069597:AAHih02l6YvPZudU6fET6LLQx9LOSIGjdaw"
U = "5152977214"
K = "4cf7b1ef28msha505e3056cd48f6p110e8djsnd6c3f7ee3424"
HOST = "://rapidapi.com"

# Aynı skorları veya sinyalleri tekrar tekrar atmaması için hafıza
hafiza = set()

def gonder(mesaj):
    url = f"https://telegram.org{T}/sendMessage"
    payload = {"chat_id": U, "text": mesaj, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def tara():
    # Canlı maçları çek
    url = f"https://{HOST}/v3/fixtures"
    headers = {"x-rapidapi-key": K, "x-rapidapi-host": HOST}
    params = {"live": "all"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        res = response.json()
        fixtures = res.get("response", [])
        
        for f in fixtures:
            f_id = f["fixture"]["id"]
            dak = f["fixture"]["status"]["elapsed"]
            
            # SENİN STRATEJİN: Sadece 15-35 ve 65-80 arası analiz yap
            if not dak or not ((15 <= dak <= 35) or (65 <= dak <= 80)):
                continue

            h_name = f["teams"]["home"]["name"]
            a_name = f["teams"]["away"]["name"]
            skor = f"{f['goals']['home']}-{f['goals']['away']}"
            
            # İstatistikleri (Korner, Şut, Baskı) çek
            try:
                s_url = f"https://{HOST}/v3/fixtures/statistics"
                s_res = requests.get(s_url, headers=headers, params={"fixture": f_id}).json()
                stats_list = s_res.get("response", [])
                
                if len(stats_list) < 2: continue
                
                # Değerleri ayıkla (Ev sahibi ve Deplasman toplamı)
                def get_val(s_data, s_type):
                    val = 0
                    for side in s_data:
                        for item in side["statistics"]:
                            if item["type"] == s_type:
                                val += int(item["value"]) if item["value"] else 0
                    return val

                t_atak = get_val(stats_list, "Dangerous Attacks")
                korner = get_val(stats_list, "Corner Kicks")
                sut = get_val(stats_list, "Shots on Goal")
                
                # SENİN FORMÜLÜN: Baskı Endeksi (Atak / Dakika)
                baski = round(t_atak / dak, 2) if dak > 0 else 0

                # ANALİZ: Baskı 1.2'den büyükse veya Korner yoğunsa
                if baski > 1.2 or korner > (dak/4):
                    key = f"{f_id}_{skor}_ai"
                    if key not in hafiza:
                        msg = (f"🔥 *AI ANALİZ: BASKI YÜKSEK*\n"
                               f"🏟 {h_name} - {a_name}\n"
                               f"⏱ Dakika: {dak}' | Skor: {skor}\n"
                               f"📊 Baskı Endeksi: {baski}\n"
                               f"🎯 İsabetli Şut: {sut}\n"
                               f"🚩 Toplam Korner: {korner}\n"
                               f"💡 *Öneri:* Gol Baskısı Var!")
                        gonder(msg)
                        hafiza.add(key)
            except:
                continue
                
    except Exception as e:
        print(f"Hata: {e}")

# BAŞLAT
if __name__ == "__main__":
    print("🚀 AI Analiz Sistemi Başlatıldı...")
    gonder("🤖 *Vertigo AI Analiz Sistemi Aktif!* Takip başlıyor.")
    while True:
        tara()
        time.sleep(120) # 2 dakikada bir kontrol analiz için idealdir
