from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7513610669:AAEDOH0JWDpU0K_RSvEmW7XVPAKpYEN72I0"

user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Chỉ chấp nhận lệnh trong nhóm (group hoặc supergroup)
    if update.effective_chat.type not in ["group", "supergroup"]:
        await context.bot.send_message(chat_id=chat_id, text="Hãy dùng lệnh này trong nhóm bị khóa nhé!")
        return

    # Khóa user (tắt quyền gửi tin nhắn)
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False)
    )

    # Reset số lần chia sẻ
    user_progress[user_id] = 0

    msg = await context.bot.send_message(
        chat_id=chat_id,
        text="""
🔒 Bạn đang bị khóa chat.

Để mở khóa, hãy chia sẻ link này vào 3 nhóm khác:
➡️ https://t.me/+abcdefghi123

Sau mỗi lần chia sẻ, hãy gõ /shared để xác nhận.
"""
    )

    try:
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=msg.message_id, disable_notification=True)
    except Exception:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Bot chưa có quyền ghim tin nhắn.")

async def shared(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Chỉ cho phép trong nhóm
    if update.effective_chat.type not in ["group", "supergroup"]:
        await context.bot.send_message(chat_id=chat_id, text="Lệnh này chỉ dùng trong nhóm bị khóa.")
        return

    if user_id not in user_progress:
        await context.bot.send_message(chat_id=chat_id, text="Bạn chưa bắt đầu, hãy dùng /start trước.")
        return

    user_progress[user_id] += 1

    if user_progress[user_id] >= 3:
        # Mở khóa toàn quyền
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )
        await context.bot.send_message(chat_id=chat_id, text="✅ Bạn đã mở khóa chat!")
        user_progress.pop(user_id)  # Xóa dữ liệu user khi mở khóa xong
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"📢 Bạn đã chia sẻ {user_progress[user_id]}/3. Tiếp tục nhé!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("shared", shared))
app.run_polling()
