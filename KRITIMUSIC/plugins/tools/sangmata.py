# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.raw.functions.messages import DeleteHistory
from KRITIMUSIC import userbot as us, app
from KRITIMUSIC.core.userbot import assistants

@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply("**➤ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.**")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split()[1]

    loading = await message.reply("**❖ ᴘʀᴏᴄᴇssɪɴɢ...**")

    try:
        user = await client.get_users(user_id)
    except Exception:
        return await loading.edit("**✘ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ.**")

    sangmata_bots = ["sangmata_bot", "sangmata_beta_bot"]
    target_bot = random.choice(sangmata_bots)

    if 1 in assistants:
        ubot = us.one
    else:
        return await loading.edit("**✘ ɴᴏ ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀʙᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ.**")

    try:
        sent = await ubot.send_message(target_bot, str(user.id))
        await sent.delete()
    except Exception as e:
        return await loading.edit(f"**✘ ᴇʀʀᴏʀ :-** {e}")

    await asyncio.sleep(2)

    found = False
    async for msg in ubot.search_messages(target_bot):
        if not msg.text:
            continue
        await message.reply(
            f"🧾 <b>ʜɪsᴛᴏʀʏ :-</b>\n\n{msg.text}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
        )
        found = True
        break

    if not found:
        await message.reply("**✘ ɴᴏ ʀᴇsᴘᴏɴsᴇ ʀᴇᴄᴇɪᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ sᴀɴɢᴍᴀᴛᴀ ʙᴏᴛ.**")

    try:
        peer = await ubot.resolve_peer(target_bot)
        await ubot.send(DeleteHistory(peer=peer, max_id=0, revoke=True))
    except Exception:
        pass

    await loading.delete()

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================
