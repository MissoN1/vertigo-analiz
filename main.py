
import requests

# Bellek (hafıza) fonksiyonun dışında olmalı, yoksa her seferinde sıfırlanır.
hafiza = set()

def tara():
    print("--- Tarama Başlatıldı ---")
    try:
        # 1. DOĞRU URL: RapidAPI endpointini kullanın
        url = "https://rapidapi.com"
        
        # 2. DOĞRU HEADERS: '://' içermemeli ve büyük/küçük harfe dikkat edilmeli
        headers = {
            "X-RapidAPI-Key": "YOUR_REAL_API_KEY", # Buraya kendi keyinizi yazın
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        
        # 3. DOĞRU PARAMETRELER: API dökümanına göre 'live=all'
        response = requests.get(url, headers=headers, params={"live": "all"}, timeout=15)
        
        # Hata kontrolü için detaylı log
        if response.status_code != 200:
            print(f"Hata Kodu: {response.status_code} - Mesaj: {response.text}")
            return

        res = response.json()
        matches = res.get("response", [])
        
        for f in matches:
            # Maç dakikasını güvenli şekilde alalım
            dak = f.get("fixture", {}).get("status", {}).get("elapsed")
            
            if dak is not None:
                h = f["teams"]["home"]["name"]
                a = f["teams"]["away"]["name"]
                skor = f"{f['goals']['home']}-{f['goals']['away']}"
                
                # Sadece yeni bir olay (gol/başlangıç) olduğunda sinyal gönder
                key = f"{f['fixture']['id']}_{skor}"
                if key not in hafiza:
                    print(f"Yeni Sinyal: {h} {skor} {a}")
                    # gonder(f"🎯 MAÇ: {h} {skor} {a} ({dak}')") 
                    hafiza.add(key)
                    
    except Exception as e:
        print(f"Sistemsel Hata: {e}")





