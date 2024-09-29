#(©)Codeflix_Bots

import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FORCESUB_CHANNEL, FORCESUB_CHANNEL2, FORCESUB_CHANNEL3
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is already present in the database
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except:
            pass

    # Check for any encoded link in the message
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")

            # Handle content delivery based on the encoded link
            await handle_encoded_link(client, message, argument)

        except:
            await message.reply("Invalid link or something went wrong!")
        return

    # Force-Join logic
    channels_to_join = []

    # Check if the user has joined each force-sub channel
    try:
        member_status_1 = await client.get_chat_member(FORCESUB_CHANNEL, user_id)
        if member_status_1.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            channels_to_join.append(InlineKeyboardButton(text="Join Channel 1", url=client.invitelink))
    except:
        pass

    try:
        member_status_2 = await client.get_chat_member(FORCESUB_CHANNEL2, user_id)
        if member_status_2.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            channels_to_join.append(InlineKeyboardButton(text="Join Channel 2", url=client.invitelink2))
    except:
        pass

    try:
        member_status_3 = await client.get_chat_member(FORCESUB_CHANNEL3, user_id)
        if member_status_3.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            channels_to_join.append(InlineKeyboardButton(text="Join Channel 3", url=client.invitelink3))
    except:
        pass

    # If user hasn't joined all channels, show remaining ones
    if channels_to_join:
        buttons = [channels_to_join]
        buttons.append([InlineKeyboardButton(text="• ɴᴏᴡ ᴄʟɪᴄᴋ ʜᴇʀᴇ •", url=f"https://t.me/{client.username}?start={message.command[1]}")])
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
        return

    # If the user has joined all channels, proceed with normal start message
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⚡️ ᴀʙᴏᴜᴛ", callback_data="about")],
            [InlineKeyboardButton('🍁 sᴇʀɪᴇsғʟɪx', url='https://t.me/Team_Netflix/40')]
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


async def handle_encoded_link(client: Client, message: Message, argument: list):
    """Handles the logic for processing an encoded link."""
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
            caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
        else:
            caption = "" if not msg.caption else msg.caption.html

        if DISABLE_CHANNEL_BUTTON:
            reply_markup = msg.reply_markup
        else:
            reply_markup = None

        try:
            await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            await asyncio.sleep(0.5)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
        except:
            pass


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="<b>ᴡᴏʀᴋɪɴɢ....</b>")
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

        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪʟʟ ᴡᴀɪᴛ ʙʀᴏᴏ... </i>")
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
            total += 1

        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>
        ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{total}</code>
        ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
        ʙʟᴏᴄᴋᴇᴅ: <code>{blocked}</code>
        ᴅᴇʟᴇᴛᴇᴅ: <code>{deleted