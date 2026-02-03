

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Miku(Client):
    def __init__(self):
        LOGGER(__name__).info(f"sᴛʀᴀᴛɪɴɢ ʙᴏᴛ...")
        super().__init__(
            name="KRITIMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention}</u> ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :-</b>\n\n"
                    f"ɪᴅ :- <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ :- {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ :- @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "ʙᴏᴛ ʜᴀs ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴄᴄᴇss ᴛʜᴇ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ. ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴅᴇᴅ ᴛʜᴇʀᴇ."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"ʙᴏᴛ ʜᴀs ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴄᴄᴇss ᴛʜᴇ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.\n  ʀᴇᴀsᴏɴ :- {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "ᴘʟᴇᴀsᴇ ᴘʀᴏᴍᴏᴛᴇ ʏᴏᴜʀ ʙᴏᴛ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ."
            )
            exit()

        LOGGER(__name__).info(f"ᴍᴜsɪᴄ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ᴀs {self.name}")

    async def stop(self):
        await super().stop()

# ======================================================
# ©️ 2025-26 All Rights Reserved by KRITI Bots (suraj08832) 😎
# 🧑‍💻 Developer : t.me/brahix
# 🔗 Source link : GitHub.com/suraj08832/Mikus-MusicV2
# 📢 Telegram channel : t.me/about_brahix
# =======================================================
