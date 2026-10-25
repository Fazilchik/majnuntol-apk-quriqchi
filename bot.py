import os
import sqlite3
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "").strip()
DB_PATH = "users.sqlite3"
APK_LINK = "https://promo-bot-ucad.onrender.com/r/_BL6uwm93AAItIlF9C2kbg"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

def register_user(user_id):
    with sqlite3.connect(DB_PATH) as db:
        db.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (user_id,))

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Pensiya yoshiga yetgan", callback_data="age_pension")],
        [InlineKeyboardButton("Pensiya yoshiga yetmagan", callback_data="age_under_pension")],
        [InlineKeyboardButton("Voyaga yetmagan", callback_data="underage")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        register_user(update.effective_user.id)
    await update.effective_message.reply_text(
        "Assalomu alaykum!\n\nIltimos, quyidagi bo‘limlardan birini tanlang:",
        reply_markup=menu()
    )

async def choose_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "APK Quriqchini ochish uchun quyidagi havolani bosing:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("APK Quriqchini ochish", url=APK_LINK)],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]
        ])
    )

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("Iltimos, quyidagi bo‘limlardan birini tanlang:", reply_markup=menu())

def main():
    if not TOKEN:
        raise SystemExit("BOT_TOKEN topilmadi. .env faylini yarating va tokenni kiriting.")
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(choose_age, pattern="^(age_pension|age_under_pension|underage)$"))
    print("Bot ishga tushdi. To‘xtatish uchun Ctrl+C bosing.")
    app.run_polling()

if __name__ == "__main__":
    main()
