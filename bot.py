import telebot

TOKEN = "YOUR_BOT_TOKEN"  # Замени на свой токен
CHANNEL_LINK = "https://t.me/YOUR_CHANNEL"  # Замени на свою ссылку
VIDEO_PATH = "start_video.mp4"  # Укажи название видеофайла

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    text = "🔥 Welcome to the NikeDrop Giveaway! 🔥\n\nWe're giving away 133 exclusive Nike sneakers! 👟\n\nClick the link to join: " + CHANNEL_LINK
    with open(VIDEO_PATH, 'rb') as video:
        bot.send_video(chat_id, video, caption=text)

bot.polling(none_stop=True)
