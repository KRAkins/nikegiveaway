from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import os

# Твой токен бота
TOKEN = "8166268833:AAGwIkGiD0RtaVCEWWTUMbEvzqW8pM4RgTA"
CHANNEL_ID = "@RTFKTxNIKEnft"  # Твой канал

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# 📌 Кнопка подписки на канал
def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton(text="🔥 Подписаться", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")
    keyboard.add(subscribe_button)
    return keyboard

# ✅ Функция проверки подписки
async def is_user_subscribed(user_id):
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False  # Если ошибка API

# 📌 Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id

    # Проверяем подписку
    if not await is_user_subscribed(user_id):
        await message.answer(
            "❌ Ты не подписан на канал! Подпишись, чтобы участвовать:",
            reply_markup=get_subscription_keyboard()
        )
        return  # Прерываем выполнение

    # Отправляем видео и текст
    video_path = "start_video.mp4"  # Указываем путь к видео в той же папке
    text = "🎉 Добро пожаловать в розыгрыш NikeDrop!\n\n🔹 Подпишись на наш канал\n🔹 Жми кнопку ниже, чтобы войти в приложение!"
    
    with open(video_path, "rb") as video:
        await message.answer_video(video, caption=text)

    # Кнопка входа в приложение
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🚀 Войти в приложение", web_app=types.WebAppInfo(url="https://vercel.com/roriks-projects-9f1743db/nikegiveaway")))

    await message.answer("👇 Жми кнопку, чтобы участвовать!", reply_markup=keyboard)

# Запуск бота
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
