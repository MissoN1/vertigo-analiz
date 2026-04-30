def tara():
    try:
        url = "https://rapidapi.com"
        headers = {
            "x-rapidapi-key": K, 
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params={"live": "all"}, timeout=15)
        
        # HATA AYIKLAMA SATIRLARI:
        print(f"Status Code: {response.status_code}") # 200 mü?
        res = response.json()
        
        if "errors" in res and res["errors"]:
            print(f"API Hatası: {res['errors']}") # Key veya kota hatası burada yazar
            return

        matches = res.get("response", [])
        print(f"Bulunan Canlı Maç Sayısı: {len(matches)}") # 0 ise o an kriterlerine uygun maç yoktur

        for f in matches:
            # ... geri kalan işlemler ...
