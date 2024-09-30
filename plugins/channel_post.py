#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_IDS, DISABLE_CHANNEL_BUTTON
from helper_func import encode

# Handler for admin posts
@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    try:
        # Loop through each channel ID to post the message to multiple channels
        for channel_id in CHANNEL_IDS:
            try:
                post_message = await message.copy(chat_id=channel_id, disable_notification=True)
                converted_id = post_message.id * abs(channel_id)
                string = f"get-{converted_id}"
                base64_string = await encode(string)
                link = f"https://t.me/{client.username}?start={base64_string}"
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

                # Edit the reply message with the generated link
                await reply_text.edit(f"<b>Here is your link for channel {channel_id}</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

                if not DISABLE_CHANNEL_BUTTON:
                    try:
                        await post_message.edit_reply_markup(reply_markup)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        await post_message.edit_reply_markup(reply_markup)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                post_message = await message.copy(chat_id=channel_id, disable_notification=True)
            except Exception as e:
                print(e)
                await reply_text.edit_text("Something went wrong!")
                return

    except Exception as e:
        print(f"Error while posting to channel: {e}")
        await reply_text.edit_text("Something went wrong!")


# Handler for new posts in the channel
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_IDS))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    # Loop through each channel ID
    for channel_id in CHANNEL_IDS:
        if message.chat.id == channel_id:  # Check if the message is from a valid channel
            converted_id = message.id * abs(channel_id)
            string = f"get-{converted_id}"
            base64_string = await encode(string)
            link = f"https://t.me/{client.username}?start={base64_string}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

            try:
                await message.edit_reply_markup(reply_markup)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.edit_reply_markup(reply_markup)
            except Exception:
                pass