import requests
import json
from datetime import date, timedelta
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

keyboard = [
    [InlineKeyboardButton("Последние новости за сегодня", callback_data="/today_latest")]
]

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Выберите команду", 
        reply_markup=InlineKeyboardMarkup(keyboard))
    
async def today_latest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api_key = os.environ["NEWSAPI_KEY"]
    cryptocurrencies = ["bitcoin", "ethereum", "dogecoin"]
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": " OR ".join(cryptocurrencies),
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": api_key,
        "from": (date.today() - timedelta(days=2)).isoformat()
    }

    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    articles_number = data["totalResults"]
    message = "Количество статей: <b>{0}</b>".format(articles_number)
    itteration = 1

    for article in data["articles"][:10]:
        message += "\n\n<b>{0}. {1}</b>\n{2}".format(itteration, article["title"], article["url"])
        itteration += 1
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=ParseMode.HTML
    )

if __name__ == '__main__':
    load_dotenv()
    application = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(today_latest_handler))
    application.run_polling()