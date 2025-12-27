import telebot
import yt_dlp
import os

TOKEN = 'ضع_هنا_التوكن_الخاص_بك'
bot = telebot.TeleBot(TOKEN)

def download_video(url):
    # خيارات متوافقة مع سيرفرات Render
    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/video.mp4', # استخدام مجلد /tmp المسموح بالكتابة فيه
        'nocheckcertificate': True,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً! أنا الآن أعمل من منصة Render القوية. أرسل لي أي رابط فيديو.")

@bot.message_handler(func=lambda message: "http" in message.text)
def handle_download(message):
    temp_msg = bot.reply_to(message, "جاري التحميل من Render... 🚀")
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

bot.infinity_polling()
