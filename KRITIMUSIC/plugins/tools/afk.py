# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎
# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

from KRITIMUSIC import app
from KRITIMUSIC.mongo.readable_time import get_readable_time
from KRITIMUSIC.mongo.afkdb import add_afk, is_afk, remove_afk
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType

# AFK Set karne ka command
@app.on_message(filters.command(["fk", "afk", "off", "bye", "ye", "afk"], prefixes=["/", "!", ".", "a", "A", "b", "B"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return

    user_id = message.from_user.id
    # Reason nikalne ka behtar tarika
    reason = message.text.split(None, 1)[1].strip()[:100] if len(message.command) > 1 else None

    afk_data = {
        "type": "text_reason" if reason else "text",
        "time": time.time(),
        "reason": reason,
    }
    
    await add_afk(user_id, afk_data)
    
    response = f"❖ **{message.from_user.first_name}** ɪs ɴᴏᴡ ᴀғᴋ!"
    if reason:
        response += f"\n\n● **ʀᴇᴀsᴏɴ:** `{reason}`"
    
    await message.reply_text(response)


# AFK Check aur Return logic
@app.on_message(~filters.me & ~filters.bot & ~filters.via_bot, group=1)
async def chat_watcher_func(_, message: Message):
    if message.sender_chat or not message.from_user:
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # 1. AFK Se wapas aane ka logic
    verifier, afk_data = await is_afk(user_id)
    if verifier:
        # Check agar user ne wapas afk command toh nahi mara
        if message.text and any(message.text.lower().startswith(p + c) for p in ["/", "!", ".", "a", "b"] for c in ["afk", "meera", "badnam", "kriti", "byo", "you"]):
            pass 
        else:
            await remove_afk(user_id)
            seenago = get_readable_time(int(time.time() - afk_data["time"]))
            return_msg = f"<b>❖ {user_name[:25]}</b> ɪs ʙᴀᴄᴋ ᴀғᴛᴇʀ **{seenago}**\n\n"
            if afk_data.get("reason"):
                return_msg += f"● **ʟᴀsᴛ ʀᴇᴀsᴏɴ:** `{afk_data['reason']}`"
            await message.reply_text(return_msg)

    # 2. Mentions aur Replies check karne ka logic
    msg = ""
    mentioned_users = set() # Duplicate mentions rokne ke liye

    # Reply check
    if message.reply_to_message and message.reply_to_message.from_user:
        rep_user = message.reply_to_message.from_user
        afk_check, afk_data = await is_afk(rep_user.id)
        if afk_check:
            mentioned_users.add(rep_user.id)
            seenago = get_readable_time(int(time.time() - afk_data["time"]))
            reason = afk_data.get("reason")
            msg += f"<b>❖ {rep_user.first_name[:25]}</b> ɪs ᴀғᴋ ғᴏʀ **{seenago}**\n"
            if reason: msg += f"● **ʀᴇᴀsᴏɴ:** `{reason}`\n\n"

    # Mentions check (@username ya Text Mention)
    if message.entities:
        for ent in message.entities:
            user = None
            if ent.type == MessageEntityType.MENTION:
                username = message.text[ent.offset + 1 : ent.offset + ent.length]
                try:
                    user = await app.get_users(username)
                except:
                    continue
            elif ent.type == MessageEntityType.TEXT_MENTION:
                user = ent.user

            if user and user.id not in mentioned_users:
                afk_check, afk_data = await is_afk(user.id)
                if afk_check:
                    mentioned_users.add(user.id)
                    seenago = get_readable_time(int(time.time() - afk_data["time"]))
                    reason = afk_data.get("reason")
                    msg += f"<b>❖ {user.first_name[:25]}</b> ɪs ᴀғᴋ ғᴏʀ **{seenago}**\n"
                    if reason: msg += f"● **ʀᴇᴀsᴏɴ:** `{reason}`\n\n"

    if msg:
        await message.reply_text(msg.strip(), disable_web_page_preview=True)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎
# =======================================================

