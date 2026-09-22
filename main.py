import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# =====================================================
# BOT TOKEN
# =====================================================

TOKEN = "8851685095:AAEZGYQg0VBJF62HGs70wDzCynmxoAyvWqc"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# =====================================================
# SAVOLLAR
# =====================================================

questions = {
    "5": [
        {
            "question": "O'zbekiston poytaxti qaysi shahar?",
            "answers": ["Toshkent", "Samarqand", "Buxoro", "Xiva"],
            "correct": "Toshkent"
        },
        {
            "question": "2 + 3 nechaga teng?",
            "answers": ["4", "5", "6", "7"],
            "correct": "5"
        },
    ],

    "6": [
        {
            "question": "Yerning tabiiy yo'ldoshi nima?",
            "answers": ["Oy", "Quyosh", "Mars", "Venera"],
            "correct": "Oy"
        },
        {
            "question": "7 × 8 nechaga teng?",
            "answers": ["54", "56", "64", "48"],
            "correct": "56"
        },
    ],

    "7": [
        {
            "question": "Suvning kimyoviy formulasi qaysi?",
            "answers": ["H2O", "CO2", "O2", "NaCl"],
            "correct": "H2O"
        },
        {
            "question": "O'zbekiston qachon mustaqillikka erishgan?",
            "answers": ["1990", "1991", "1992", "1989"],
            "correct": "1991"
        },
    ],

    "8": [
        {
            "question": "Eng katta sayyora qaysi?",
            "answers": ["Yupiter", "Yer", "Mars", "Venera"],
            "correct": "Yupiter"
        },
        {
            "question": "9² nechaga teng?",
            "answers": ["18", "72", "81", "99"],
            "correct": "81"
        },
    ],

    "9": [
        {
            "question": "Dunyodagi eng katta okean qaysi?",
            "answers": ["Tinch", "Atlantika", "Hind", "Shimoliy Muz"],
            "correct": "Tinch"
        },
        {
            "question": "12 × 12 nechaga teng?",
            "answers": ["124", "144", "132", "154"],
            "correct": "144"
        },
    ],

    "10": [
        {
            "question": "Alisher Navoiy qaysi asarni yozgan?",
            "answers": [
                "Xamsa",
                "Boburnoma",
                "O'tkan kunlar",
                "Mehrobdan chayon"
            ],
            "correct": "Xamsa"
        },
        {
            "question": "Fotosintez asosan qayerda amalga oshadi?",
            "answers": ["Bargda", "Ildizda", "Poyada", "Gulda"],
            "correct": "Bargda"
        },
    ],

    "11": [
        {
            "question": "Python dasturlash tilining asoschisi kim?",
            "answers": [
                "Guido van Rossum",
                "Bill Gates",
                "Mark Zuckerberg",
                "Elon Musk"
            ],
            "correct": "Guido van Rossum"
        },
        {
            "question": "1 byte nechta bitdan iborat?",
            "answers": ["8", "4", "16", "32"],
            "correct": "8"
        },
    ],
}


# =====================================================
# USER HOLATLARI
# =====================================================

user_data = {}


# =====================================================
# SINFLAR MENYUSI
# =====================================================

def class_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="5-sinf",
                    callback_data="class_5"
                ),
                InlineKeyboardButton(
                    text="6-sinf",
                    callback_data="class_6"
                )
            ],
            [
                InlineKeyboardButton(
                    text="7-sinf",
                    callback_data="class_7"
                ),
                InlineKeyboardButton(
                    text="8-sinf",
                    callback_data="class_8"
                )
            ],
            [
                InlineKeyboardButton(
                    text="9-sinf",
                    callback_data="class_9"
                ),
                InlineKeyboardButton(
                    text="10-sinf",
                    callback_data="class_10"
                )
            ],
            [
                InlineKeyboardButton(
                    text="11-sinf",
                    callback_data="class_11"
                ),
                InlineKeyboardButton(
                    text="🎲 Barchasi (Aralash)",
                    callback_data="class_all"
                )
            ]
        ]
    )


# =====================================================
# START
# =====================================================

@dp.message(CommandStart())
async def start_handler(message: Message):

    user_id = message.from_user.id

    # Eski o'yinni tozalash
    user_data.pop(user_id, None)

    await message.answer(
        "👋 Xush kelibsiz!\n\n"
        "🎮 O'yinni boshlash uchun kerakli sinfni tanlang:",
        reply_markup=class_keyboard()
    )


# =====================================================
# SINIF TANLASH
# =====================================================

@dp.callback_query(F.data.startswith("class_"))
async def class_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    class_name = callback.data.replace("class_", "")

    # ARALASH
    if class_name == "all":

        all_questions = []

        for class_questions in questions.values():
            all_questions.extend(class_questions)

        selected_questions = all_questions.copy()

        class_text = "🎲 Barchasi (Aralash)"

    # MUAYYAN SINIF
    else:

        selected_questions = questions.get(
            class_name,
            []
        ).copy()

        class_text = f"{class_name}-sinf"

    if not selected_questions:

        await callback.answer(
            "❌ Bu sinf uchun savollar mavjud emas.",
            show_alert=True
        )

        return

    # Savollarni aralashtirish
    random.shuffle(selected_questions)

    # User ma'lumotlarini saqlash
    user_data[user_id] = {
        "class": class_name,
        "questions": selected_questions,
        "current": 0,
        "score": 0
    }

    # MUHIM:
    # Eski sinf tugmalarini olib tashlaymiz
    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.answer()

    await send_question(
        callback.message,
        user_id,
        class_text
    )


# =====================================================
# SAVOL YUBORISH
# =====================================================

async def send_question(
    message: Message,
    user_id: int,
    class_text: str
):

    data = user_data.get(user_id)

    if not data:
        return

    current = data["current"]
    question_list = data["questions"]

    # =================================================
    # O'YIN TUGADI
    # =================================================

    if current >= len(question_list):

        score = data["score"]
        total = len(question_list)

        await message.answer(
            "🏆 <b>O'YIN TUGADI!</b>\n\n"
            f"📚 Sinf: {class_text}\n\n"
            f"✅ To'g'ri: {score}\n"
            f"❌ Noto'g'ri: {total - score}\n"
            f"📊 Natija: {score}/{total}",
            parse_mode="HTML",
            reply_markup=restart_keyboard()
        )

        return

    # =================================================
    # SAVOL
    # =================================================

    question = question_list[current]

    answers = question["answers"].copy()

    random.shuffle(answers)

    keyboard = []

    for answer in answers:

        keyboard.append([
            InlineKeyboardButton(
                text=answer,
                callback_data=f"answer:{current}:{answer}"
            )
        ])

    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

    await message.answer(
        f"🎓 <b>{class_text}</b>\n\n"
        f"❓ <b>Savol {current + 1}/{len(question_list)}</b>\n\n"
        f"{question['question']}",
        parse_mode="HTML",
        reply_markup=markup
    )


# =====================================================
# JAVOBNI TEKSHIRISH
# =====================================================

@dp.callback_query(F.data.startswith("answer:"))
async def answer_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    data = user_data.get(user_id)

    if not data:

        await callback.answer(
            "❌ O'yin topilmadi. /start ni bosing.",
            show_alert=True
        )

        return

    parts = callback.data.split(":", 2)

    question_index = int(parts[1])
    selected_answer = parts[2]

    # Eski savolga bosilsa
    if data["current"] != question_index:

        await callback.answer(
            "⚠️ Bu savolga allaqachon javob berilgan.",
            show_alert=True
        )

        return

    question = data["questions"][question_index]

    correct_answer = question["correct"]

    # =================================================
    # TO'G'RI / NOTO'G'RI
    # =================================================

    if selected_answer == correct_answer:

        data["score"] += 1

        result = (
            "✅ <b>TO'G'RI!</b>\n\n"
            f"🎯 Javob: <b>{correct_answer}</b>"
        )

    else:

        result = (
            "❌ <b>NOTO'G'RI!</b>\n\n"
            f"✅ To'g'ri javob: "
            f"<b>{correct_answer}</b>"
        )

    # Javob tugmalarini olib tashlash
    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.answer()

    await callback.message.answer(
        result,
        parse_mode="HTML"
    )

    # Keyingi savol
    data["current"] += 1

    await asyncio.sleep(0.5)

    # Sinf nomi
    if data["class"] == "all":
        class_text = "🎲 Barchasi (Aralash)"
    else:
        class_text = f"{data['class']}-sinf"

    await send_question(
        callback.message,
        user_id,
        class_text
    )


# =====================================================
# QAYTA O'YNASH TUGMASI
# =====================================================

def restart_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Qayta o'ynash",
                    callback_data="restart"
                )
            ]
        ]
    )


# =====================================================
# QAYTA O'YNASH
# =====================================================

@dp.callback_query(F.data == "restart")
async def restart_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    user_data.pop(user_id, None)

    try:
        await callback.message.edit_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    await callback.answer()

    await callback.message.answer(
        "🎮 <b>Yangi o'yin</b>\n\n"
        "Kerakli sinfni tanlang:",
        parse_mode="HTML",
        reply_markup=class_keyboard()
    )


# =====================================================
# BOTNI ISHGA TUSHIRISH
# =====================================================

async def main():

    print("=================================")
    print("🤖 QUIZ BOT ISHGA TUSHDI")
    print("=================================")

    await dp.start_polling(bot)


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    asyncio.run(main())
