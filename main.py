import requests

# --- TELEGRAM BİLGİLERİN ---
TOKEN = "BOT_TOKEN_BURAYA"  # BotFather'dan aldığın kod
CHAT_ID = "CHAT_ID_BURAYA"  # Kendi kullanıcı ID'n

def test_mesaji_gonder(mesaj):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Test mesajı Telegram'a başarıyla gönderildi!")
        else:
            print(f"❌ Hata oluştu: {response.text}")
    except Exception as e:
        print(f"⚠️ Bağlantı hatası: {e}")

if __name__ == "__main__":
    print("Telegram testi başlatılıyor...")
    test_mesaji_gonder("🚀 *Bot Test Mesajı:* Selam! Eğer bu mesajı görüyorsan bağlantı tamamdır.")
