import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

# --- إعداد خادم وهمي لإبقاء Render سعيداً ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- كود البوت الأساسي ---
TOKEN = '6692891979:AAHptNMWADSbaEQeo1va7ojB-wdrb89IwkM'
bot = telebot.TeleBot(TOKEN)

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/video.mp4',
        'nocheckcertificate': True,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً! البوت يعمل الآن بنظام 24/7 على Render. أرسل الرابط.")

@bot.message_handler(func=lambda message: "http" in message.text)
def handle_download(message):
    temp_msg = bot.reply_to(message, "جاري التحميل... 🚀")
    video_path = '/tmp/video.mp4'
    try:
        download_video(message.text)
        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بنجاح ✅")
        os.remove(video_path)
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")
        if os.path.exists(video_path): os.remove(video_path)
    finally:
        bot.delete_message(message.chat.id, temp_msg.message_id)

if __name__ == "__main__":
    keep_alive()  # تشغيل الخادم الوهمي في الخلفية
    bot.infinity_polling()

bot.infinity_polling()
