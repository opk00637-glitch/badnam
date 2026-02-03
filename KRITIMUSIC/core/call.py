# =======================================================
# © 2025-26 All Rights Reserved by Aarumi Bot (karma) 🚀
# This source code is under MIT License 📜 
# =======================================================

import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

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
from KRITIMUSIC.utils.formatters import check_duration, seconds_to_min, speed_converter
from KRITIMUSIC.utils.inline.play import stream_markup
from KRITIMUSIC.utils.stream.autoclear import auto_clean
from KRITIMUSIC.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}

async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)

class Call(PyTgCalls):
    def __init__(self):
        # Assistants Initialization
        self.userbot1 = Client(name="MikuAss1", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING1))
        self.one = PyTgCalls(self.userbot1, cache_duration=100)
        
        self.userbot2 = Client(name="MikuAss2", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING2))
        self.two = PyTgCalls(self.userbot2, cache_duration=100)
        
        self.userbot3 = Client(name="MikuXAss3", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING3))
        self.three = PyTgCalls(self.userbot3, cache_duration=100)
        
        self.userbot4 = Client(name="MikuXAss4", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING4))
        self.four = PyTgCalls(self.userbot4, cache_duration=100)
        
        self.userbot5 = Client(name="MikuAss5", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING5))
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    # --- Basic Controls ---

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    # --- Advanced Features ---

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        # FFmpeg seek logic
        stream = (AudioVideoPiped(file_path, HighQualityAudio(), MediumQualityVideo(), additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}")
                  if mode == "video" 
                  else AudioPiped(file_path, HighQualityAudio(), additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}"))
        await assistant.change_stream(chat_id, stream)

    async def join_call(self, chat_id: int, original_chat_id: int, link, video: Union[bool, str] = None):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)
        
        stream = AudioVideoPiped(link, HighQualityAudio(), MediumQualityVideo()) if video else AudioPiped(link, HighQualityAudio())
        
        try:
            await assistant.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(_["call_9"])
        except TelegramServerError:
            raise AssistantErr(_["call_10"])
        
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        
        if await is_autoend():
            autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        if not check:
            return await _clear_(chat_id)

        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                await set_loop(chat_id, loop - 1)
            
            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
        except Exception:
            await _clear_(chat_id)
            return

        # Play next track logic
        queued = check[0]["file"]
        videoid = check[0]["vidid"]
        video = True if str(check[0]["streamtype"]) == "video" else False
        
        # Stream Type selection
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            stream = AudioVideoPiped(link, HighQualityAudio(), MediumQualityVideo()) if video else AudioPiped(link, HighQualityAudio())
        else:
            stream = AudioVideoPiped(queued, HighQualityAudio(), MediumQualityVideo()) if video else AudioPiped(queued, HighQualityAudio())

        await client.change_stream(chat_id, stream)
        
        # UI Update
        img = await get_thumb(videoid)
        button = stream_markup(get_string(await get_lang(chat_id)), chat_id)
        await app.send_photo(
            chat_id=check[0]["chat_id"],
            photo=img,
            caption=f"<b>Started Streaming:</b> {check[0]['title']}",
            reply_markup=InlineKeyboardMarkup(button),
        )

    # --- Initialization ---

    async def start(self):
        LOGGER(__name__).info("Starting Miku Music Assistants...")
        assistants = [self.one, self.two, self.three, self.four, self.five]
        for ass in assistants:
            if ass.app.session_string: # Only start if string is provided
                await ass.start()

    async def decorators(self):
        @self.one.on_stream_end()
        @self.two.on_stream_end()
        @self.three.on_stream_end()
        @self.four.on_stream_end()
        @self.five.on_stream_end()
        async def stream_end_handler(client, update: Update):
            if isinstance(update, StreamAudioEnded):
                await self.change_stream(client, update.chat_id)

Miku = Call()
