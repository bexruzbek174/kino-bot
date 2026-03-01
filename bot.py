import os
import telebot

TOKEN = os.getenv("8480649282:AAGWZpxMthZ6opERfZhPQGmQqEusg_ECRiE")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Kino bot ishlayapti 🎬")

bot.infinity_polling()
