import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I am Sweety 💕\n"
        "I can chat with you, answer questions, and keep you company 😊\n\n"
        "Just type anything 💬"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hi" in text or "hello" in text:
        reply = "Hey 😊 I'm here for you 💖"
    elif "how are you" in text:
        reply = "I'm feeling good because you're here 🥰"
    elif "cat" in text:
        reply = "🐱 A cat is a small, cute, furry animal that loves sleep and play."
    elif "your name" in text:
        reply = "My name is Sweety 💕"
    else:
        reply = "Hmm 😊 tell me more..."

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
