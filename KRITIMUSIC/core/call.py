# =======================================================
# © 2025-26 All Rights Reserved by Aarumi Bot (karma) 🚀
# This source code is under MIT License 📜
# =======================================================

import asyncio
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    MediumQualityVideo,
)

import config
from KRITIMUSIC import LOGGER, YouTube, app
from KRITIMUSIC.misc import db
from KRITIMUSIC.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from KRITIMUSIC.utils.exceptions import AssistantErr
from KRITIMUSIC.utils.inline.play import stream_markup
from KRITIMUSIC.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}


async def _clear_(chat_id: int):
    db.pop(chat_id, None)
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call:
    def __init__(self):

        self.userbots = []
        self.calls = []

        for i, string in enumerate(
            [config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5],
            start=1,
        ):
            if not string:
                continue

            userbot = Client(
                name=f"MikuAss{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(string),
            )
            call = PyTgCalls(userbot, cache_duration=100)

            self.userbots.append(userbot)
            self.calls.append(call)

    # ---------------- BASIC CONTROLS ---------------- #

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await _clear_(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    # ---------------- JOIN STREAM ---------------- #

    async def join_call(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = False,
    ):
        assistant = await group_assistant(self, chat_id)
        lang = get_string(await get_lang(chat_id))

        stream = (
            AudioVideoPiped(link, HighQualityAudio(), MediumQualityVideo())
            if video
            else AudioPiped(link, HighQualityAudio())
        )

        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().local_stream,
            )
        except NoActiveGroupCall:
            raise AssistantErr(lang["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(lang["call_9"])
        except TelegramServerError:
            raise AssistantErr(lang["call_10"])

        await add_active_chat(chat_id)
        await music_on(chat_id)

        if video:
            await add_active_video_chat(chat_id)

        if await is_autoend():
            autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    # ---------------- AUTO NEXT ---------------- #

    async def change_stream(self, client: PyTgCalls, chat_id: int):
        queue = db.get(chat_id)
        if not queue:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)

        loop = await get_loop(chat_id)

        if loop == 0:
            queue.pop(0)
        else:
            await set_loop(chat_id, loop - 1)

        if not queue:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)

        data = queue[0]
        video = data["streamtype"] == "video"

        if "live_" in data["file"]:
            _, link = await YouTube.video(data["vidid"], True)
        else:
            link = data["file"]

        stream = (
            AudioVideoPiped(link, HighQualityAudio(), MediumQualityVideo())
            if video
            else AudioPiped(link, HighQualityAudio())
        )

        await client.change_stream(chat_id, stream)

        thumb = await get_thumb(data["vidid"])
        buttons = stream_markup(get_string(await get_lang(chat_id)), chat_id)

        await app.send_photo(
            chat_id=data["chat_id"],
            photo=thumb,
            caption=f"<b>Now Playing:</b> {data['title']}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    # ---------------- START ---------------- #

    async def start(self):
        LOGGER(__name__).info("🚀 Starting Miku Music Assistants")

        for userbot, call in zip(self.userbots, self.calls):
            await userbot.start()
            await call.start()

            @call.on_stream_end()
            async def stream_end_handler(client, update: Update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(client, update.chat_id)


Miku = Call()
