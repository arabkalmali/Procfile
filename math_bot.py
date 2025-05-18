from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from sympy import sympify
from sympy.core.sympify import SympifyError

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! أرسل لي معادلة رياضية وسأحسبها لك.")

async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        expression = update.message.text
        result = sympify(expression).evalf()
        await update.message.reply_text(f"✅ النتيجة: {result}")
    except SympifyError:
        await update.message.reply_text("⚠️ لم أفهم المعادلة. تأكد من الصيغة.")
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء الحساب.")

app = ApplicationBuilder().token("6881217646:AAEqoG67QRfW-ukCK63rtaq0g9YifW02qYw").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))

app.run_polling()
