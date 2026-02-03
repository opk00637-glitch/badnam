# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================

import time

import psutil

from KRITIMUSIC.misc import _boot_
from KRITIMUSIC.utils.formatters import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    UP = f"{get_readable_time(bot_uptime)}"
    CPU = f"{psutil.cpu_percent(interval=0.5)}%"
    RAM = f"{psutil.virtual_memory().percent}%"
    DISK = f"{psutil.disk_usage('/').percent}%"
    return UP, CPU, RAM, DISK

# ======================================================
# ©️ 2025-26 All Rights Reserved by Kirti 😎

# 🧑‍💻 Developer : t.me/lll_APNA_BADNAM_BABY_lll
# 🔗 Source link : https://github.com/Badnam019
# 📢 Telegram channel : t.me/lll_APNA_BADNAM_BABY_lll
# =======================================================
