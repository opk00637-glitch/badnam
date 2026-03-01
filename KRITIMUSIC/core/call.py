import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
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
    if chat_id in db:
        db[chat_id].clear()
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call:
    def __init__(self):
        self.userbot1 = Client("MikuAss1", config.API_ID, config.API_HASH, session_string=str(config.STRING1))
        self.userbot2 = Client("MikuAss2", config.API_ID, config.API_HASH, session_string=str(config.STRING2))
        self.userbot3 = Client("MikuMikuAss3", config.API_ID, config.API_HASH, session_string=str(config.STRING3))
        self.userbot4 = Client("MikuAss4", config.API_ID, config.API_HASH, session_string=str(config.STRING4))
        self.userbot5 = Client("MikuAss5", config.API_ID, config.API_HASH, session_string=str(config.STRING5))

        self.one = PyTgCalls(self.userbot1, cache_duration=100)
        self.two = PyTgCalls(self.userbot2, cache_duration=100)
        self.three = PyTgCalls(self.userbot3, cache_duration=100)
        self.four = PyTgCalls(self.userbot4, cache_duration=100)
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

        self.assistants = [self.one, self.two, self.three, self.four, self.five]

    # ================= BASIC CONTROLS ================= #

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
        except:
            pass

    async def stop_stream_force(self, chat_id: int):
        for assistant in self.assistants:
            try:
                await assistant.leave_group_call(chat_id)
            except:
                pass
        await _clear_(chat_id)

    # ================= SPEED CONTROL ================= #

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)

        if str(speed) != "1.0":
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            os.makedirs(chatdir, exist_ok=True)
            out = os.path.join(chatdir, base)

            if not os.path.isfile(out):
                speed_map = {"0.5": 2.0, "0.75": 1.35, "1.5": 0.68, "2.0": 0.5}
                vs = speed_map.get(str(speed), 1.0)

                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", file_path,
                    "-filter:v", f"setpts={vs}*PTS",
                    "-filter:a", f"atempo={speed}",
                    out,
                ]

                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
        else:
            out = file_path

        dur = await asyncio.get_event_loop().run_in_executor(None, check_duration, out)
        played, con_seconds = speed_converter(playing[0]["played"], speed)
        duration = seconds_to_min(int(dur))

        stream = (
            AudioVideoPiped(out, HighQualityAudio(), MediumQualityVideo(),
                            additional_ffmpeg_parameters=f"-ss {played} -to {duration}")
            if playing[0]["streamtype"] == "video"
            else AudioPiped(out, HighQualityAudio(),
                            additional_ffmpeg_parameters=f"-ss {played} -to {duration}")
        )

        await assistant.change_stream(chat_id, stream)

        db[chat_id][0].update({
            "played": con_seconds,
            "dur": duration,
            "seconds": int(dur),
            "speed_path": out,
            "speed": speed,
        })

    # ================= STREAM MANAGEMENT ================= #

    async def join_call(self, chat_id: int, original_chat_id: int, link,
                        video: Union[bool, str] = None):

        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        stream = (
            AudioVideoPiped(link, HighQualityAudio(), MediumQualityVideo())
            if video else AudioPiped(link, HighQualityAudio())
        )

        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
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
            await _clear_(chat_id)
            try:
                return await client.leave_group_call(chat_id)
            except:
                return

        loop = await get_loop(chat_id)

        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                await set_loop(chat_id, loop - 1)
                popped = None

            if popped:
                await auto_clean(popped)

            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)

        except:
            await _clear_(chat_id)
            try:
                await client.leave_group_call(chat_id)
            except:
                pass
            return

        queued = check[0]["file"]
        streamtype = check[0]["streamtype"]
        video = True if str(streamtype) == "video" else False

        stream = (
            AudioVideoPiped(queued, HighQualityAudio(), MediumQualityVideo())
            if video else AudioPiped(queued, HighQualityAudio())
        )

        try:
            await client.change_stream(chat_id, stream)
        except:
            return

    # ================= UTILITIES ================= #

    async def ping(self):
        pings = []
        for ass in self.assistants:
            try:
                pings.append(await ass.ping())
            except:
                pass
        return str(round(sum(pings) / len(pings), 3)) if pings else "0.0"

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        if config.STRING1: await self.one.start()
        if config.STRING2: await self.two.start()
        if config.STRING3: await self.three.start()
        if config.STRING4: await self.four.start()
        if config.STRING5: await self.five.start()

    async def decorators(self):
        for assistant in self.assistants:

            @assistant.on_stream_end()
            async def stream_end_handler(client, update: Update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(client, update.chat_id)


Miku = Call()
