from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
CHANNEL_LINK = "https://t.me/Ani_Major"

# Anime ma'lumotlari (keyin admin fayllarni qo'shadi)
anime_list = [
    {"title": "Anime 1", "file": "anime1.mp4"},
    {"title": "Anime 2", "file": "anime2.mp4"}
]

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"Salom! Hurmat bilan AniMajorBotga xush kelibsiz!\n\n"
        f"Iltimos, kanalimizga obuna bo'ling: {CHANNEL_LINK}"
    )

# Admin banner yuborish (kanalga)
async def send_banner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Faqat admin foydalanishi mumkin.")
        return

    # Inline tugma yaratish
    button = InlineKeyboardButton("Animeni ko'rish", callback_data="watch_anime")
    keyboard = InlineKeyboardMarkup([[button]])

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="Yangi banner! 🎬",
        reply_markup=keyboard
    )
    await update.message.reply_text("Banner kanalga yuborildi ✅")

# Inline tugma bosilganda anime yuborish
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    await context.bot.send_message(chat_id=user_id, text="Animeni boshlaymiz 🎥")

    for anime in anime_list:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"Endi tomosha qiling: {anime['title']}")
            # Faylni yuborish (keyin admin fayl yuklaydi)
            # await context.bot.send_video(chat_id=user_id, video=open(anime['file'], 'rb'))
        except:
            await context.bot.send_message(chat_id=user_id, text="Xato yuz berdi!")

# Bot ishga tushirish
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("send_banner", send_banner))
app.add_handler(CallbackQueryHandler(button_callback))

print("AniMajorBot ishga tushdi ✅")
app.run_polling()
