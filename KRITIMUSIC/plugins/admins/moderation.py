# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

from KRITIMUSIC import app
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from KRITIMUSIC.utils.Miku_BAN import admin_filter
from pyrogram.types import ChatPermissions

@app.on_message(filters.command("unbanall") & admin_filter)
async def unban_all(_, msg):
    chat_id = msg.chat.id

    me = await app.get_me()
    BOT_ID = me.id

    try:
        bot = await app.get_chat_member(chat_id, BOT_ID)
        bot_permission = bot.privileges.can_restrict_members if bot.privileges else False

        if not bot_permission:
            await msg.reply_text(
                "**ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ.**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="stop")]]
                ),
            )
            return

        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)

        if not banned_users:
            await msg.reply_text("**ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ᴛᴏ ᴜɴʙᴀɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**")
            return

        unbanned_count = 0
        for user_id in banned_users:
            try:
                await app.unban_chat_member(chat_id, user_id)
                unbanned_count += 1
            except Exception:
                pass

        await msg.reply_text(
            f"**ᴜɴʙᴀɴɴᴇᴅ `{unbanned_count}` ᴜsᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ✅**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="stop")]]
            ),
        )

    except Exception as e:
        await msg.reply_text(
            f"**sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ :-** `{e}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="stop")]]
            ),
        )


@app.on_message(filters.command("unmuteall") & admin_filter)
async def unmute_all(_, msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    

    bot = await app.get_chat_member(chat_id, user_id)
    if not (bot.privileges and bot.privileges.can_restrict_members):
        return await msg.reply_text("**⚠️ ɴᴏ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀs.**")

    count = 0
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
        try:
            await app.restrict_chat_member(
                chat_id,
                m.user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True
                )
            )
            count += 1
            print(f"**✅ ᴜɴᴍᴜᴛᴇᴅ {m.user.mention}**")
        except Exception as e:
            print(f"❌ {m.user.id} - {e}")

    if count == 0:
        await msg.reply_text("**😶 ɴᴏ ᴍᴜᴛᴇᴅ ᴍᴇᴍʙᴇʀs ғᴏᴜɴᴅ.**")
    else:
        await msg.reply_text(f"**🔊 ᴜɴᴍᴜᴛᴇᴅ `{count}` ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ ✅**")



@app.on_message(filters.command(["unpinall"]) & filters.group)
async def unpinall_command(client, message):
    chat = message.chat
    admin_id = message.from_user.id
    member = await chat.get_member(admin_id)

    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] \
       or not member.privileges.can_pin_messages:
        return await message.reply_text(
            "**⚠ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴘɪɴ ᴍᴇssᴀɢᴇs.**"
        )

    await message.reply_text(
        "**❓ ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴᴘɪɴ ᴀʟʟ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ᴄʜᴀᴛ?**",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("✔ ʏᴇs", callback_data="unpin=yes"),
                InlineKeyboardButton("✖ ɴᴏ", callback_data="unpin=no")
            ]]
        )
    )


@app.on_callback_query(filters.regex(r"^unpin=(yes|no)$"))
async def unpin_callback(client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    action = CallbackQuery.data.split("=")[1]

    if action == "yes":
        await client.unpin_all_chat_messages(chat_id)
        text = "**✅ ᴀʟʟ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ʜᴀᴠᴇ ʙᴇᴇɴ ᴜɴᴘɪɴɴᴇᴅ!**"
    else:
        text = "**❌ ᴏᴋᴀʏ, ɪ ᴡɪʟʟ ɴᴏᴛ ᴜɴᴘɪɴ ᴀɴʏᴛʜɪɴɢ.**"

    await CallbackQuery.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]]
        )
)

@app.on_callback_query(filters.regex("^stop$"))
async def stop_callback(_, query):
    await query.message.delete()

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================
