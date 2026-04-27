from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import datetime
import os

# ================== 直接写死（调试用） ==================
TOKEN = "8616207021:AAFbbuQhUSAOOLYuSWP8mr31YF8cVjjfydg"
OWNER_ID = 8260959315

# 图片文件名
IMAGE_PATH = "synt.png"

active_users = {}
current_target = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 很高兴接待您～")

async def auto_reply_with_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    
    user = update.message.from_user
    uid = user.id
    text = update.message.text or ""

    active_users[uid] = datetime.datetime.now()
    global current_target
    current_target = uid

    # 通知你
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🔔 新消息\n👤 {user.first_name} (@{user.username or '无'})\n🆔 `{uid}`\n💬 {text}"
    )

    # 自动回复
    caption = """您好，这边的话门槛66r，然后会送一份花嫁申鹤的私房图包

★★★★★★ 精修78p ★★★★★★

这边有图包出售 还有 图包定制
可以过门槛再交流呢

★★★★★★ 支付宝口令红包 或 微信扫码都行 ★★★★★★

收到红包后我会回复的"""

    try:
        with open(IMAGE_PATH, 'rb') as photo:
            await context.bot.send_photo(chat_id=uid, photo=InputFile(photo), caption=caption)
    except:
        await update.message.reply_text(caption)

async def owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID or not current_target:
        return
    text = update.message.text
    try:
        await context.bot.send_message(chat_id=current_target, text=text)
        await update.message.reply_text("✅ 已手动回复")
    except:
        await update.message.reply_text("❌ 发送失败")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.ChatType.PRIVATE,
        lambda u, c: owner_reply(u, c) if u.effective_user.id == OWNER_ID else auto_reply_with_image(u, c)
    ))

    print("✅ 机器人启动成功！（Token 已硬编码）")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
