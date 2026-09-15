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


# 3. Render Web Service uchun soxta HTTP server
async def handle_ping(request):
    return web.Response(text="Bot is running 24/7!")


# 4. Groq AI orqali matnni formatlash funksiyasi
def format_rules_with_groq(text: str) -> str:
    """Groq API orqali qoidalar matnini tozalash va chiroyli shaklga keltirish funksiyasi"""
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Ushbu Telegram o'yin qoidalaridagi keraksiz chalkashliklarni tozalab, "
                        "Telegram Markdown formatida (qalin matnlar uchun ** dan foydalanib) "
                        f"chiroyli va o'qishga qulay ko'rinishga keltirib ber:\n\n{text}"
                    ),
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Groq API xatoligi: {e}")
        return text


# 5. Handlerlar
@dp.message(F.text == "🚀 O'yinni Boshlash")
@dp.message(Command("startgame"))
async def start_game(message: types.Message):
    user_id = message.from_user.id
    room_id = user_room.get(user_id)

    if not room_id or room_id not in rooms:
        await message.answer(
            "⚠️ Iltimos, /start yoki /game buyrug'i orqali yangi xona yarating!"
        )
        return

    room = rooms[room_id]

    if user_id != room["captain"]:
        await message.answer(
            "⚠️ O'yinni faqat xonani yaratgan **Kapitan** boshlay oladi!",
            parse_mode="Markdown",
        )
        return

    # --- HAR SAFAR HAR XIL (RANDOM) VA YECHILMAGAN SAVOLLARNI TANLASH ---
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
        f"🥈 **2, 3, 4, 5...-bo'lib to'g'ri javob berganlar:** 1 Ball\n\n"
        f"⏱ **Vaqt:** Har bir savol uchun 1 daqiqa 50 soniya beriladi.\n"
        f"🤫 Javobingizni chatga yozing, vaqt tugagach yoki hamma javob berib bo'lgach natija e'lon qilinadi!\n\n"
        f"🚀 **O'yin 5 soniyadan so'ng boshlanadi. Muvaffaqiyat tilaymiz!**"
    )

    rules_text = format_rules_with_groq(raw_rules_text)

    if room["is_group"]:
        await bot.send_message(
            room["chat_id"], rules_text, parse_mode="Markdown"
        )
    else:
        for m_id in room["members"].keys():
            await bot.send_message(m_id, rules_text, parse_mode="Markdown")

    await asyncio.sleep(5)
    await send_question(room_id)


# 6. Asosiy ishga tushirish funksiyasi
async def main():
    # Render bergan Port'da aiohttp serverini parallel ishga tushiramiz
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logging.info(f"Port {port} da Web Server ishga tushdi!")
    logging.info("Bot Render'da muvaffaqiyatli ishlayapti!")

    # Webhook'ni tozalash va polling'ni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
