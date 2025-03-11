import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "8166268833:AAGwIkGiD0RtaVCEWWTUMbEvzqW8pM4RgTA"  # Твой токен бота
CHANNEL_USERNAME = "@RTFKTxNIKEnft"  # Твой канал

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Клавиатура с кнопкой подписки
subscribe_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🔥 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
)

# Клавиатура с кнопкой входа в приложение
app_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🚀 Войти в приложение", web_app=types.WebAppInfo(url="https://vercel.com/roriks-projects-9f1743db/nikegiveaway"))
)


# Функция проверки подписки
async def check_subscription(user_id):
    try:
        chat_member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer(
            "✅ Вы подписаны! Добро пожаловать!\nНажмите кнопку ниже, чтобы войти в приложение:",
            reply_markup=app_kb
        )
    else:
        await message.answer(
            "❌ Вы не подписаны!\nПодпишитесь на канал, чтобы продолжить:",
            reply_markup=subscribe_kb
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

