# =======================================================
# ©️ 2025-26 All Rights Reserved by kriti Bots (kriti) 🚀
 
# 📩 DM for permission : kriti 
# =======================================================

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

import config
from KRITIMUSIC import app

class BUTTONS(object):
    BBUTTON = [
    [
        InlineKeyboardButton("• ᴀᴄᴛɪᴏɴ •", callback_data="TOOL_BACK HELP_06"),
        InlineKeyboardButton("• ᴀɴᴛɪ-ғʟᴏᴏᴅ •", callback_data="TOOL_BACK HELP_11"),
        InlineKeyboardButton("• ᴀᴘᴘʀᴏᴠᴀʟ •", callback_data="TOOL_BACK HELP_12"),
    ],
    [
        InlineKeyboardButton("• ᴄʜᴀᴛ-ɢᴘᴛ •", callback_data="TOOL_BACK HELP_01"),
        InlineKeyboardButton("• ɢɪᴛʜᴜʙ •", callback_data="TOOL_BACK HELP_09"),
        InlineKeyboardButton("• ɢʀᴏᴜᴘ •", callback_data="TOOL_BACK HELP_07"),
    ],
    [
        InlineKeyboardButton("• ʜɪsᴛᴏʀʏ •", callback_data="TOOL_BACK HELP_08"),
        InlineKeyboardButton("• ɪɴғᴏ •", callback_data="TOOL_BACK HELP_03"),
        InlineKeyboardButton("• ᴘᴜʀɢᴇ •", callback_data="TOOL_BACK HELP_13"),
    ],
    [
        InlineKeyboardButton("• sᴛɪᴄᴋᴇʀ•", callback_data="TOOL_BACK HELP_05"),
        InlineKeyboardButton("• ᴛᴀɢ-ᴀʟʟ •", callback_data="TOOL_BACK HELP_04"),
        InlineKeyboardButton("• ᴛᴏᴏʟs •", callback_data="TOOL_BACK HELP_10"),
    ],
    [
        InlineKeyboardButton("• ᴠᴄ-ᴛᴏᴏʟs •", callback_data="TOOL_BACK HELP_14"),
        InlineKeyboardButton("• ᴡʜɪsᴘᴇʀ •", callback_data="TOOL_BACK HELP_02"),
    ],
    [
        InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="MAIN_CP"),
    ]
]
    
    
    
    
    PBUTTON = [
        [
            InlineKeyboardButton("˹ ᴄσηᴛᴧᴄᴛ ˼", url="https://badnam_xd"),
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="MAIN_CP"),
        ]
        ]
    
    ABUTTON = [
        [
            InlineKeyboardButton("˹ sυᴘᴘσʀᴛ ˼", url="https://t.me/+8XQCCzEVYQY2NWJl"),
            InlineKeyboardButton("˹ υᴘᴅᴧᴛєs ˼", url="https://t.me/kriti_update"),
        ],
        [  
            InlineKeyboardButton("˹ ᴘʀᴏᴍᴏ ˼", url="https://t.me/badnam_xd?text=𝖧ᴇʏ%20ʙᴀʙʏ%20%20😄%20ɪ%20ᴡᴀɴᴛ%20ᴘᴀɪᴅ%20ᴘʀᴏᴍᴏᴛɪᴏɴ,%20ɢɪᴠᴇ%20ᴍᴇ%20ᴘʀɪᴄᴇ%20ʟɪsᴛ%20😙"),
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="settingsback_helper"),
        ]
        ]
    
    SBUTTON = [
        [
            InlineKeyboardButton("ϻᴜѕɪᴄ", callback_data="settings_back_helper"),
            InlineKeyboardButton("ϻᴧηᴧɢєϻєηᴛ", callback_data="TOOL_CP"),
        ],
        
        [
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ᴛσ ʜσϻє ⌯", callback_data="settingsback_helper"),
            
        ]
        ]
