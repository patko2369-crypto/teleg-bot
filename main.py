import os
import re
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("8816935387:AAGQZt0s_TmF4XIYaTTM8euuu_rhI4yoo3s")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ ربات چکر یوزرنیم\n\n"
        "لیست یوزرنیم‌ها رو بفرست (مثال: @avazi, chobi)"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("/start"):
        return
    
    if ',' in text:
        raw = text.split(',')
    else:
        raw = text.split('\n')
    
    usernames = []
    for item in raw:
        item = item.strip().lstrip('@')
        if item and len(item) >= 5 and item not in usernames:
            usernames.append(item)
    
    if not usernames:
        await update.message.reply_text("❌ یوزرنیم معتبر پیدا نشد")
        return
    
    await update.message.reply_text(f"🔍 بررسی {len(usernames)} یوزرنیم...")
    
    available = []
    for u in usernames:
        try:
            r = requests.get(f"https://t.me/{u}", timeout=8)
            if "If you have Telegram, you can contact" in r.text:
                available.append(u)
                await update.message.reply_text(f"✅ @{u} آزاد")
            else:
                await update.message.reply_text(f"❌ @{u} گرفته")
        except:
            await update.message.reply_text(f"⚠️ @{u} خطا")
    
    if available:
        msg = "✅ آزادها:\n" + "\n".join([f"@{x}" for x in available])
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ هیچ آزادی پیدا نشد")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check))
    print("🤖 ربات روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
