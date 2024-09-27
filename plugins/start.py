import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

# Handles the basic /start command and subscription check
@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text

    if len(text) > 7:  # If the user starts with a link
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")
        except:
            return
        
        # Check if the user is subscribed
        if not await subscribed(client, message):
            buttons = [
                [InlineKeyboardButton(text="• Join Channel", url=f"https://t.me/{FORCESUB_CHANNEL}")],
                [InlineKeyboardButton(text="• Now Click Here •", url=f"https://t.me/{client.username}?start={text.split(' ', 1)[1]}")]
            ]
            await message.reply(
                text=FORCE_MSG.format(
                    first=message.from_user.first_name,
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True
            )
            return

        # If the user is subscribed, process the start link and provide the file
        if len(argument) == 3:
            start = int(int(argument[1]) / abs(client.db_channel.id))
            end = int(int(argument[2]) / abs(client.db_channel.id))
            ids = range(start, end + 1)
        elif len(argument) == 2:
            ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        
        temp_msg = await message.reply("Fetching file, please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await temp_msg.edit_text("Something went wrong!")
            return
        await temp_msg.delete()

        for msg in messages:
            if bool(CUSTOM_CAPTION) and bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "", filename=msg.document.file_name)
            else:
                caption = msg.caption.html if msg.caption else ""

            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None
            try:
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    
    # If the user starts without any arguments, send the regular start message
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚡️ About", callback_data="about"),
                InlineKeyboardButton("🍁 SeriesFlix", url="https://t.me/Team_Netflix/40")
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

# Handles force subscription
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="• Join Channel", url=client.invitelink2),
            InlineKeyboardButton(text="Join Channel •", url=client.invitelink3),
        ],
        [
            InlineKeyboardButton(text="• Join Channel •", url=client.invitelink),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='• Now Click Here •',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )