import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging (helps debug if anything breaks)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("8672600900:AAE3-uxZBLkuTncdprtNV6Nmn9MKvzBn7hA")
ADMIN_ID = int(os.getenv("8273206128"))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Start"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "This bot helps you unlock rewards by completing simple steps.\n\n"
        "Click Start below to begin.",
        reply_markup=reply_markup
    )

# Handle Start button
async def start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Yes", "No"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Were you referred by someone?",
        reply_markup=reply_markup
    )

# Handle Yes/No
async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Step 1:\n"
        "Download Cardcosmic app\n"
        "Use invite code: JSEXD8\n\n"
        "🎁 Reward comes from Cardcosmic\n\n"
        "📌 Step 2:\n"
        "Send a screenshot of your dashboard after signup."
    )

# Handle screenshot
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Forward to admin
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    await update.message.reply_text(
        "✅ Screenshot received.\n"
        "Verification in progress.\n\n"
        "📢 Final Step:\n"
        "Invite 5 friends to unlock your reward."
    )

# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Start$"), start_button))
app.add_handler(MessageHandler(filters.TEXT & (filters.Regex("^Yes$") | filters.Regex("^No$")), referral))
app.add_handler(MessageHandler(filters.PHOTO, screenshot))

app.run_polling()
