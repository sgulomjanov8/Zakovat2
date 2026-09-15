import os
import re
import random
import logging
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("BOT_TOKEN", "8851685095:AAGmqCD8e-fdVh-XOaEXpPEr_ZHXvuvC6bw")

# --- RENDER UCHUN FLASK SERVER (Health Check) ---
app_web = Flask("")

@app_web.route("/")
def home():
    return "Zakovat Boti Faol Ishlamoqda!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()


# --- SAVOLLAR BAZASI (Sinflar va Mos Rasmlar Bilan) ---
QUESTIONS = [
    {
        "id": 1,
        "grade": 5,
        "q": "Suratdagi elektron qurilmalarning 'miya'si hisoblangan obyekt nima?",
        "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800",
        "hint": "Mikrosxema yoki chip",
        "a": ["mikrosxema", "chip", "protsessor"],
    },
    {
        "id": 2,
        "grade": 5,
        "q": "Dengizda suzib yurgan bu ulkan muz bo'lagi nima deyiladi?",
        "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
        "hint": "Titanik kemasi ham shunga urilgan",
        "a": ["aysberg", "muzlomi", "muz tog'i"],
    },
    {
        "id": 3,
        "grade": 6,
        "q": "Ushbu qadimiy Amfiteatr (Kolizey) qaysi shaharda joylashgan?",
        "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
        "hint": "Italiya poytaxti",
        "a": ["rim", "rome"],
    },
    {
        "id": 4,
        "grade": 6,
        "q": "Suratda ko'rsatilgan 'O'rmon qiroli' deb ataluvchi jonli nima?",
        "img": "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?w=800",
        "hint": "Yirtqich sutemizuvchi",
        "a": ["sher", "arslon", "lion"],
    },
    {
        "id": 5,
        "grade": 7,
        "q": "Ushbu mashhur va mazali meva nomini yozing.",
        "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
        "hint": "Nyu-Tonga yordam bergan meva",
        "a": ["olma", "apple"],
    },
    # Qolgan barcha 107 ta savol shu tarbiatda grade (sinf) parametri bilan joylashadi...
]


# --- YORDAMCHI FUNKSIYALAR ---
def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def check_answer(user_answer: str, correct_answers: list) -> bool:
    norm_user = normalize_text(user_answer)
    for ans in correct_answers:
        if normalize_text(ans) in norm_user:
            return True
    return False


# --- BOT MENYU VA HANDLERLARI ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """1-BOSQICH: Sinfni tanlash menyusi"""
    keyboard = [
        [InlineKeyboardButton("5-Sinf", callback_data="grade_5"), InlineKeyboardButton("6-Sinf", callback_data="grade_6")],
        [InlineKeyboardButton("7-Sinf", callback_data="grade_7"), InlineKeyboardButton("Barcha Sinflar 🌐", callback_data="grade_all")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = "🧠 **Zakovat Mantiqiy Savollar Botiga Xush Kelibsiz!**\n\nBoshlash uchun sinfni tanlang:"
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugmalar bosilganda ishlaydigan mantiq"""
    query = update.callback_query
    await query.answer()
    data = query.data

    # Sinf tanlanganda -> Savollar sonini so'rash
    if data.startswith("grade_"):
        selected_grade = data.split("_")[1]
        context.user_data["selected_grade"] = selected_grade

        keyboard = [
            [InlineKeyboardButton("5 ta savol", callback_data="count_5"), InlineKeyboardButton("10 ta savol", callback_data="count_10")],
            [InlineKeyboardButton("20 ta savol", callback_data="count_20"), InlineKeyboardButton("Barcha savollar 📚", callback_data="count_all")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"📌 Tanlandi: **{selected_grade.upper()}** sinf.\n\nEndi testda nechta savol bo'lishini tanlang:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # Savollar soni tanlanganda -> O'yinni tayyorlash va boshlash
    elif data.startswith("count_"):
        count_str = data.split("_")[1]
        grade = context.user_data.get("selected_grade", "all")

        # Sinf bo'yicha saralash
        if grade == "all":
            filtered_q = QUESTIONS.copy()
        else:
            filtered_q = [q for q in QUESTIONS if q.get("grade") == int(grade)]

        if not filtered_q:
            filtered_q = QUESTIONS.copy() # Agar ushbu sinfda savol bo'lmasa, barchasini beradi

        # Savollarni aralashtirish
        random.shuffle(filtered_q)

        # Cheklov qo'yish
        if count_str != "all":
            limit = int(count_str)
            filtered_q = filtered_q[:limit]

        context.user_data["questions"] = filtered_q
        context.user_data["current_question"] = 0
        context.user_data["score"] = 0

        await query.edit_message_text(
            text=f"🚀 **O'yin Boshlandi!**\nJami savollar soni: {len(filtered_q)} ta.\nOmad!",
            parse_mode="Markdown"
        )
        await send_question(query.message, context)


async def send_question(message, context: ContextTypes.DEFAULT_TYPE):
    """Savolni yuborish"""
    q_index = context.user_data.get("current_question", 0)
    user_questions = context.user_data.get("questions", [])

    if q_index >= len(user_questions):
        score = context.user_data.get("score", 0)
        
        # O'yin tugagach qayta boshlash tugmasi
        keyboard = [[InlineKeyboardButton("🔄 Yangi O'yin Boshlash", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            f"🎉 **O'yin yakunlandi!**\n\nSizning natijangiz: **{score}/{len(user_questions)}**",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    q_data = user_questions[q_index]
    caption = f"❓ **Savol №{q_index + 1} / {len(user_questions)}**:\n\n{q_data['q']}"

    if q_data.get("hint"):
        caption += f"\n\n💡 *Maslahat:* {q_data['hint']}"

    if q_data.get("img"):
        try:
            await message.reply_photo(photo=q_data["img"], caption=caption, parse_mode="Markdown")
        except Exception:
            await message.reply_text(caption, parse_mode="Markdown")
    else:
        await message.reply_text(caption, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Matnli javoblarni tekshirish"""
    q_index = context.user_data.get("current_question")
    user_questions = context.user_data.get("questions")

    if q_index is None or not user_questions or q_index >= len(user_questions):
        await update.message.reply_text("Yangi o'yinni boshlash uchun /start buyrug'ini bosing.")
        return

    user_text = update.message.text
    q_data = user_questions[q_index]

    if check_answer(user_text, q_data["a"]):
        context.user_data["score"] = context.user_data.get("score", 0) + 1
        await update.message.reply_text("✅ **To'g'ri javob!**", parse_mode="Markdown")
    else:
        correct_answers = ", ".join(q_data["a"])
        await update.message.reply_text(
            f"❌ **Noto'g'ri javob.**\nTo'g'ri javob(lar): *{correct_answers}*",
            parse_mode="Markdown"
        )

    context.user_data["current_question"] += 1
    await send_question(update.message, context)


# --- MAIN ---
def main():
    keep_alive()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot menyu bilan muvaffaqiyatli ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
