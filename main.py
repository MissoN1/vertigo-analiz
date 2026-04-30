
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# BotFather'dan aldığın token'ı buraya yapıştır
TOKEN = 'BURAYA_TOKEN_GELECEK'

async def merhaba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Selam {update.effective_user.first_name}! Kanalın için hazır mısın?')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # /merhaba komutunu tanımlıyoruz
    app.add_handler(CommandHandler("merhaba", merhaba))
    
    print("Bot çalışıyor...")
    app.run_polling()
