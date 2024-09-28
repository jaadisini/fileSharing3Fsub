# (©)CodeXBotz
# Recoded By @Codeflix_Bots

import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import is_subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    text = message.text
    # If the user started the bot with an encoded link
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return

        # Decoding the link
        string = await decode(base64_string)
        argument = string.split("-")

        # Check subscription status for each channel
        unsubscribed_buttons = []

        # Check for each channel and add join button if not subscribed
        if not await is_subscribed(client, message.from_user.id, client.invitelink):
            unsubscribed_buttons.append([InlineKeyboardButton(text=" 🔴 Join Channel ", url=client.invitelink)])

        if not await is_subscribed(client, message.from_user.id, client.invitelink2):
            unsubscribed_buttons.append([InlineKeyboardButton(text=" 🔵 Join Channel ", url=client.invitelink2)])

        if not await is_subscribed(client, message.from_user.id, client.invitelink3):
            unsubscribed_buttons.append([InlineKeyboardButton(text=" 🟢 Join Channel ", url=client.invitelink3)])

        # If user is not subscribed to one or more channels
        if unsubscribed_buttons:
            unsubscribed_buttons.append([InlineKeyboardButton(text=' 🔄 Try Again ', url=f"https://t.me/{client.username}?start={message.command[1]}")])
            await message.reply(
                text=FORCE_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=InlineKeyboardMarkup(unsubscribed_buttons),
                quote=True,
                disable_web_page_preview=True
            )
            return

        # If subscribed to all channels, give access to files
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("ᴡᴀɪᴛ ʙʀᴏᴏ...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("ɪ ꜰᴇᴇʟ ʟɪᴋᴇ ᴛʜᴇʀᴇ ɪꜱ ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ..!")
            return
        await temp_msg.delete()

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                )
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        # Regular start message if the user has not used a special link
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💠 About ", callback_data="about"),
                    InlineKeyboardButton('🔒 Close ', callback_data="close")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

# ============================================================================================================##

WAIT_MSG = "<b>ᴡᴏʀᴋɪɴɢ....</b>"

REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"

# ============================================================================================================##

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} ᴜꜱᴇʀꜱ ᴀʀᴇ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcast in progress, please wait...</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""Broadcast completed my senpai!!

Total users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked users: <code>{blocked}</code>
Deleted accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_callback_query(filters.regex('close'))
async def close_button(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()