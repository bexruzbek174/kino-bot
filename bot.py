import os
import telebot
import sqlite3
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = -1003747471816

# DATABASE
conn = sqlite3.connect("movies.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    code TEXT,
    message_id INTEGER
)
""")
conn.commit()

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti 🚀"

def run_bot():
    bot.infinity_polling()

# Kanalga yangi kino tushsa
@bot.channel_post_handler(content_types=['video', 'document'])
def save_movie(message):
    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0] + 1
    code = str(count)

    cursor.execute("INSERT INTO movies VALUES (?, ?)", (code, message.message_id))
    conn.commit()

    bot.send_message(
        CHANNEL_ID,
        f"🎬 Kino kodi: {code}",
        reply_to_message_id=message.message_id
    )

# User kod yuborsa
@bot.message_handler(func=lambda message: True)
def send_movie(message):
    code = message.text

    cursor.execute("SELECT message_id FROM movies WHERE code=?", (code,))
    result = cursor.fetchone()

    if result:
        bot.copy_message(message.chat.id, CHANNEL_ID, result[0])
    else:
        bot.send_message(message.chat.id, "❌ Bunday kino topilmadi")

# Botni alohida threadda ishga tushiramiz
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
