import logging
import os
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Replace with your API server URL
API_BASE_URL = "http://localhost:8000"

# Telegram bot token
TOKEN = "8667535912:AAHqXhpMfHhNlZhY1Kd26KwwVogeQiyWdJA"

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Conversation states
STEP, QUESTION = range(2)

# Helper functions to call API

def api_post(path, data):
    try:
        resp = requests.post(API_BASE_URL + path, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None

# Bot handlers

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Send /virgildiana to start the idea workflow."
    )


def start_virgildiana(update: Update, context: CallbackContext):
    session_id = str(update.effective_user.id)
    response = api_post("/start", {"session_id": session_id})
    if response and "message" in response:
        update.message.reply_text(response["message"])
        context.user_data['step'] = 0
        context.user_data['question'] = 0
        return STEP
    else:
        update.message.reply_text("Failed to start workflow.")
        return ConversationHandler.END


def handle_answer(update: Update, context: CallbackContext):
    session_id = str(update.effective_user.id)
    user_answer = update.message.text
    response = api_post("/answer", {"session_id": session_id, "answer": user_answer})
    if response and "message" in response:
        update.message.reply_text(response["message"])
        if response["message"].startswith("All steps complete"):
            return ConversationHandler.END
        return STEP
    else:
        update.message.reply_text("An error occurred while processing your answer.")
        return ConversationHandler.END


def virgildiana_report(update: Update, context: CallbackContext):
    session_id = str(update.effective_user.id)
    response = api_post("/report", {"session_id": session_id})
    if response and "report" in response:
        update.message.reply_text(response["report"], parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Failed to retrieve report.")


def virgildiana_restart(update: Update, context: CallbackContext):
    session_id = str(update.effective_user.id)
    response = api_post("/restart", {"session_id": session_id})
    if response and "message" in response:
        update.message.reply_text(response["message"])
    else:
        update.message.reply_text("Failed to restart workflow.")


def virgildiana_cancel(update: Update, context: CallbackContext):
    session_id = str(update.effective_user.id)
    response = api_post("/cancel", {"session_id": session_id})
    if response and "message" in response:
        update.message.reply_text(response["message"])
    else:
        update.message.reply_text("Failed to cancel workflow.")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("virgildiana", start_virgildiana)],
        states={
            STEP: [MessageHandler(Filters.text & ~Filters.command, handle_answer)]
        },
        fallbacks=[CommandHandler("virgildiana_cancel", virgildiana_cancel)]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("virgildiana_report", virgildiana_report))
    dispatcher.add_handler(CommandHandler("virgildiana_restart", virgildiana_restart))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("virgildiana_cancel", virgildiana_cancel))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
