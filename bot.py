import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8166268833:AAGwIkGiD0RtaVCEWWTUMbEvzqW8pM4RgTA"
CHANNEL_USERNAME = "RTFKTxNIKEnft"  # Имя канала без @

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # Создаем кнопку для подписки
    markup = InlineKeyboardMarkup()
    btn_subscribe = InlineKeyboardButton(
        "🔥 Подписаться на канал",
        url=f"https://t.me/{CHANNEL_USERNAME}"
    )
    btn_check = InlineKeyboardButton("✅ Проверить подписку", callback_data="check_sub")
    markup.add(btn_subscribe)
    markup.add(btn_check)

    bot.send_message(
        chat_id,
        "🎁 Чтобы участвовать в розыгрыше, подпишись на наш канал!\n\n👇 Подпишись и нажми кнопку 'Проверить подписку'",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    chat_member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)

    if chat_member.status in ["member", "administrator", "creator"]:
        bot.send_message(call.message.chat.id, "✅ Вы подписаны! Теперь вы можете участвовать в розыгрыше.")
    else:
        bot.send_message(call.message.chat.id, "❌ Вы не подписаны! Подпишитесь и попробуйте снова.")

bot.polling()
