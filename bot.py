
import os
import sqlite3
import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "").strip()

DB_DIR = os.environ.get("DATA_DIR", ".")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "users.sqlite3")

APK_LINK = "https://promo-bot-ucad.onrender.com/r/_BL6uwm93AAItIlF9C2kbg"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)


# Ma'lumotlar bazasi
def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def register_user(user_id):
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)",
            (user_id,),
        )


# Asosiy menyu
def menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👴 Pensiya yoshiga yetganlar",
                callback_data="age_pension",
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Pensiya yoshiga yetmaganlar",
                callback_data="age_under_pension",
            )
        ],
        [
            InlineKeyboardButton(
                "🧒 Voyaga yetmaganlar",
                callback_data="underage",
            )
        ],
    ])


# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        register_user(update.effective_user.id)

    text = (
        "🛡️ MAJNUNTOL APK QURIQCHI\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Assalomu alaykum! 👋\n\n"
        "Botimizga xush kelibsiz!\n"
        "Davom etish uchun o'zingizga mos bo'limni tanlang 👇"
    )

    await update.effective_message.reply_text(
        text,
        reply_markup=menu(),
    )


# Yosh bo'limini tanlash
async def choose_age(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    q = update.callback_query
    await q.answer()

    text = (
        "📱 APK QURIQCHI\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Tanlangan bo'lim uchun xizmatni ochish uchun "
        "quyidagi tugmani bosing.\n\n"
        "🔐 Davom etish uchun tugmani tanlang 👇"
    )

    await q.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📲 APK Quriqchini ochish",
                    url=APK_LINK,
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Orqaga",
                    callback_data="back",
                )
            ],
        ]),
    )


# Asosiy menyuga qaytish
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    await q.edit_message_text(
        "🛡️ MAJNUNTOL APK QURIQCHI\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Davom etish uchun o'zingizga mos bo'limni tanlang 👇",
        reply_markup=menu(),
    )


# Render uchun HTTP server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Majnuntol APK Quriqchi is running"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format, *args):
        pass


def start_web_server():
    port = int(os.environ.get("PORT", "10000"))

    server = ThreadingHTTPServer(
        ("0.0.0.0", port),
        HealthHandler,
    )

    logging.info("HTTP server %s-portda ishga tushdi", port)
    server.serve_forever()


# Botni ishga tushirish
def main():
    if not TOKEN:
        raise SystemExit(
            "BOT_TOKEN topilmadi. Render Environment sozlamalarini tekshiring."
        )

    init_db()

    threading.Thread(
        target=start_web_server,
        daemon=True,
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(back, pattern="^back$")
    )
    app.add_handler(
        CallbackQueryHandler(
            choose_age,
            pattern="^(age_pension|age_under_pension|underage)$",
        )
    )

    print("Majnuntol APK Quriqchi ishga tushdi.")
    app.run_polling()


if __name__ == "__main__":
    main()
