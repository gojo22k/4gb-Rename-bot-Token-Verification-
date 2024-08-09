import random
from helper.ffmpeg import fix_thumb, take_screen_shot
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from PIL import Image
import asyncio
import os
import time
from helper.utils import add_prefix_suffix
from config import Config
from utils import verify_user, check_token, check_verification, get_token

app = Client("test", api_id=Config.STRING_API_ID,
             api_hash=Config.STRING_API_HASH, session_string=Config.STRING_SESSION)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def prompt_rename(client, message):
    # Check if the user is verified
    is_verified = await check_verification(client, message.from_user.id)
    if not is_verified:
        # Send verification message and return
        verification_url = await get_token(client, message.from_user.id, f"https://t.me/{Config.BOT_USERNAME}?start=")
        await message.reply_text(
            "You need to verify your account before you can use this feature. Please verify your account using the following link:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🔗 Verify Now', url=verification_url)]
            ])
        )
        return
    
    await message.reply_text("✏️ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ...",
                             reply_to_message_id=message.id,
                             reply_markup=ForceReply(True))


# Define the main message handler for private messages with replies
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()

        await start_renaming(client, file, new_name)

async def start_renaming(bot, file, new_name):
    # Creating Directory for Metadata
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    # Extracting necessary information
    prefix = await db.get_prefix(file.chat.id)
    suffix = await db.get_suffix(file.chat.id)
    new_filename_ = new_name

    try:
        # adding prefix and suffix
        new_filename = add_prefix_suffix(new_filename_, prefix, suffix)

    except Exception as e:
        return await file.reply(f"⚠️ Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴄᴀɴ'ᴛ ᴀʙʟᴇ ᴛᴏ sᴇᴛ Pʀᴇғɪx ᴏʀ Sᴜғғɪx ☹️ \n\n❄️ Cᴏɴᴛᴀᴄᴛ Mʏ Cʀᴇᴀᴛᴏʀ -> @aniflixClou\nError: {e}")

    file_path = f"downloads/{new_filename}"

    ms = await file.reply("Wᴀɪᴛ Fᴏʀ Fᴇᴡ Mɪɴᴜᴛᴇs__\n\n**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Fɪʟᴇ....**")

    # Stream download to handle large files
    try:
        path = await bot.download_media(
            message=file, 
            file_name=file_path, 
            progress=progress_for_pyrogram, 
            progress_args=("🦋 Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()),
            in_memory=False
        )
    except Exception as e:
        return await ms.edit(e)

    _bool_metadata = await db.get_metadata(file.chat.id)

    if _bool_metadata:
        metadata_path = f"Metadata/{new_filename}"
        metadata = await db.get_metadata_code(file.chat.id)
        if metadata:
            await ms.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")

            cmd = f"""ffmpeg -i "{path}" {metadata} "{metadata_path}" """
            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            er = stderr.decode()

            if er:
                return await ms.edit(str(er) + "\n\n**Error**")

            await ms.edit("**Mᴇᴛᴀᴅᴀᴛᴀ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ ғɪʟᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\n ✨ Wᴀɪᴛ Fᴏʀ Fᴇᴡ Sᴇᴄᴏɴᴅs__\n\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅ...**")
    else:
        await ms.edit("✨ Wᴀɪᴛ Fᴏʀ Fᴇᴡ Sᴇᴄᴏɴᴅs__\n\n\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅ....**")

    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()

    except:
        pass

    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(file.chat.id)
    c_thumb = await db.get_thumbnail(file.chat.id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    if media.thumbs or c_thumb:
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
            width, height, ph_path = await fix_thumb(ph_path)
        else:
            try:
                ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                width, height, ph_path = await fix_thumb(ph_path_)
            except Exception as e:
                ph_path = None
                print(e)

    # Stream upload to handle large files
    try:
        await bot.send_video(
            file.chat.id,
            video=metadata_path if _bool_metadata else file_path,
            caption=caption,
            thumb=ph_path,
            width=width,
            height=height,
            duration=duration,
            progress=progress_for_pyrogram,
            progress_args=("✨__**Wᴀɪᴛ Fᴏʀ Fᴇᴡ Sᴇᴄᴏɴᴅs**__\n\n🌨️ **Uᴩʟᴏaᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()),
            supports_streaming=True  # To support streaming of large files
        )

        await ms.delete()

        # Clean up
        try:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
        except:
            pass

    except Exception as e:
        await ms.edit(f" Error {e} occurred while uploading")
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        if metadata_path:
            os.remove(metadata_path)
