#
# Copyright (C) 2021-2025
# Project : KRITIMUSIC
# License : GNU v3.0
#

import asyncio
import time

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message

from KRITIMUSIC import app
from KRITIMUSIC.core.call import Miku
from KRITIMUSIC.misc import db
from KRITIMUSIC.utils.database import (
    get_assistant,
    get_authuser_names,
    get_cmode,
)
from KRITIMUSIC.utils.decorators import (
    ActualAdminCB,
    AdminActual,
    language,
)
from KRITIMUSIC.utils.formatters import (
    alpha_to_int,
    get_readable_time,
)
from config import BANNED_USERS, adminlist, lyrical

# ======================================================
# ADMIN CACHE
# ======================================================

_reload_timer = {}


@app.on_message(
    filters.command(["admincache", "reload", "refresh"])
    & filters.group
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(_, message: Message, _l):
    try:
        chat_id = message.chat.id
        now = int(time.time())

        if _reload_timer.get(chat_id, 0) > now:
            left = get_readable_time(_reload_timer[chat_id] - now)
            return await message.reply_text(_l["reload_1"].format(left))

        adminlist[chat_id] = []

        async for member in app.get_chat_members(
            chat_id,
            filter=ChatMembersFilter.ADMINISTRATORS,
        ):
            if member.privileges and member.privileges.can_manage_video_chats:
                adminlist[chat_id].append(member.user.id)

        auth_users = await get_authuser_names(chat_id)
        for user in auth_users:
            adminlist[chat_id].append(await alpha_to_int(user))

        _reload_timer[chat_id] = now + 180
        await message.reply_text(_l["reload_2"])

    except Exception:
        await message.reply_text(_l["reload_3"])


# ======================================================
# REBOOT BOT
# ======================================================

@app.on_message(filters.command("reboot") & filters.group & ~BANNED_USERS)
@AdminActual
async def reboot_bot(_, message: Message, _l):
    msg = await message.reply_text(_l["reload_4"].format(app.mention))
    await asyncio.sleep(1)

    try:
        db[message.chat.id] = []
        await Miku.stop_stream_force(message.chat.id)
    except:
        pass

    assistant = await get_assistant(message.chat.id)
    try:
        await assistant.resolve_peer(
            message.chat.username or message.chat.id
        )
    except:
        pass

    linked_chat = await get_cmode(message.chat.id)
    if linked_chat:
        try:
            db[linked_chat] = []
            await Miku.stop_stream_force(linked_chat)
        except:
            pass

    await msg.edit_text(_l["reload_5"].format(app.mention))


# ======================================================
# CLOSE BUTTON (AUTO DELETE)
# ======================================================

@app.on_callback_query(filters.regex("^close$") & ~BANNED_USERS)
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()

        close_msg = await query.message.reply_text(
            f"Cʟᴏsᴇᴅ ʙʏ : {query.from_user.mention}"
        )

        await query.message.delete()
        await asyncio.sleep(3)
        await close_msg.delete()

    except Exception:
        pass


# ======================================================
# STOP DOWNLOADING
# ======================================================

@app.on_callback_query(filters.regex("^stop_downloading$") & ~BANNED_USERS)
@ActualAdminCB
async def stop_downloading(_, query: CallbackQuery, _l):
    try:
        task = lyrical.get(query.message.id)

        if not task:
            return await query.answer(_l["tg_4"], show_alert=True)

        if task.done() or task.cancelled():
            return await query.answer(_l["tg_5"], show_alert=True)

        task.cancel()
        lyrical.pop(query.message.id, None)

        await query.answer(_l["tg_6"], show_alert=True)
        await query.edit_message_text(
            _l["tg_7"].format(query.from_user.mention)
        )

    except Exception:
        await query.answer(_l["tg_8"], show_alert=True)
