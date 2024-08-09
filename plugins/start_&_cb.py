from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from helper.database import db
from config import Config, Txt
from utils import verify_user, check_token, check_verification, get_token
import humanize
from time import sleep

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if len(message.command) > 1:
        data = message.command[1]
        if data.split("-", 1)[0] == "verify":
            userid = data.split("-", 2)[1]
            token = data.split("-", 3)[2]
            if str(message.from_user.id) != str(userid):
                return await message.reply_text(
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
            is_valid = await check_token(client, userid, token)
            if is_valid:
                await message.reply_text(
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all files till today midnight.</b>",
                    protect_content=True
                )
                await verify_user(client, userid, token)
            else:
                return await message.reply_text(
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
            return
    
    user = message.from_user
    await db.add_user(client, message)
    
    verification_url = await get_token(client, message.from_user.id, f"https://t.me/{Config.BOT_USERNAME}?start=")
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton('⛅ Uᴘᴅᴀᴛᴇs', url='https://t.me/aniflixClou'),
        InlineKeyboardButton('🌨️ Sᴜᴘᴘᴏʀᴛ', url='https://t.me/aniflixClou')
    ], [
        InlineKeyboardButton('❄️ Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('❗ Hᴇʟᴘ', callback_data='help')
    ], [
        InlineKeyboardButton('🔗 Verify Now', url=verification_url)
    ]])
    
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    try:
        user_id = message.from_user.id
        
        # Check if the user is verified
        is_verified = await check_verification(client, user_id)
        if not is_verified:
            # Send verification message and return
            verification_url = await get_token(client, user_id, f"https://t.me/{Config.BOT_USERNAME}?start=")
            await message.reply_text(
                "You need to verify your account before you can use this feature. Please verify your account using the following link:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🔗 Verify Now', url=verification_url)]
                ])
            )
            return
        
        # If verified, proceed with file renaming
        file = getattr(message, message.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size)

        if not Config.STRING_SESSION:
            if file.file_size > 4000 * 1024 * 1024:
                return await message.reply_text("Sorry, this bot does not support uploading files larger than 4GB")

        text = f"""**__What do you want me to do with this file?__**\n\n**File Name**: `{filename}`\n\n**File Size**: `{filesize}`"""
        buttons = [
            [InlineKeyboardButton("📝 Start Rename 📝", callback_data="rename")],
            [InlineKeyboardButton("✖️ Cancel ✖️", callback_data="close")]
        ]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
        
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file?__**\n\n**File Name**: `{filename}`\n\n**File Size**: `{filesize}`"""
        buttons = [
            [InlineKeyboardButton("📝 Start Rename 📝", callback_data="rename")],
            [InlineKeyboardButton("✖️ Cancel ✖️", callback_data="close")]
        ]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        print(f"Error in rename_start command: {e}")

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    try:
        data = query.data
        if data == "start":
            await query.message.edit_text(
                text=Txt.START_TXT.format(query.from_user.mention),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('⛅ Uᴘᴅᴀᴛᴇs', url='https://t.me/aniflixClou'), InlineKeyboardButton('🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/aniflixClou')],
                    [InlineKeyboardButton('❄️ Aʙᴏᴜᴛ', callback_data='about'), InlineKeyboardButton('❗ Hᴇʟᴘ', callback_data='help')]
                ])
            )
        elif data == "help":
            await query.message.edit_text(
                text=Txt.HELP_TXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✘ Close", callback_data="close"), InlineKeyboardButton("⟪ Back", callback_data="start")]
                ])
            )
        elif data == "about":
            await query.message.edit_text(
                text=Txt.ABOUT_TXT.format(client.mention),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✘ Close", callback_data="close"), InlineKeyboardButton("⟪ Back", callback_data="start")]
                ])
            )
        elif data == "close":
            try:
                await query.message.delete()
                await query.message.reply_to_message.delete()
                await query.message.continue_propagation()
            except:
                await query.message.delete()
                await query.message.continue_propagation()
    except Exception as e:
        print(f"Error in callback query handler: {e}")
