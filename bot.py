import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
TOKEN = os.geten(BOT_TOKEN)
# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔢 عدد اول هست؟", callback_data="prime")],
        [InlineKeyboardButton("⚖️ زوج یا فرد؟", callback_data="even_odd")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام 👋\nیکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=reply_markup
    )

# ---------- دکمه‌ها ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "prime":
        context.user_data["mode"] = "prime"
        await query.message.reply_text("یک عدد بفرست تا بگم عدد اوله یا نه 🔢")

    elif query.data == "even_odd":
        context.user_data["mode"] = "even_odd"
        await query.message.reply_text("یک عدد بفرست تا بگم زوجه یا فرد ⚖️")

# ---------- دریافت عدد ----------
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        await update.message.reply_text("❌ لطفاً فقط عدد بفرست")
        return

    num = int(update.message.text)
    mode = context.user_data.get("mode")

    if mode == "prime":
        if num < 2:
            await update.message.reply_text("❌ عدد اول نیست")
            return

        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                await update.message.reply_text("❌ عدد اول نیست")
                return

        await update.message.reply_text("✅ عدد اول است")

    elif mode == "even_odd":
        if num % 2 == 0:
            await update.message.reply_text("✅ عدد زوج است")
        else:
            await update.message.reply_text("✅ عدد فرد است")

# ---------- اجرای ربات ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))

app.run_polling()
