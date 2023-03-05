from typing import Any
import requests
import json
from datetime import date, timedelta
from dotenv import load_dotenv
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.constants import ParseMode
from fastapi import FastAPI
from Models.Request import UpdateRequest

keyboard = [
    [InlineKeyboardButton("Последние новости за сегодня", callback_data="/today_latest")]
]

load_dotenv()

app = FastAPI()

@app.post("/")
async def handle_bot_message(update: UpdateRequest):
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    
    if update.callback_query is None  & update.message is not None: 
        await handle_message(bot, update)
    elif update.callback_query is not None & update.message is None:
        await handle_command(bot, update)
    else:
        return { "status": "Not detected" }
    
    return { "status": "OK" }

async def handle_message(bot: Bot, update: UpdateRequest):
    await bot.send_message(
        chat_id=update.message.chat.id, 
        text="Выберите команду", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_command(bot: Bot, update: UpdateRequest):
    if update.callback_query.data == "/today_latest":
        await handeLatestNews(bot, chat_id=update.callback_query.message.chat.id)

async def handeLatestNews(bot: Bot, chat_id: int):
    data = makeNewsApiRequest()
    articles_number = data["totalResults"]
    message = "Количество статей: <b>{0}</b>".format(articles_number)
    itteration = 1

    for article in data["articles"][:10]:
        message += "\n\n<b>{0}. {1}</b>\n{2}".format(itteration, article["title"], article["url"])
        itteration += 1
        
    await bot.send_message(
        chat_id,
        text=message,
        parse_mode=ParseMode.HTML
    )

    await bot.send_message(
        chat_id, 
        text="Выберите команду", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def makeNewsApiRequest() -> Any:
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
    return json.loads(response.text)