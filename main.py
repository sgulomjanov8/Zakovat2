import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiohttp import web
from groq import Groq

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# 1. API Kalitlar va Muhit o'zgaruvchilari
BOT_TOKEN = os.getenv(
    "BOT_TOKEN", "8851685095:AAGdY98HQeT9mksQW73XO0pS7fsYYbF5GP0"
)
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY", "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"
)

# 2. Ob'ektlarni yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY)

# Xotira bazasi (Xonalar va O'yinchilar)
rooms = {}
user_room = {}
user_solved = {}


def get_user_solved(uid):
    return user_solved.get(uid, set())


# Test uchun namuna savollar bazasi
LOGICAL_QUESTIONS = [
    {
        "id": 1,
        "question": "O'zi kirmaydi, lekin hammaga yo'l ko'rsatadi. U nima?",
        "answer": "kalit",
    },
    {
        "id": 2,
        "question": "Suvda cho'kmaydi, otda o'lmaydi. U nima?",
        "answer": "muz",
    },
]


# 3. Render Web Service uchun HTTP server (24/7 ishlashi uchun)
async def handle_ping(request):
    return web.Response(text="Bot is running 24/7!")


# 4. Groq AI orqali matnni formatlash funksiyasi
def format_rules_with_groq(text: str) -> str:
    """Groq AI orqali qoidalar va nizomni chiroyli ko'rinishga keltirish"""
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Ushbu Telegram o'yin qoidalaridagi keraksiz chalkashliklarni tozalab, "
                        "Telegram Markdown formatida (qalin matnlar uchun ** foydalanib) "
                        f"chiroyli, ta'sirli va o'qishga qulay ko'rinishga keltirib ber:\n\n{text}"
                    ),
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Groq API xatoligi: {e}")
        return text


# 5. Handlerlar (Buyruqlar va Tugmalar)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="➕ Yangi Xona Yaratish")],
            [types.KeyboardButton(text="🚀 O'yinni Boshlash")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "👋 **Zakovat Quiz Botiga xush kelibsiz!**\n\nO'yinni boshlash uchun quyidagi tugmalardan birini tanlang:",
        reply_markup=kb,
        parse_mode="Markdown",
    )


@dp.message(F.text == "➕ Yangi Xona Yaratish")
@dp.message(Command("game"))
async def create_room(message: types.Message):
    user_id = message.from_user.id
    room_id = f"room_{user_id}"

    rooms[room_id] = {
        "captain": user_id,
        "members": {user_id: message.from_user.full_name},
        "class": "7-sinf",
        "question_count": 5,
        "questions": [],
        "is_started": False,
        "is_group": False,
        "chat_id": message.chat.id,
    }
    user_room[user_id] = room_id

    await message.answer(
        f"✨ **Yangi xona yaratildi!**\n\n"
        f"👤 **Kapitan:** {message.from_user.full_name}\n"
        f"⚙️ **Sozlama:** 7-sinf, 5 ta savol.\n\n"
        f"O'yinni boshlash uchun **🚀 O'yinni Boshlash** tugmasini bosing!",
        parse_mode="Markdown",
    )


@dp.message(F.text == "🚀 O'yinni Boshlash")
@dp.message(Command("startgame"))
async def start_game(message: types.Message):
    user_id = message.from_user.id
    room_id = user_room.get(user_id)

    if not room_id or room_id not in rooms:
        await message.answer(
            "⚠️ Iltimos, avval **➕ Yangi Xona Yaratish** tugmasini bosing!",
            parse_mode="Markdown",
        )
        return

    room = rooms[room_id]

    if user_id != room["captain"]:
        await message.answer(
            "⚠️ O'yinni faqat xonani yaratgan **Kapitan** boshlay oladi!",
            parse_mode="Markdown",
        )
        return

    # Savollarni tayyorlash
    all_solved = set()
    for uid in room["members"].keys():
        all_solved.update(get_user_solved(uid))

    available_questions = [
        q for q in LOGICAL_QUESTIONS if q.get("id") not in all_solved
    ]

    if len(available_questions) < room["question_count"]:
        available_questions = LOGICAL_QUESTIONS.copy()

    random.shuffle(available_questions)
    room["questions"] = available_questions[: room["question_count"]]
    room["is_started"] = True

    members_count = len(room["members"])
    members_text = ", ".join(
        [f"**{name}**" for name in room["members"].values()]
    )

    raw_rules_text = (
        f"📜 **ZAKOVAT O'YINI QOIDALARI VA NIZOMI:**\n\n"
        f"🎯 **Kategoriya:** {room['class']}\n"
        f"🔢 **Savollar soni:** {room['question_count']} ta\n"
        f"👥 **Qatnashchilar ({members_count} kishi):** {members_text}\n\n"
        f"🏆 **Ball berish tartibi:**\n"
        f"🥇 **1-bo'lib to'g'ri javob bergan o'yinchi:** 2 Ball\n"
        f"🥈 **Keyingi to'g'ri javob berganlar:** 1 Ball\n\n"
        f"🚀 **O'yin tez orada boshlanadi. Muvaffaqiyat tilaymiz!**"
    )

    # Groq AI orqali matnni chiroyli formatlash
    await message.answer("🤖 *Groq AI qoidalarni formatlamoqda...*", parse_mode="Markdown")
    rules_text = format_rules_with_groq(raw_rules_text)

    await message.answer(rules_text, parse_mode="Markdown")


# 6. Asosiy ishga tushirish funksiyasi
async def main():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logging.info(f"Port {port} da Web Server va Bot ishga tushdi!")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
