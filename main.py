import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web
from groq import Groq

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# API Kalitlar
BOT_TOKEN = os.getenv(
    "BOT_TOKEN", "8851685095:AAGdY98HQeT9mksQW73XO0pS7fsYYbF5GP0"
)
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY", "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"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY)

# Ma'lumotlar xotirasi
rooms = {}
user_room = {}
user_solved = {}


def get_user_solved(uid):
    return user_solved.get(uid, set())


# RASMLI VA MATNLI SAVOLLAR BAZASI
LOGICAL_QUESTIONS = [
    {
        "id": 1,
        "question": "Ushbu suratdagi obyektni va uning mantiqiy ma'nosini toping?",
        "photo": "https://picsum.photos/800/600",  # Savol rasmining havolasi
        "answer": "bayroq",
    },
    {
        "id": 2,
        "question": "O'zi kirmaydi, lekin hammaga yo'l ko'rsatadi. U nima?",
        "photo": None,
        "answer": "kalit",
    },
    {
        "id": 3,
        "question": "Suvda cho'kmaydi, otda o'lmaydi. U nima?",
        "photo": None,
        "answer": "muz",
    },
]


# Render uchun Web Server (24/7 Live uchun)
async def handle_ping(request):
    return web.Response(text="Bot is running 24/7!")


# Groq AI orqali qoidalarni formatlash
def format_rules_with_groq(text: str) -> str:
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Ushbu Telegram o'yin qoidalaridagi keraksiz chalkashliklarni tozalab, "
                        "Telegram Markdown formatida (qalin matnlar uchun ** foydalanib) "
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


# SAVOLNI YUBORISH (RASMLI YOKI MATNLI)
async def send_question(room_id):
    if room_id not in rooms:
        return
    room = rooms[room_id]

    if not room["questions"]:
        await bot.send_message(
            room["chat_id"],
            "🏁 **O'yin o'z nihoyasiga yetdi! Qatnashganingiz uchun rahmat.**",
            parse_mode="Markdown",
        )
        return

    current_q = room["questions"].pop(0)
    q_text = f"❓ **SAVOL:**\n\n{current_q['question']}\n\n⏱ Javob berish uchun 1 daqiqa 50 soniya bor!"
    photo_url = current_q.get("photo")

    targets = (
        [room["chat_id"]]
        if room["is_group"]
        else list(room["members"].keys())
    )

    for target in targets:
        try:
            if photo_url:
                # Agar savolda rasm bo'lsa, rasm bilan yuboradi
                await bot.send_photo(
                    chat_id=target,
                    photo=photo_url,
                    caption=q_text,
                    parse_mode="Markdown",
                )
            else:
                # Agar rasm bo'lmasa, faqat matn yuboradi
                await bot.send_message(
                    chat_id=target, text=q_text, parse_mode="Markdown"
                )
        except Exception as e:
            logging.error(f"Xabar yuborishda xatolik ({target}): {e}")


# Handlers
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
        "👋 **Zakovat Quiz Botiga xush kelibsiz!**",
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
        "is_group": message.chat.type != "private",
        "chat_id": message.chat.id,
    }
    user_room[user_id] = room_id

    class_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="5-sinf", callback_data="setclass_5-sinf"
                ),
                InlineKeyboardButton(
                    text="6-sinf", callback_data="setclass_6-sinf"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="7-sinf", callback_data="setclass_7-sinf"
                ),
                InlineKeyboardButton(
                    text="8-sinf", callback_data="setclass_8-sinf"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="9-sinf", callback_data="setclass_9-sinf"
                ),
                InlineKeyboardButton(
                    text="10-sinf", callback_data="setclass_10-sinf"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="11-sinf", callback_data="setclass_11-sinf"
                )
            ],
        ]
    )

    invite_url = f"https://t.me/MY_Zakovat_Quiz_Bot?start={room_id}"
    await message.answer(
        f"✨ **Yangi xona yaratildi!**\n\n"
        f"👤 **Kapitan:** {message.from_user.full_name}\n"
        f"🔗 **Do'stlarni taklif qilish:** {invite_url}\n\n"
        f"📌 **Sinfni tanlang:**",
        reply_markup=class_kb,
        parse_mode="Markdown",
    )


@dp.callback_query(F.data.startswith("setclass_"))
async def process_class_select(callback: types.CallbackQuery):
    selected_class = callback.data.split("_")[1]
    user_id = callback.from_user.id
    room_id = user_room.get(user_id)

    if room_id in rooms:
        rooms[room_id]["class"] = selected_class

    count_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="5 ta savol", callback_data="setcount_5"
                ),
                InlineKeyboardButton(
                    text="10 ta savol", callback_data="setcount_10"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="15 ta savol", callback_data="setcount_15"
                )
            ],
        ]
    )
    await callback.message.edit_text(
        f"✅ Sinf: **{selected_class}** tanlandi.\n\n🔢 **Endi savollar sonini belgilang:**",
        reply_markup=count_kb,
        parse_mode="Markdown",
    )


@dp.callback_query(F.data.startswith("setcount_"))
async def process_count_select(callback: types.CallbackQuery):
    count = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    room_id = user_room.get(user_id)

    if room_id in rooms:
        rooms[room_id]["question_count"] = count

    await callback.message.edit_text(
        f"⚙️ **Sozlamalar saqlandi!**\n\n"
        f"📚 Sinf: **{rooms[room_id]['class']}**\n"
        f"🔢 Savollar soni: **{count} ta**\n\n"
        f"Tayyor bo'lsangiz, **🚀 O'yinni Boshlash** tugmasini bosing!",
        parse_mode="Markdown",
    )


@dp.message(F.text == "🚀 O'yinni Boshlash")
@dp.message(Command("startgame"))
async def start_game(message: types.Message):
    user_id = message.from_user.id
    room_id = user_room.get(user_id)

    if not room_id or room_id not in rooms:
        await message.answer(
            "⚠️ Iltimos, **➕ Yangi Xona Yaratish** tugmasi orqali xona yarating!",
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
        f"🚀 **O'yin 5 soniyadan so'ng boshlanadi. Muvaffaqiyat tilaymiz!**"
    )

    rules_text = format_rules_with_groq(raw_rules_text)
    await message.answer(rules_text, parse_mode="Markdown")

    # 5 soniya kutib, birinchi savolni yuborish (rasmli bo'lsa rasmi bilan)
    await asyncio.sleep(5)
    await send_question(room_id)


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
