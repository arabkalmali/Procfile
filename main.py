import logging
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# توكن البوت الذي زودتني به
BOT_TOKEN = "6881217646:AAGbR2nJQ2MYEwHWyoUhIIrHdkra5z1fB04"

# ضبط اللوجينج (اختياري لكن مفيد لتتبع الأخطاء)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة التحقق من السيشن واستخراج اسم المستخدم
def get_username_from_session(session_cookie_value):
    cookies = {
        'sessionid': session_cookie_value.strip()
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json',
    }
    try:
        response = requests.get('https://www.instagram.com/accounts/edit/', cookies=cookies, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return False, f"خطأ في الاتصال: {e}"

    if response.status_code == 200:
        text = response.text
        match = re.search(r'"username":"([^"]+)"', text)
        if match:
            return True, match.group(1)
        else:
            return False, "لم يتم العثور على اسم المستخدم في الصفحة."
    elif response.status_code in [401, 403]:
        return False, "السيشن غير صالح أو منتهي الصلاحية."
    else:
        return False, f"فشل الطلب، رمز الحالة: {response.status_code}"

# دالة استقبال رسالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أرسل لي قيمة sessionid لإنستغرام لأتحقق منها وأخبرك باسم المستخدم."
    )

# دالة استقبال الرسائل (تتعامل مع أي رسالة نصية)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session_value = update.message.text.strip()
    await update.message.reply_text("جاري التحقق من السيشن، الرجاء الانتظار...")
    valid, result = get_username_from_session(session_value)
    if valid:
        await update.message.reply_text(f"السيشن صالح.\nاسم المستخدم: {result}")
    else:
        await update.message.reply_text(f"فشل التحقق:\n{result}")

# نقطة البداية لتشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("البوت يعمل الآن...")
    app.run_polling()
