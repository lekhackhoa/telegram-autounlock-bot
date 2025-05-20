from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "THAY_TOKEN_VAO_DAY"

user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    user_progress[user_id] = 0

    # Gửi tin nhắn hướng dẫn
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text="""
🔒 Bạn đang bị khóa chat.

Để mở khóa, hãy chia sẻ link này vào 3 nhóm khác:
➡️ https://t.me/+abcdefghi123

Sau mỗi lần chia sẻ, hãy gõ /shared để xác nhận.
"""
    )

    # Ghim tin nhắn đó lên đầu
    try:
        await context.bot.pin_chat_message(
            chat_id=chat_id,
            message_id=msg.message_id,
            disable_notification=True
        )
    except:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Không thể ghim (bot chưa được quyền admin).")

async def shared(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    user_progress[user_id] = user_progress.get(user_id, 0) + 1

    if user_progress[user_id] >= 3:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await context.bot.send_message(chat_id=chat_id, text="✅ Đã mở khóa chat cho bạn!")
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📢 Bạn đã chia sẻ {user_progress[user_id]}/3. Hãy tiếp tục!"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("shared", shared))
app.run_polling()
