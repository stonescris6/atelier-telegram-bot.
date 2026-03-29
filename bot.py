# bot.py
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# ========================
# Replace this with your bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# ========================

FAQ_ANSWERS = {
    "what is atelier": "Atelier is a decentralized AI marketplace where you can buy and sell AI agent services. More info at https://atelierai.xyz.",
    "register": "To register on Atelier, visit https://atelierai.xyz and click 'Sign Up'.",
    "payment": "Payments on Atelier are processed via your connected wallet. Learn more at https://atelierai.xyz/payments.",
    "list service": "You can list your AI agent services on Atelier by visiting your dashboard and clicking 'Create Agent'.",
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi! I'm AtelierFAQBot 🤖\nAsk me anything about Atelier!"
    )

def answer_question(update: Update, context: CallbackContext):
    question = update.message.text.lower()
    response = None
    for keyword, answer in FAQ_ANSWERS.items():
        if keyword in question:
            response = answer
            break
    if not response:
        response = "I’m not sure about that. Please check https://atelierai.xyz for details."
    update.message.reply_text(response)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_question))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
