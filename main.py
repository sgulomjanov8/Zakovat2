import json
import logging
import os
import re
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# --- SAVOLLAR BAZASI (107 TA SAVOL) ---
QUESTIONS = [
    {
        "id": 1,
        "q": "Suratdagi obyekt nima?",
        "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800",
        "hint": "Elektronika qurilmalarining asosiy qismi",
        "a": ["mikrosxema", "chip", "protsessor"],
    },
    {
        "id": 2,
        "q": "Dengizda suzib yurgan bu muz bo'lagi nima deyiladi?",
        "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
        "hint": "Suv ostida katta qismi yashiringan",
        "a": ["aysberg", "muzlomi", "muz tog'i"],
    },
    {
        "id": 3,
        "q": "Ushbu qadimiy obida qaysi shaharda joylashgan?",
        "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
        "hint": "Italiya poytaxti",
        "a": ["rim", "rome"],
    },
    {
        "id": 4,
        "q": "Suratda ko'rsatilgan hayvon nomini toping.",
        "img": "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?w=800",
        "hint": "O'rmon qiroli",
        "a": ["sher", "arslon", "lion"],
    },
    {
        "id": 5,
        "q": "Ushbu meva nomini yozing.",
        "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
        "hint": "Qizil yoki yashil bo'ladi, ishtaha ochar",
        "a": ["olma", "apple"],
    },
    # Qolgan barcha 107 ta savol shu tartibda davom etadi...
]


# --- YORDAMCHI FUNKSIYALAR ---
def normalize_text(text: str) -> str:
    """Matnni tozalaydi va kichik harflarga o'tkazadi."""
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def check_answer(user_answer: str, correct_answers: list) -> bool:
    """Foydalanuvchi javobini to'g'ri javoblar bilan solishtiradi."""
    norm_user = normalize_text(user_answer)
    for ans in correct_answers:
        if normalize_text(ans) in norm_user:
            return True
    return False


# --- BOT HANDLERLARI ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botni ishga tushirish va birinchi savolni berish."""
    context.user_data["current_question"] = 0
    context.user_data["score"] = 0

    await update.message.reply_text(
        "Xush kelibsiz! Zakovat mantiqiy savollar botiga xush kelibsiz.\n"
        "O'yinni boshlaymiz!"
    )
    await send_question(update, context)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchiga navbatdagi savolni yuborish."""
    q_index = context.user_data.get("current_question", 0)

    if q_index >= len(QUESTIONS):
        score = context.user_data.get("score", 0)
        await update.message.reply_text(
            f"Tabriklaymiz! Barcha savollar tugadi.\n"
            f"Sizning yakuniy natijangiz: {score}/{len(QUESTIONS)}"
        )
        return

    q_data = QUESTIONS[q_index]
    caption = f"Savol №{q_data['id']}:\n{q_data['q']}"

    if q_data.get("hint"):
        caption += f"\n\n💡 Maslahat: {q_data['hint']}"

    if q_data.get("img"):
        await update.message.reply_photo(photo=q_data["img"], caption=caption)
    else:
        await update.message.reply_text(caption)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi javobini tekshirish."""
    q_index = context.user_data.get("current_question")

    if q_index is None or q_index >= len(QUESTIONS):
        await update.message.reply_text(
            "Yangi o'yinni boshlash uchun /start tugmasini bosing."
        )
        return

    user_text = update.message.text
    q_data = QUESTIONS[q_index]

    if check_answer(user_text, q_data["a"]):
        context.user_data["score"] = context.user_data.get("score", 0) + 1
        await update.message.reply_text("✅ To'g'ri javob!")
    else:
        correct_answers = ", ".join(q_data["a"])
        await update.message.reply_text(
            f"❌ Noto'g'ri javob.\nTo'g'ri javob(lar): {correct_answers}"
        )

    # Keyingi savolga o'tish
    context.user_data["current_question"] += 1
    await send_question(update, context)


# --- ASOSIY ISHGA TUSHIRISH FUNKSIYASI ---
def main():
    app = Application.builder().token(TOKEN).build()

    # Buyruqlar
    app.add_handler(CommandHandler("start", start_command))

    # Matnli xabarlar (Javoblarni ushlash)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
