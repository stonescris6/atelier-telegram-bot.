# bot.py
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Use Railway environment variable
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

FAQ_ANSWERS = {
    "what is atelier": "Atelier is a decentralized AI marketplace where you can buy and sell AI agent services. More info at https://atelierai.xyz.",
    "register": "To register on Atelier, visit https://atelierai.xyz and click 'Sign Up'.",
    "payment": "Payments on Atelier are processed via your connected wallet. Learn more at https://atelierai.xyz/payments.",
    "list service": "You can list your AI agent services on Atelier by visiting your dashboard and clicking 'Create Agent'.",
}

# /start command
def start(update, context):
    update.message.reply_text("Hi! I'm AtelierFAQBot 🤖\nAsk me anything about Atelier!")

# Handle messages
def answer_question(update, context):
    question = update.message.text.lower()
    response = None
    for keyword, answer in FAQ_ANSWERS.items():
        if keyword in question:
            response = answer
            break
    if not response:
        response = "I’m not sure about that. Please check https://atelierai.xyz for details."
    update.message.reply_text(response)

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_question))

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Root route
@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
