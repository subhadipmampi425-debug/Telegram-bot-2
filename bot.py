import os
import random
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters
from flask import Flask, request
from transformers import pipeline
from langdetect import detect
from googletrans import Translator

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
translator = Translator()

chatbot = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-medium"
)

emotional_lines = [
    "I'm here for you ❤️",
    "You are not alone 🫂",
    "I care about you deeply 💖",
    "Everything will be okay 🌈"
]

romantic_lines = [
    "I feel close to you 💕",
    "You mean a lot to me 🌸",
    "If I could, I'd hug you right now 🤍"
]

health_tips = [
    "Drink enough water 💧",
    "Sleep 7–8 hours 😴",
    "Daily walking improves mental health 🚶",
    "Eat fresh food 🍎"
]

def reply_logic(text):
    t = text.lower()

    if any(x in t for x in ["sad", "lonely", "depressed", "cry"]):
        return random.choice(emotional_lines)

    if any(x in t for x in ["love", "miss", "hug", "kiss"]):
        return random.choice(romantic_lines)

    if "health" in t or "lifestyle" in t:
        return random.choice(health_tips)

    response = chatbot(text, max_length=120, pad_token_id=50256)
    return response[0]["generated_text"]

def handle_message(update: Update, context):
    user_text = update.message.text

    try:
        lang = detect(user_text)
    except:
        lang = "en"

    if lang != "en":
        user_text = translator.translate(user_text, dest="en").text

    reply = reply_logic(user_text)

    if lang != "en":
        reply = translator.translate(reply, dest=lang).text

    update.message.reply_text(reply)

dispatcher = Dispatcher(None, None, workers=0, use_context=True)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), None)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
