import telebot
from telebot import types
import requests

# Твой токен бота
TOKEN = "8166268833:AAGwIkGiD0RtaVCEWWTUMbEvzqW8pM4RgTA"
# Твой канал
CHANNEL_USERNAME = "RTFKTxNIKEnft"

bot = telebot.TeleBot(TOKEN)

# Функция проверки подписки
def check_subscription(user_id):
    try:
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id=@{CHANNEL_USERNAME}&user_id={user_id}")
        result = response.json()
        status = result.get("result", {}).get("status", "")

        return status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    subscribed = check_subscription(user_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if not subscribed:
        # Если НЕ подписан – показываем кнопку "Подписаться"
        subscribe_button = types.KeyboardButton("🔥 Подписаться на канал")
        markup.add(subscribe_button)
        bot.send_message(
            message.chat.id,
            "👋 Добро пожаловать! Чтобы продолжить, подпишись на наш канал:\n\n"
            f"👉 [Подписаться](https://t.me/{CHANNEL_USERNAME})",
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        # Если подписан – скрываем кнопку и отправляем следующее сообщение
        bot.send_message(
            message.chat.id,
            "✅ Отлично! Ты подписался! Теперь можешь продолжить.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        # Здесь можно добавить другую кнопку (например, "Перейти в приложение")
        start_button = types.InlineKeyboardMarkup()
        start_button.add(types.InlineKeyboardButton("🚀 Войти в приложение", web_app=types.WebAppInfo(url="https://vercel.com/roriks-projects-9f1743db/nikegiveaway")))
        bot.send_message(message.chat.id, "Нажми на кнопку ниже, чтобы войти в приложение:", reply_markup=start_button)

# Обработка кнопки "Подписаться на канал"
@bot.message_handler(func=lambda message: message.text == "🔥 Подписаться на канал")
def subscribe_check(message):
    user_id = message.from_user.id
    subscribed = check_subscription(user_id)

    if subscribed:
        bot.send_message(
            message.chat.id,
            "✅ Ты подписался! Теперь можешь продолжить.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        # После подписки отправляем кнопку для входа
        start_button = types.InlineKeyboardMarkup()
        start_button.add(types.InlineKeyboardButton("🚀 Войти в приложение", web_app=types.WebAppInfo(url="https://vercel.com/roriks-projects-9f1743db/nikegiveaway")))
        bot.send_message(message.chat.id, "Нажми на кнопку ниже, чтобы войти в приложение:", reply_markup=start_button)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Ты ещё не подписался! Пожалуйста, подпишись и нажми кнопку снова.",
            parse_mode="Markdown"
        )

# Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True)

