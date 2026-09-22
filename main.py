import os
import asyncio
import random
import logging
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

# Импорт вопросов и функции проверки из вашего questions.py
from questions import LOGICAL_QUESTIONS, check_answer

# Настройка логирования для отслеживания ошибок в консоли Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (берётся из переменных Render или используется текущий рабочий)
TOKEN = os.getenv("BOT_TOKEN", "8744991351:AAGVE82fuE3k910i-Xk-GG8_qGDgYzeWQOY")

# ----------------- FLASK WEB SERVER FOR RENDER -----------------
app = Flask('')

@app.route('/')
def home():
    return "Bot status: ONLINE"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ----------------- КЛАВИАТУРЫ И МЕНЮ -----------------

def get_class_keyboard():
    """Выбор класса (от 5 до 11) и вариант 'Aralash'"""
    keyboard = [
        [InlineKeyboardButton("5-sinf", callback_data="class_5"), InlineKeyboardButton("6-sinf", callback_data="class_6")],
        [InlineKeyboardButton("7-sinf", callback_data="class_7"), InlineKeyboardButton("8-sinf", callback_data="class_8")],
        [InlineKeyboardButton("9-sinf", callback_data="class_9"), InlineKeyboardButton("10-sinf", callback_data="class_10")],
        [InlineKeyboardButton("11-sinf", callback_data="class_11"), InlineKeyboardButton("🎲 Barchasi (Aralash)", callback_data="class_all")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_count_keyboard():
    """Выбор количества вопросов"""
    keyboard = [
        [InlineKeyboardButton("3 ta savol", callback_data="count_3"), InlineKeyboardButton("5 ta savol", callback_data="count_5")],
        [InlineKeyboardButton("10 ta savol", callback_data="count_10"), InlineKeyboardButton("15 ta savol", callback_data="count_15")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ----------------- ОБРАБОТКА /START -----------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Очищаем старые таймеры, если они были
    if "timer_task" in context.user_data and context.user_data["timer_task"]:
        context.user_data["timer_task"].cancel()
        
    context.user_data.clear()
    
    await update.message.reply_text(
        "👋 **Xush kelibsiz!** O'yinni boshlash uchun kerakli **sinfni** tanlang:",
        reply_markup=get_class_keyboard(),
        parse_mode="Markdown"
    )

# ----------------- ТАЙМЕР И ПОДСКАЗКА -----------------

async def timer_task(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, total_seconds: int):
    try:
        hint_sent = False
        while total_seconds > 0:
            await asyncio.sleep(1)
            total_seconds -= 1
            
            if not context.user_data.get("is_answering", False):
                return

            # Отправка подсказки (hint) на 80-й секунде (когда остается <= 30 сек)
            if total_seconds <= 30 and not hint_sent:
                hint_sent = True
                q_data = context.user_data.get("current_q")
                if q_data and q_data.get("hint"):
                    try:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=f"💡 <b>Maslahat:</b> {q_data['hint']}",
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        logger.error(f"Ошибка при отправке подсказки: {e}")
            
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
                if q_data.get("image"):
                    await context.bot.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption=text,
                        parse_mode="HTML"
                    )
                else:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=text,
                        parse_mode="HTML"
                    )
            except Exception:
                pass

        if context.user_data.get("is_answering", False):
            context.user_data["is_answering"] = False
            await context.bot.send_message(
                chat_id=chat_id,
                text="⏰ <b>Vaqt tugadi!</b> Javob qabul qilinmadi.",
                parse_mode="HTML"
            )
            context.user_data["q_index"] = context.user_data.get("q_index", 0) + 1
            await ask_next_question(context, chat_id)
            
    except asyncio.CancelledError:
        pass

# ----------------- ОТПРАВКА СЛЕДУЮЩЕГО ВОПРОСА -----------------

async def ask_next_question(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    q_index = context.user_data.get("q_index", 0)
    selected_questions = context.user_data.get("questions", [])
    
    if q_index >= len(selected_questions):
        score = context.user_data.get("score", 0)
        total = len(selected_questions)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"🎉 <b>O'yin yakunlandi!</b>\n\n"
                f"📊 <b>Natijangiz:</b> siz {total} ta savoldan <b>{score}</b> tasiga to'g'ri javob berdingiz!\n\n"
                f"Qayta o'ynash uchun sinfni tanlang:"
            ),
            parse_mode="HTML",
            reply_markup=get_class_keyboard()
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
    
    try:
        if q_data.get("image"):
            msg = await context.bot.send_photo(
                chat_id=chat_id,
                photo=q_data["image"],
                caption=text,
                parse_mode="HTML"
            )
        else:
            msg = await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Ошибка отправки фото: {e}")
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML"
        )
    
    if "timer_task" in context.user_data and context.user_data["timer_task"]:
        context.user_data["timer_task"].cancel()
        
    task = asyncio.create_task(timer_task(context, chat_id, msg.message_id, 110))
    context.user_data["timer_task"] = task

# ----------------- ОБРАБОТКА НАЖАТИЙ НА КНОПКИ -----------------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data.startswith("class_"):
            selected_class = query.data.split("_")[1]
            context.user_data["selected_class"] = selected_class
            
            class_title = f"{selected_class}-sinf" if selected_class != "all" else "Barcha sinflar"
            await query.message.edit_text(
                f"✅ **{class_title}** tanlandi!\nEndi **savollar sonini** tanlang:",
                reply_markup=get_count_keyboard(),
                parse_mode="Markdown"
            )
            
        elif query.data.startswith("count_"):
            count = int(query.data.split("_")[1])
            selected_class = context.user_data.get("selected_class", "all")
            
            all_q = LOGICAL_QUESTIONS.copy()
            
            if selected_class != "all":
                filtered_q = [q for q in all_q if str(q.get("class", "")) == selected_class]
                if filtered_q:
                    all_q = filtered_q

            random.shuffle(all_q)
            
            context.user_data["questions"] = all_q[:count]
            context.user_data["q_index"] = 0
            context.user_data["score"] = 0
            context.user_data["total_q"] = min(count, len(all_q))
            
            await query.message.delete()
            await ask_next_question(context, query.message.chat_id)

    except Exception as e:
        logger.error(f"Ошибка в button_handler: {e}")

# ----------------- ПРОВЕРКА ОТВЕТА -----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("is_answering", False):
        return

    user_text = update.message.text
    current_q = context.user_data.get("current_q")
    
    if not current_q:
        return
        
    context.user_data["is_answering"] = False
    
    if "timer_task" in context.user_data and context.user_data["timer_task"]:
        context.user_data["timer_task"].cancel()

    is_correct = check_answer(user_text, current_q["a"])
    
    if is_correct:
        context.user_data["score"] = context.user_data.get("score", 0) + 1
        await update.message.reply_text("✅ <b>To'g'ri javob!</b>", parse_mode="HTML")
    else:
        correct_one = current_q["a"][0] if isinstance(current_q["a"], list) else current_q["a"]
        await update.message.reply_text(
            f"❌ <b>Noto'g'ri javob.</b>\nTo'g'ri javob: <i>{correct_one}</i>", 
            parse_mode="HTML"
        )
        
    context.user_data["q_index"] = context.user_data.get("q_index", 0) + 1
    await ask_next_question(context, update.message.chat_id)

# ----------------- ЗАПУСК БОТА -----------------

def main():
    # Запуск фонового веб-сервера
    keep_alive()
    
    # Сборка приложения Telegram
    app_bot = Application.builder().token(TOKEN).build()
    
    # Регистрация хэндлеров
    app_bot.add_handler(CommandHandler("start", start_command))
    app_bot.add_handler(CallbackQueryHandler(button_handler))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot uspeshno zapushen!")
    
    # drop_pending_updates=True удаляет подвисшие старые команды и сбрасывает вебхуки
    app_bot.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
