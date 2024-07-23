


import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.config import Config
from plugins.script import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.add import add_user_to_database
from plugins.functions.forcesub import handle_force_subscribe
from utils import verify_user, check_token
from database.adduser import AddUser


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    await add_user_to_database(bot, update)
    await bot.send_message(
        Config.LOG_CHANNEL,
           f"#NEW_USER: \n\nNew User [{update.from_user.first_name}](tg://user?id={update.from_user.id}) started @{Config.BOT_USERNAME} !!"
    )
    
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    if len(update.command) != 2:
        await update.reply_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=Translation.START_BUTTONS
        )
        return

    data = update.command[1]

    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(update.from_user.id) != str(userid):
            return await update.reply_text(
                text="<b>ᴇxᴘɪʀᴇᴅ ʟɪɴᴋ ᴏʀ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ !</b>",
                protect_content=True
            )
        is_valid = await check_token(bot, userid, token)
        if is_valid == True:
            await update.reply_text(
                text=f"<b>ʜᴇʟʟᴏ {update.from_user.mention} 👋,\nʏᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\n\nɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴜʀʟ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛɪʟʟ ᴛᴏᴅᴀʏ ᴍɪᴅɴɪɢʜᴛ.</b>",
                protect_content=True
            )
            await verify_user(bot, userid, token)
            sender = update.from_user
            username = f"@{sender.username}" if sender.username else f"{sender.first_name} {sender.last_name or ''}"
            # Send message to the bot admin or log channel about the verification
            chat_id = -1002239847745  # Replace with actual admin ID
            thread_id = 4064
            admin_message = f"**User {username}**\nverified access with \n**URL: {data}**"
            await bot.send_message(chat_id, admin_message, reply_to_message_id=thread_id)

    
        else:
            return await update.reply_text(
                text="<b>ᴇxᴘɪʀᴇᴅ ʟɪɴᴋ ᴏʀ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ !</b>",
                protect_content=True
            )


