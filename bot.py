from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import aiohttp

TOKEN = "8166268833:AAGwIkGiD0RtaVCEWWTUMbEvzqW8pM4RgTA"  # Твой токен бота
CHANNEL_USERNAME = "@RTFKTxNIKEnft"  # Юзернейм канала без t.me/

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

async def check_subscription(user_id):
    """Функция проверяет, подписан ли пользователь на канал"""
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            status = data.get("result", {}).get("status", "")
            return status in ["member", "administrator", "creator"]

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        button = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚀 Войти в приложение", web_app=types.WebAppInfo(url="https://vercel.com/roriks-projects-9f1743db/nikegiveaway"))
        )
        await message.answer("✅ Добро пожаловать! Нажмите на кнопку, чтобы войти в мини-приложение.", reply_markup=button)
    else:
        button = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔥 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")
        )
        await message.answer("❌ Чтобы продолжить, подпишитесь на канал!", reply_markup=button)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
