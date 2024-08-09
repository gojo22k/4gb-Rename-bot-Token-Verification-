import re
import os
import time
from os import environ

# Shortlink API configuration
API = environ.get("API", "d92f120bd61ee18e32d4a5e4f4cfad8d747eeec4") # shortlink api
URL = environ.get("URL", "publicearn.com") # shortlink domain without https://
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "") # how to open link 
BOT_USERNAME = environ.get("BOT_USERNAME", "AniflixAutoFilterBot") # bot username without @
VERIFY = environ.get("VERIFY", "True") == "True"  # Convert string to boolean

id_pattern = re.compile(r'^.\d+$')

class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "25198711")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "2a99a1375e26295626c04b4606f72752")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7393513769:AAGRttVn6-EXPI5GdRpeepDpXjnnU_ukqME")  # ⚠️ Required

    # premium 4g renaming client
    STRING_API_ID = os.environ.get("STRING_API_ID", "")
    STRING_API_HASH = os.environ.get("STRING_API_HASH", "")
    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    # database config
    DB_NAME = os.environ.get("DB_NAME", "Aniflix")
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://Aniflix:Lipun123@aniflix.q2wina5.mongodb.net/?retryWrites=true&w=majority&appName=Aniflix")  # ⚠️ Required

    # other configs
    BOT_UPTIME = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/9c910cbc74144b3b2efce.jpg")
    ADMIN = [int(admin) if id_pattern.search(
        admin) else admin for admin in os.environ.get('ADMIN', '1740287480').split()]  # ⚠️ Required
    
    FORCE_SUB = os.environ.get("FORCE_SUB", "aniflixClou") # ⚠️ Required Username without @
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002219568827"))  # ⚠️ Required
    FLOOD = int(os.environ.get("FLOOD", '105'))
    BANNED_USERS = set(int(x) for x in os.environ.get(
        "BANNED_USERS", "1234567890").split())

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))

    # Add the missing attributes
    VERIFY = VERIFY
    BOT_USERNAME = BOT_USERNAME
    VERIFY_TUTORIAL = VERIFY_TUTORIAL


class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hɪ {} ♡゙,\n\n◈ I Aᴍ A Pᴏᴡᴇʀғᴜʟ Fɪʟᴇ Rᴇɴᴀᴍᴇʀ Bᴏᴛ.
◈ I Cᴀɴ Rᴇɴᴀᴍᴇ Fɪʟᴇs ᴜᴘᴛᴏ 4GB, Cʜᴀɴɢᴇ Tʜᴜᴍʙɴᴀɪʟs, Cᴏɴᴠᴇʀᴛ Bᴇᴛᴡᴇᴇɴ Vɪᴅᴇᴏ Aɴᴅ Fɪʟᴇ, Aɴᴅ Sᴜᴘᴘᴏʀᴛ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟs Aɴᴅ Cᴀᴘᴛɪᴏɴs.\n\n• Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ : @Straw_Hat_Bots
"""

    ABOUT_TXT = """<b>╭───────────⍟
• ᴍy ɴᴀᴍᴇ : {}
• ᴘʀᴏɢʀᴀᴍᴇʀ : <a href=https://t.me/Urr_Sanjii>𝐒ᴀɴJɪ 𝐒αᴍᴀ</a>
• ɴᴇᴛᴡᴏʀᴋ : <a href=https://t.me/Straw_Hat_bots>𝐒ᴛʀᴀᴡ 𝐇ᴀᴛ 𝐁ᴏᴛs</a>
• ᴄʜᴀᴛ ɢʀᴏᴜᴘ: <a href=https://t.me/Straw_hat_support>sᴜᴘᴘᴏʀᴛ</a>
• ᴍʏ ᴏᴡɴᴇʀ / ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/Straw_Hat_Bots>𝐒ᴛʀᴀᴡ 𝐇ᴀᴛ ꭙ 𝐁ᴏᴛs </a>
╰───────────────⍟ """

    HELP_TXT = """
🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>
  
<b>•></b> /start Tʜᴇ Bᴏᴛ Aɴᴅ Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.


📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>

<b>•></b> /set_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ ᴀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /see_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /del_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
Exᴀᴍᴩʟᴇ:- <code> /set_caption 📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration} </code>

✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ \nAɴᴅ Aᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].           


<b>➜ ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> <a href=https://t.me/Straw_Hat_Bots>𝐒ᴛʀᴀᴡ 𝐇ᴀᴛ ꭙ 𝐁ᴏᴛs</a>
"""

    SEND_METADATA = """
❪ SET CUSTOM METADATA ❫

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

◦ <code> -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @Straw_Hat_Bots" -metadata author="@straw_hat_bots" -metadata:s:s title="Subtitled By :- @Straw_Hat_Bots" -metadata:s:a title="By :- @Straw_Hat_Bots" -metadata:s:v title="By:- @Straw_Hat_bots" </code>

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @aniflixClou
"""

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱➜
➜ 🗃️ sɪᴢᴇ: {1} | {2}
➜ ⏳️ ᴅᴏɴᴇ : {0}%
➜ 🚀 sᴘᴇᴇᴅ: {3}/s
➜ ⏰️ ᴇᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➜ </b>"""
