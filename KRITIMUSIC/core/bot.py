from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Miku(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
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

        # Get bot info safely
        self.me = await self.get_me()
        self.id = self.me.id
        self.name = f"{self.me.first_name or ''} {self.me.last_name or ''}".strip()
        self.username = self.me.username or "NoUsername"
        self.mention = self.me.mention

        # Send startup message
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention}</b></u>\n\n"
                    f"<b>Bot Started Successfully ✅</b>\n\n"
                    f"<b>ID :</b> <code>{self.id}</code>\n"
                    f"<b>Name :</b> {self.name}\n"
                    f"<b>Username :</b> @{self.username}"
                ),
                parse_mode=ParseMode.HTML,
            )

        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot cannot access the log group/channel. Make sure bot is added there."
            )
            raise SystemExit()

        except Exception as ex:
            LOGGER(__name__).error(
                f"Failed to access log group/channel. Reason: {type(ex).__name__}"
            )
            raise SystemExit()

        # Check admin status
        member = await self.get_chat_member(config.LOGGER_ID, self.id)

        if member.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote the bot as ADMIN in the log group/channel."
            )
            raise SystemExit()

        LOGGER(__name__).info(f"Music Bot Started Successfully as {self.name}")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("Bot Stopped Successfully")
