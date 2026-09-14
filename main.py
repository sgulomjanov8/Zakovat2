import asyncio
import logging
import random
import sqlite3
import uuid
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

# Savollarni alohida questions.py faylidan yuklaymiz
from questions import LOGICAL_QUESTIONS

BOT_TOKEN = "8851685095:AAFAZIWW0kRKnj7cXL3mSkzkwVww5cB_V-E"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- BAZA (SQLite) ---
def init_db():
    conn = sqlite3.connect("zakovat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            score INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solved_questions (
            user_id INTEGER,
            question_id INTEGER,
            PRIMARY KEY (user_id, question_id)
        )
    """)
    conn.commit()
    conn.close()

def add_score(user_id: int, full_name: str, points: int):
    conn = sqlite3.connect("zakovat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE users SET score = ?, full_name = ? WHERE user_id = ?", (row[0] + points, full_name, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, full_name, score) VALUES (?, ?, ?)", (user_id, full_name, points))
    conn.commit()
    conn.close()

def get_top_players(limit=10):
    conn = sqlite3.connect("zakovat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, score FROM users ORDER BY score DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_user_solved(user_id: int):
    conn = sqlite3.connect("zakovat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question_id FROM solved_questions WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def mark_question_solved(user_ids: list, question_id: int):
    conn = sqlite3.connect("zakovat.db")
    cursor = conn.cursor()
    for uid in user_ids:
        cursor.execute("INSERT OR IGNORE INTO solved_questions (user_id, question_id) VALUES (?, ?)", (uid, question_id))
    conn.commit()
    conn.close()

init_db()

rooms = {}
user_room = {}

def classes_keyboard():
    builder = InlineKeyboardBuilder()
    for c in ["5-sinf", "6-sinf", "7-sinf", "8-sinf", "9-sinf", "10-sinf", "11-sinf"]:
        builder.button(text=c, callback_data=f"class_{c}")
    builder.adjust(2)
    return builder.as_markup()

def count_keyboard():
    builder = InlineKeyboardBuilder()
    for n in [3, 5, 7, 10]:
        builder.button(text=f"❓ {n} ta savol", callback_data=f"count_{n}")
    builder.adjust(2)
    return builder.as_markup()

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="➕ Yangi Xona Yaratish")
    builder.button(text="🚀 O'yinni Boshlash")
    builder.button(text="🏆 Top Bilimdonlar")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- HANDLERLAR ---
@dp.message(CommandStart())
@dp.message(Command("game"))
async def start_cmd(message: types.Message, command: CommandObject = None):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    chat_type = message.chat.type
    chat_id = message.chat.id
    args = command.args if command else None

    if chat_type in ["group", "supergroup"]:
        room_id = f"group_{chat_id}"
        if room_id not in rooms:
            rooms[room_id] = {
                "captain": user_id,
                "members": {user_id: user_name},
                "class": "6-sinf",
                "question_count": 5,
                "questions": [],
                "q_idx": 0,
                "scores": {},
                "answers": [],
                "hint_used": False,
                "active_messages": {},
                "is_started": False,
                "is_group": True,
                "chat_id": chat_id,
                "evaluated": False
            }
        else:
            rooms[room_id]["members"][user_id] = user_name

        user_room[user_id] = room_id
        members_list = "\n".join([f"👤 **{name}**" for name in rooms[room_id]["members"].values()])

        await message.answer(
            f"🎉 **Guruhda Zakovat xonasi aktivlashtirildi!**\n\n"
            f"👥 **A'zolar ro'yxati:**\n{members_list}\n\n"
            f"Sinfni tanlang:",
            reply_markup=classes_keyboard()
        )
        return

    if args and args.startswith("room_"):
        room_id = args
        if room_id in rooms:
            room = rooms[room_id]
            if room["is_started"]:
                await message.answer("⚠️ Ushbu xonada o'yin allaqachon boshlanib ketgan!", reply_markup=main_menu())
                return

            room["members"][user_id] = user_name
            user_room[user_id] = room_id

            members_list = "\n".join([
                f"👑 **{name} (Kapitan)**" if uid == room["captain"] else f"👤 **{name}**" 
                for uid, name in room["members"].items()
            ])

            for m_id in room["members"].keys():
                await bot.send_message(
                    m_id,
                    f"🎉 **{user_name}** jamoaga qo'shildi!\n\n"
                    f"👥 **Xonadagi a'zolar ({len(room['members'])} kishi):**\n{members_list}\n\n"
                    f"Kapitan sozlamalarni tanlab, **🚀 O'yinni Boshlash** tugmasini bosishi mumkin!",
                    reply_markup=main_menu()
                )
            return
        else:
            await message.answer("⚠️ Havola eskirgan yoki xona topilmadi.")

    room_id = f"room_{uuid.uuid4().hex[:8]}"
    rooms[room_id] = {
        "captain": user_id,
        "members": {user_id: user_name},
        "class": "6-sinf",
        "question_count": 5,
        "questions": [],
        "q_idx": 0,
        "scores": {},
        "answers": [],
        "hint_used": False,
        "active_messages": {},
        "is_started": False,
        "is_group": False,
        "evaluated": False
    }
    user_room[user_id] = room_id

    bot_info = await bot.get_me()
    invite_link = f"https://t.me/{bot_info.username}?start={room_id}"

    await message.answer(
        f"🧠 **Zakovat Botiga Xush Kelibsiz, {user_name}!**\n\n"
        f"👤 **Sizning ismingiz:** {user_name}\n"
        f"🔗 **Do'stlaringizni taklif qilish havolasi:**\n"
        f"`{invite_link}`\n\n"
        f"👇 **Sinf va Savollar sonini tanlang:**",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
    await message.answer("🎓 **Sinfni tanlang:**", reply_markup=classes_keyboard())

@dp.message(F.text == "➕ Yangi Xona Yaratish")
async def create_new_room(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    room_id = f"room_{uuid.uuid4().hex[:8]}"
    rooms[room_id] = {
        "captain": user_id,
        "members": {user_id: user_name},
        "class": "6-sinf",
        "question_count": 5,
        "questions": [],
        "q_idx": 0,
        "scores": {},
        "answers": [],
        "hint_used": False,
        "active_messages": {},
        "is_started": False,
        "is_group": False,
        "evaluated": False
    }
    user_room[user_id] = room_id

    bot_info = await bot.get_me()
    invite_link = f"https://t.me/{bot_info.username}?start={room_id}"

    await message.answer(
        f"✨ **Yangi xona yaratildi!**\n\n"
        f"👤 **Kapitan:** {user_name}\n"
        f"🔗 **Do'stlarga yuborish uchun havola:**\n"
        f"`{invite_link}`\n\n"
        f"🎓 Sinf va Savollar sonini belgilang:",
        reply_markup=classes_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("class_"))
async def process_class_selection(callback: types.CallbackQuery):
    selected_class = callback.data.split("_")[1]
    user_id = callback.from_user.id
    room_id = user_room.get(user_id)

    if room_id and room_id in rooms:
        rooms[room_id]["class"] = selected_class
        await callback.message.edit_text(
            f"✅ Siz **{selected_class}** kategoriyasini tanladingiz!\n\n"
            f"❓ Endi xonada nechta savol bo'lishini tanlang:",
            reply_markup=count_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("⚠️ Avval /start bosing!")

@dp.callback_query(F.data.startswith("count_"))
async def process_count_selection(callback: types.CallbackQuery):
    count = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    room_id = user_room.get(user_id)

    if room_id and room_id in rooms:
        rooms[room_id]["question_count"] = count
        await callback.message.edit_text(
            f"✅ Savollar soni **{count} ta** qilib belgilandi!\n\n"
            f"Tayyor bo'lsangiz, **🚀 O'yinni Boshlash** tugmasini bosing.",
            parse_mode="Markdown"
        )
    else:
        await callback.answer("⚠️ Avval /start bosing!")

@dp.message(F.text == "🚀 O'yinni Boshlash")
@dp.message(Command("startgame"))
async def start_game(message: types.Message):
    user_id = message.from_user.id
    room_id = user_room.get(user_id)

    if not room_id or room_id not in rooms:
        await message.answer("⚠️ Iltimos, /start yoki /game buyrug'i orqali yangi xona yarating!")
        return

    room = rooms[room_id]

    if user_id != room["captain"]:
        await message.answer("⚠️ O'yinni faqat xonani yaratgan **Kapitan** boshlay oladi!")
        return

    all_solved = set()
    for uid in room["members"].keys():
        all_solved.update(get_user_solved(uid))

    available_questions = [q for q in LOGICAL_QUESTIONS if q.get("id") not in all_solved]

    if len(available_questions) < room["question_count"]:
        available_questions = LOGICAL_QUESTIONS.copy()

    random.shuffle(available_questions)
    room["questions"] = available_questions[:room["question_count"]]

    room["is_started"] = True
    members_count = len(room["members"])
    members_text = ", ".join([f"**{name}**" for name in room["members"].values()])

    rules_text = (
        f"📜 **ZAKOVAT O'YINI QOIDALARI VA NIZOMI:**\n\n"
        f"🎯 **Kategoriya:** {room['class']}\n"
        f"🔢 **Savollar soni:** {room['question_count']} ta\n"
        f"👥 **Qatnashchilar ({members_count} kishi):** {members_text}\n\n"
        f"🏆 **Ball berish tartibi:**\n"
        f"🥇 **1-bo'lib to'g'ri javob bergan o'yinchi:** 2 Ball\n"
        f"🥈 **2, 3, 4, 5...-bo'lib to'g'ri javob berganlar:** 1 Ball\n\n"
        f"⏱ **Vaqt:** Har bir savol uchun 1 daqiqa 50 soniya beriladi.\n"
        f"🤫 Javobingizni chatga yozing, vaqt tugagach yoki hamma javob berib bo'lgach natija e'lon qilinadi!\n\n"
        f"🚀 *O'yin 5 soniyadan so'ng boshlanadi. Muvaffaqiyat tilaymiz!*"
    )

    if room["is_group"]:
        await bot.send_message(room["chat_id"], rules_text, parse_mode="Markdown")
    else:
        for m_id in room["members"].keys():
            await bot.send_message(m_id, rules_text, parse_mode="Markdown")

    await asyncio.sleep(5)
    await send_question(room_id)

async def send_question(room_id: str):
    room = rooms.get(room_id)
    if not room:
        return

    q_idx = room["q_idx"]
    questions = room["questions"]

    if q_idx >= len(questions):
        await finish_game(room_id)
        return

    q_data = questions[q_idx]
    room["answers"] = []
    room["hint_used"] = False
    room["active_messages"] = {}
    room["evaluated"] = False

    caption_text = (
        f"❓ **{q_idx + 1}-SAVOL (jami {len(questions)} ta):**\n\n"
        f"{q_data['q']}\n\n"
        f"⏱ **Qolgan vaqt:** 01:50\n\n"
        f"✍️ *Javobingizni chatga yozib yuboring!*"
    )

    if room["is_group"]:
        msg = await bot.send_photo(
            chat_id=room["chat_id"],
            photo=q_data["image"],
            caption=caption_text
        )
        room["active_messages"][room["chat_id"]] = msg.message_id
    else:
        for m_id in room["members"].keys():
            msg = await bot.send_photo(
                chat_id=m_id,
                photo=q_data["image"],
                caption=caption_text
            )
            room["active_messages"][m_id] = msg.message_id

    asyncio.create_task(question_timer(room_id, q_idx))

async def question_timer(room_id: str, q_idx: int):
    total_seconds = 110
    step = 10

    while total_seconds > 0:
        await asyncio.sleep(step)
        total_seconds -= step

        room = rooms.get(room_id)
        if not room or room["q_idx"] != q_idx or room["evaluated"]:
            return

        if total_seconds == 50 and not room["hint_used"]:
            room["hint_used"] = True
            q_data = room["questions"][q_idx]
            hint_msg = f"💡 **Maslahat:**\n{q_data['hint']}"
            if room["is_group"]:
                await bot.send_message(room["chat_id"], hint_msg)
            else:
                for m_id in room["members"].keys():
                    await bot.send_message(m_id, hint_msg)

        mins, secs = divmod(total_seconds, 60)
        time_str = f"{mins:02d}:{secs:02d}"

        q_data = room["questions"][q_idx]
        for c_id, msg_id in room["active_messages"].items():
            caption_text = (
                f"❓ **{q_idx + 1}-SAVOL (jami {len(room['questions'])} ta):**\n\n"
                f"{q_data['q']}\n\n"
                f"⏱ **Qolgan vaqt:** {time_str}"
            )
            try:
                await bot.edit_message_caption(chat_id=c_id, message_id=msg_id, caption=caption_text)
            except TelegramBadRequest:
                pass

    await evaluate_answers(room_id)

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_user_answers(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    chat_type = message.chat.type

    if chat_type in ["group", "supergroup"]:
        room_id = f"group_{message.chat.id}"
    else:
        room_id = user_room.get(user_id)

    if not room_id or room_id not in rooms:
        return

    room = rooms[room_id]
    if not room["is_started"] or room["evaluated"]:
        return

    has_answered = any(ans["uid"] == user_id for ans in room["answers"])
    if not has_answered:
        user_text = message.text.lower().strip()
        room["answers"].append({"uid": user_id, "name": user_name, "text": user_text})
        await message.reply(f"📥 **{user_name}**, javobingiz qabul qilindi!")

    if len(room["answers"]) >= len(room["members"]):
        await evaluate_answers(room_id)

async def evaluate_answers(room_id: str):
    room = rooms.get(room_id)
    if not room or room["evaluated"]:
        return

    room["evaluated"] = True
    q_idx = room["q_idx"]
    q_data = room["questions"][q_idx]
    correct_answers = q_data["a"]

    text = f"⏰ **{q_idx + 1}-savol bosqichi yakunlandi!**\n\n"
    text += f"✅ **To'g'ri javob:** {correct_answers[0].title()}\n\n"

    answers = room.get("answers", [])

    if not answers:
        text += "❌ Hech kim javob yubormadi.\n"
    else:
        text += "📊 **O'yinchilarning javoblari va ballar:**\n"
        correct_counter = 0

        for ans_data in answers:
            uid = ans_data["uid"]
            ans_user = ans_data["name"]
            ans_text = ans_data["text"]

            is_correct = any(c_ans in ans_text for c_ans in correct_answers)
            if is_correct:
                correct_counter += 1
                gained_points = 2 if correct_counter == 1 else 1

                pos_icon = "🥇 1-bo'lib" if correct_counter == 1 else f"🥈 {correct_counter}-bo'lib"
                text += f"🟢 **{ans_user}**: {ans_text} — **To'g'ri!** ({pos_icon} +{gained_points} Ball)\n"

                room["scores"][ans_user] = room["scores"].get(ans_user, 0) + gained_points
                add_score(uid, ans_user, gained_points)
            else:
                text += f"🔴 **{ans_user}**: {ans_text} — **Noto'g'ri**\n"

    q_id = q_data.get("id")
    if q_id is not None:
        mark_question_solved(list(room["members"].keys()), q_id)

    if room["is_group"]:
        await bot.send_message(room["chat_id"], text)
    else:
        for m_id in room["members"].keys():
            await bot.send_message(m_id, text)

    room["q_idx"] += 1
    await asyncio.sleep(4)
    await send_question(room_id)

async def finish_game(room_id: str):
    room = rooms.get(room_id)
    scores = room["scores"]

    text = "🏆 **Zakovat O'yini Yakunlandi!**\n\n**Yakuniy Natijalar:**\n"
    if not scores:
        text += "O'yinda hech kim ball to'play olmadi."
    else:
        for p, s in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            text += f"👤 **{p}**: {s} ball\n"

    if room["is_group"]:
        await bot.send_message(room["chat_id"], text)
    else:
        for m_id in room["members"].keys():
            await bot.send_message(m_id, text)
            if m_id in user_room:
                del user_room[m_id]

    if room_id in rooms:
        del rooms[room_id]

@dp.message(F.text == "🏆 Top Bilimdonlar")
@dp.message(Command("top"))
async def show_top_players(message: types.Message):
    top_players = get_top_players(10)
    if not top_players:
        await message.answer("🏆 **Reyting bo'sh.** Hali hech kim ball to'plagani yo'q!")
        return

    text = "🏆 **Eng kuchli 10 ta Bilimdon ro'yxati:**\n\n"
    for idx, (name, score) in enumerate(top_players, 1):
        icon = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        text += f"{icon} **{name}** — {score} ball\n"
    await message.answer(text)

# --- WEBSERVER (Render PORT) ---
async def handle_ping(request):
    return web.Response(text="Zakovat Bot muvaffaqiyatli ishlayapti!")

async def main():
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot va Web Server muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
