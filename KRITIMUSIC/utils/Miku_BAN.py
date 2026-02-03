# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

from pyrogram import filters
from KRITIMUSIC.utils.admin_check import admin_check


USE_AS_BOT = True

def f_sudo_filter(filt, client, message):
    return bool(
        (
            (message.from_user and message.from_user.id in SUDO_USERS)
            or (message.sender_chat and message.sender_chat.id in SUDO_USERS)
        )
        and
        # t, lt, fl 2013
        not message.edit_date
    )


sudo_filter = filters.create(func=f_sudo_filter, name="SudoFilter")


def onw_filter(filt, client, message):
    if USE_AS_BOT:
        return bool(
            True
            and  # message.from_user.id in SUDO_USERS
            # t, lt, fl 2013
            not message.edit_date
        )
    else:
        return bool(
            message.from_user
            and message.from_user.is_self
            and
            # t, lt, fl 2013
            not message.edit_date
        )


f_onw_fliter = filters.create(func=onw_filter, name="OnwFilter")


async def admin_filter_f(filt, client, message):
    return (
        # t, lt, fl 2013
        not message.edit_date
        and await admin_check(message)
    )


admin_filter = filters.create(func=admin_filter_f, name="AdminFilter")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================
