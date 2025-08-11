import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Cargamos las variables del .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy tu bot informativo de noticias, clima y criptomonedas. ¿Qué te gustaría hacer?\n"
        "Comandos disponibles:\n"
        "/clima <ciudad>: Obtén el clima actual de una ciudad.\n"
        "/noticias: Obtén las noticias más relevantes del día.\n"
        "/crypto <nombre_criptomoneda>: Obtén el precio de las principales criptomonedas cómo bitcoin, ethereum, etc.\n"
        )

# clima
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Por favor, indica una ciudad. Ej: /clima Madrid")
        return

    ciudad = " ".join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&lang=es&units=metric"
    resp = requests.get(url).json()

    if resp.get("cod") != 200:
        await update.message.reply_text("No encontré esa ciudad.")
        return

    temp = resp["main"]["temp"]
    desc = resp["weather"][0]["description"]
    await update.message.reply_text(f"🌤 Clima en {ciudad}:\n{temp}°C, {desc}")

# noticias
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://newsapi.org/v2/top-headlines?country=es&apiKey={NEWS_API_KEY}"
    resp = requests.get(url).json()

    if resp.get("status") != "ok":
        await update.message.reply_text("⚠️ No pude obtener noticias. Verifica tu API key.")
        return

    articles = resp.get("articles", [])
    if not articles:
        await update.message.reply_text("⚠️ No hay noticias disponibles en este momento.")
        return

    mensajes = []
    for article in articles[:5]:
        title = article.get("title")
        link = article.get("url")

        if title and link:
            mensajes.append(f"📰 {title}\n{link}")

    if mensajes:
        await update.message.reply_text("\n\n".join(mensajes))
    else:
        await update.message.reply_text("⚠️ No encontré noticias con información válida.")

# criptomonedas
async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("💰 Por favor, indica una criptomoneda. Ej: /crypto bitcoin")
        return

    crypto_name = context.args[0].lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd,eur"

    resp = requests.get(url).json()

    if crypto_name not in resp:
        await update.message.reply_text("⚠️ No encontré esa criptomoneda. Intenta con 'bitcoin', 'ethereum', etc.")
        return

    price_usd = resp[crypto_name]['usd']
    price_eur = resp[crypto_name]['eur']

    await update.message.reply_text(
        f"💹 Precio actual de {crypto_name.capitalize()}:\n"
        f"USD: ${price_usd}\n"
        f"EUR: €{price_eur}"
    )


# main
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CommandHandler("crypto", crypto))

    print("🤖 Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()