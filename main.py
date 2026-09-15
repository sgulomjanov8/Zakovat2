import os
import asyncio
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# questions.py faylidan savollar va check_answer funksiyasini import qilamiz
from questions import LOGICAL_QUESTIONS, check_answer

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Web Server (Render 24/7 ishlashi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot faol ishlamoqda!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- HELPER FUNKSIYALAR ---

def get_count_keyboard():
    keyboard = [
        [InlineKeyboardButton("3 ta savol", callback_data="count_3"), InlineKeyboardButton("5 ta savol", callback_data="count_5")],
        [InlineKeyboardButton("10 ta savol", callback_data="count_10"), InlineKeyboardButton("15 ta savol", callback_data="count_15")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Xush kelibsiz! O'yinni boshlash uchun savollar sonini tanlang:",
        reply_markup=get_count_keyboard()
    )

# --- TAYMER VAZIFASI ---

async def timer_task(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, total_seconds: int):
    """Xabarni har soniyada tahrirlab vaqtni ko'rsatadi"""
    try:
        while total_seconds > 0:
            await asyncio.sleep(1)
            total_seconds -= 1
            
            # Agar foydalanuvchi javob berib bo'lgan bo'lsa taymerni to'xtatamiz
            if not context.user_data.get("is_answering", False):
                return
            
            mins, secs = divmod(total_seconds, 60)
            time_str = f"{mins}:{secs:02d}"
            
            q_data = context.user_data.get("current_q")
            q_index = context.user_data.get("q_index", 0)
            total_q = context.user_data.get("total_q", 0)
            
            text = (
                f"❓ <b>Savol {q_index + 1}/{total_q}:</b>\n"
                f"{q_data['q']}\n\n"
                f"⏱ <b>Qolgan vaqt:</b> {time_str}"
            )
            
            try:
                await context.bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=text,
                    parse_mode="HTML"
                )
            except Exception:
                pass # Agar matn o'zgarmagan bo'lsa telegram xatolik berishini o'tkazib yuboramiz

        # Vaqt tugasa
        if context.user_data.get("is_answering", False):
            context.user_data["is_answering"] = False
            await context.bot.send_message(
                chat_id=chat_id,
                text="⏰ <b>Vaqt tugadi!</b> Javob qabul qilinmadi.",
                parse_mode="HTML"
            )
            await ask_next_question(context, chat_id)
            
    except asyncio.CancelledError:
        pass

# --- SAVOLLARNI BERISH ---

async def ask_next_question(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    q_index = context.user_data.get("q_index", 0)
    selected_questions = context.user_data.get("questions", [])
    
    # O'yin tugaganini tekshirish
    if q_index >= len(selected_questions):
        score = context.user_data.get("score", 0)
        total = len(selected_questions)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"🎉 <b>O'yin yakunlandi!</b>\n\n"
                f"📊 <b>Natijangiz:</b> siz {total} ta savoldan <b>{score}</b> tasiga to'g'ri javob berdingiz!\n\n"
                f"Qayta o'ynash uchun sonni tanlang:"
            ),
            parse_mode="HTML",
            reply_markup=get_count_keyboard()
        )
        return

    q_data = selected_questions[q_index]
    context.user_data["current_q"] = q_data
    context.user_data["is_answering"] = True
    
    text = (
        f"❓ <b>Savol {q_index + 1}/{len(selected_questions)}:</b>\n"
        f"{q_data['q']}\n\n"
        f"⏱ <b>Qolgan vaqt:</b> 1:50"
    )
    
    # Rasm va savolni yuborish
    msg = await context.bot.send_photo(
        chat_id=chat_id,
        photo=q_data["image"],
        caption=text,
        parse_mode="HTML"
    )
    
    # Oldingi taymerni bekor qilish va yangisini ishga tushirish (110 soniya = 1 daqiqa 50 soniya)
    if "timer_task" in context.user_data and context.user_data["timer_task"]:
        context.user_data["timer_task"].cancel()
        
    task = asyncio.create_task(timer_task(context, chat_id, msg.message_id, 110))
    context.user_data["timer_task"] = task

# --- CALLBACK QO'NG'IROQLARI (TUGMALAR) ---

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("count_"):
        count = int(query.data.split("_")[1])
        
        import random
        # questions.py faylidagi savollardan tasodifiy tanlab olamiz
        all_q = LOGICAL_QUESTIONS.copy()
        random.shuffle(all_q)
        
        context.user_data["questions"] = all_q[:count]
        context.user_data["q_index"] = 0
        context.user_data["score"] = 0
        context.user_data["total_q"] = count
        
        await query.message.delete()
        await ask_next_question(context, query.message.chat_id)

# --- JAVOBLARNI TEKSHIRISH ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Agar foydalanuvchi hozir savolga javob berish bosqichida bo'lmasa
    if not context.user_data.get("is_answering", False):
        return

    user_text = update.message.text
    current_q = context.user_data.get("current_q")
    
    if not current_q:
        return
        
    # Taymerni to'xtatamiz
    context.user_data["is_answering"] = False
    if "timer_task" in context.user_data and context.user_data["timer_task"]:
        context.user_data["timer_task"].cancel()

    # questions.py faylidagi check_answer orqali tekshirish
    is_correct = check_answer(user_text, current_q["a"])
    
    if is_correct:
        context.user_data["score"] = context.user_data.get("score", 0) + 1
        await update.message.reply_text("✅ <b>To'g'ri javob!</b>", parse_mode="HTML")
    else:
        correct_one = current_q["a"][0]
        await update.message.reply_text(
            f"❌ <b>Noto'g'ri javob.</b>\nTo'g'ri javob: <i>{correct_one}</i>", 
            parse_mode="HTML"
        )
        
    context.user_data["q_index"] += 1
    await ask_next_question(context, update.message.chat_id)

# --- MAIN ---

def main():
    keep_alive()
    
    app_bot = Application.builder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start_command))
    app_bot.add_handler(CallbackQueryHandler(button_handler))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi!")
    app_bot.run_polling()

if __name__ == '__main__':
    main()
