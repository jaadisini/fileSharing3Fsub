# (©) Codeflix_Bots

import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FORCESUB_CHANNEL, FORCESUB_CHANNEL2, FORCESUB_CHANNEL3
from helper_func import encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


async def subscribed(client, message):
    user_id = message.from_user.id
    joined_channels = []

    # Check each channel and append if the user is a member
    for channel in [FORCESUB_CHANNEL, FORCESUB_CHANNEL2, FORCESUB_CHANNEL3]:
        try:
            member_status = await client.get_chat_member(channel, user_id)
            if member_status.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                joined_channels.append(channel)
        except Exception as e:
            print(f"Error checking subscription for {channel}: {e}")

    return joined_channels


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    required_channels = [FORCESUB_CHANNEL, FORCESUB_CHANNEL2, FORCESUB_CHANNEL3]
    user_joined_channels = await subscribed(client, message)

    if not all(channel in user_joined_channels for channel in required_channels):
        # User hasn't joined all channels
        missing_channels = [channel for channel in required_channels if channel not in user_joined_channels]
        buttons = [[InlineKeyboardButton("Join Channel", url=client.invitelink[i])] for i, channel in enumerate(missing_channels)]

        await message.reply(
            "You need to join these channels to access content:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    text = message.text
    if len(text) > 7:
        # Handle content delivery when using an encoded link
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")

            # Logic for fetching and sending messages/files
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
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                    filename=msg.document.file_name)
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
            return
        except:
            return

    # If user has joined all channels, proceed with normal start message
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
                pass
            total += 1

        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴍʏ sᴇɴᴘᴀɪ!!</u>

        ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{total}</code>
        ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
        ʙʟᴏᴄᴋᴇᴅ ᴜꜱᴇʀꜱ: <code>{blocked}</code>
        ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
        ᴜɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code></b></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply("<code>Reply to a message to broadcast.</code>")
        await asyncio.sleep(8)
        await msg.delete()