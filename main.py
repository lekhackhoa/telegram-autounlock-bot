from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = os.environ.get("GROUP_ID")

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=GROUP_ID, text="🔓 Nhóm đã được mở khoá! Vào học ngay nha 📌", disable_notification=False)
    context.bot.pin_chat_message(chat_id=GROUP_ID, message_id=update.message.message_id + 1)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("unlock", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
