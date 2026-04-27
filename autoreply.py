from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import datetime
import os

# ================== Railway 配置 ==================
TOKEN = os.getenv("TOKEN")                    # ← 从 Railway Variables 读取
OWNER_ID = int(os.getenv("OWNER_ID", "8260959315"))

# 图片文件名（必须和上传到 GitHub 的图片文件名一致）
IMAGE_PATH = "synt.png"

active_users = {}
current_target = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 很高兴接待您～\n有需要随时说")

async def auto_reply_with_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    
    user = update.message.from_user
    uid = user.id
    text = update.message.text or ""

    active_users[uid] = datetime.datetime.now()
    global current_target
    current_target = uid

    # 通知主人
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🔔 新消息\n"
             f"👤 {user.first_name} (@{user.username or '无'})\n"
             f"🆔 `{uid}`\n"
             f"💬 {text}"
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
    except Exception as e:
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

    print("✅ 机器人已在 Railway 启动！")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
