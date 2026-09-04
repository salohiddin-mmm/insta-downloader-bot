import asyncio
import logging
import os
from telethon import TelegramClient, events
from telethon.tl.custom import Button
import yt_dlp

# Telegram API ma'lumotlaringiz
API_ID = 36507875  # my.telegram.org'dan olingan api_id
API_HASH = "97d61a0abed5887772bae1bf67edb536"  # my.telegram.org'dan olingan api_hash
BOT_TOKEN = "8846168320:AAFVrjTa_LT2GVKiPB89yYz8Qh_FDgY8OxE"  # @BotFather'dan olingan token

bot = TelegramClient('insta_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Faqat Instagram uchun yuklash funksiyasi
def download_instagram_video(url: str) -> str:
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'socket_timeout': 30,
        'retries': 5,
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# Menyu tugmalari
menu_buttons = [
    [Button.text("ℹ️ Bot haqida", resize=True), Button.text("📞 Bog'lanish", resize=True)]
]

# /start buyrug'i
@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond(
        f"Salom, {event.sender.first_name}!\n\nMenga **Instagram** havola yuboring, yuklab beraman!",
        buttons=menu_buttons
    )

# Tugmalar
@bot.on(events.NewMessage(pattern="ℹ️ Bot haqida"))
async def about_handler(event):
    await event.respond("Ushbu bot faqat Instagram platformasidan videolarni yuklash uchun mo'ljallangan.")

@bot.on(events.NewMessage(pattern="📞 Bog'lanish"))
async def contact_handler(event):
    await event.respond("Admin bilan bog'lanish: @mamadal1evme")

# Faqat Instagram havolalarini ushlab olish
@bot.on(events.NewMessage)
async def instagram_handler(event):
    text = event.raw_text
    if text.startswith('/') or text in ["ℹ️ Bot haqida", "📞 Bog'lanish"]:
        return

    # Faqat instagram.com bo'lsa ishlaydi
    if "instagram.com" in text:
        wait_msg = await event.respond("⏳ Video yuklanmoqda, kuting...")
        try:
            file_path = await asyncio.wait_for(
                asyncio.to_thread(download_instagram_video, text),
                timeout=180.0
            )
            
            await wait_msg.edit("⬆️ Video yuborilmoqda...")
            
            await bot.send_file(
                event.chat_id,
                file=file_path,
                caption="Video yuklab olindi! 🚀"
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
            await wait_msg.delete()

        except asyncio.TimeoutError:
            await wait_msg.edit("❌ Yuklash vaqti oshib ketdi. Qaytadan urinib ko'ring.")
        except Exception as e:
            await wait_msg.edit("❌ Videoni yuklab bo'lmadi. Havola to'g'riligini va sahifa ochiq (public) ekanligini tekshiring.")

print("Instagram downloader bot ishga tushdi!")
bot.run_until_disconnected()