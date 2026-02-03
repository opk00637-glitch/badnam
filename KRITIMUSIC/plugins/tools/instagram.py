# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
import os
import math
from KRITIMUSIC import app

os.makedirs("downloads", exist_ok=True)

def get_readable_file_size(size_in_bytes):
    if size_in_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    return f"{s} {size_name[i]}"

def download_instagram_reel(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path, info, None
    except Exception as e:
        return None, None, str(e)

@app.on_message(filters.command(["reel", "ig"]) & (filters.private | filters.group))
async def reel_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "**ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴜʀʟ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ 🙌**",
            quote=True
        )

    url = message.text.split(maxsplit=1)[1]

    if "instagram.com/reel" not in url:
        return await message.reply("**ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴜʀʟ ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ 😅😅**", quote=True)

    status = await message.reply("**⏳ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʀᴇᴇʟ, ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...**", quote=True)

    file_path, info, error = download_instagram_reel(url)
    if file_path:
        try:
            title = info.get("title", "Instagram Reel")
            duration = round(info.get("duration", 0))
            filesize = os.path.getsize(file_path)
            size = get_readable_file_size(filesize)
            quality = info.get("format", "Best")

            bot_username = (await client.get_me()).username

            caption = (
                f"**◍ ᴜᴘʟᴏᴀᴅᴇʀ :-** `{title}`\n"
                f"**◍ ǫᴜᴀʟɪᴛʏ :-** `{quality}`\n"
                f"**◍ ᴅᴜʀᴀᴛɪᴏɴ :-** `{duration} sec`\n"
                f"**◍ ꜱɪᴢᴇ :-** `{size}`"
            )

            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙",
                        url=f"https://t.me/{bot_username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
                    )
                ]
            ])

            await client.send_video(
                chat_id=message.chat.id,
                video=file_path,
                caption=caption,
                reply_markup=buttons
            )

            os.remove(file_path)
            await status.delete()

        except Exception as e:
            await status.edit(f"**⚠️ ᴇʀʀᴏʀ ᴡʜɪʟᴇ ꜱᴇɴᴅɪɴɢ ᴠɪᴅᴇᴏ :** `{e}`")
    else:
        await status.edit(f"**⚠️ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ :** `{error}`")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================
