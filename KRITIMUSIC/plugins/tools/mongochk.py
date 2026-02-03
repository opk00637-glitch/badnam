# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import re, json, io, os
from KRITIMUSIC import app as Miku

mongo_url_pattern = re.compile(r"mongodb(?:\+srv)?:\/\/[^\s]+")


@Miku.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):

    ADD_ME_BUTTON = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙", url=f"https://t.me/{Miku.username}?startgroup=true")]]
    )

    if len(message.command) < 2:
        await message.reply(
            f"**⋟ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴜʀʟ ᴀꜰᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ.**\n\n**ᴇxᴀᴍᴘʟᴇ :-** /mongochk mongo_url`",
            reply_markup=ADD_ME_BUTTON
        )
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            mongo_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            mongo_client.server_info()  # ⋟ ᴡɪʟʟ ᴄᴀᴜꜱᴇ ᴀɴ ᴇxᴄᴇᴘᴛɪᴏɴ ɪꜰ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ꜰᴀɪʟꜱ
            await message.reply(
                f"**⋟ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ɪꜱ ᴠᴀʟɪᴅ ᴀɴᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ ✅**\n\n**⋟ ᴄʜᴇᴄᴋ ʙʏ :– {Miku.mention}**",
                reply_markup=ADD_ME_BUTTON
            )
        except Exception as e:
            await message.reply(
                f"**⋟ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴍᴏɴɢᴏᴅʙ :-** {e}\n\n**⋟ ᴄʜᴇᴄᴋ ʙʏ :– {Miku.mention}",
                reply_markup=ADD_ME_BUTTON
            )
    else:
        await message.reply(
            f"**⋟ ɪɴᴠᴀʟɪᴅ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ꜰᴏʀᴍᴀᴛ 💔**\n\n**⋟ ᴄʜᴇᴄᴋ ʙʏ :– {Miku.mention}**",
            reply_markup=ADD_ME_BUTTON
        )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================
