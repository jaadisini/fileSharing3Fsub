# (©)CodeXBotz
# By @Codeflix_Bots

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, CHANNEL_IDS
from helper_func import encode, get_message_id

# Helper function to check if the forwarded message is from a valid channel
def is_valid_channel(message, channels):
    return any([message.forward_from_chat and message.forward_from_chat.id == channel_id for channel_id in channels])

# Batch command to generate links for multiple posts
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    # First, ask for the first message to generate the link
    while True:
        try:
            first_message = await client.ask(
                text="Forward the First Message from Database Channel (with Quotes)..\n\nOr Send the Database Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded & filters.chat(CHANNEL_IDS)),  # Only forwarded messages from the specified channels
                timeout=60
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id and is_valid_channel(first_message, CHANNEL_IDS):
            break
        else:
            await first_message.reply("❌ Error\n\nIt's not from a valid Database Channel. Try again!", quote=True)
            continue

    # Then, ask for the second message to generate the link range
    while True:
        try:
            second_message = await client.ask(
                text="Forward the Last Message from Database Channel..! (with Quotes)\nOr Send the Database Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded & filters.chat(CHANNEL_IDS)),  # Only forwarded messages from the specified channels
                timeout=60
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id and is_valid_channel(second_message, CHANNEL_IDS):
            break
        else:
            await second_message.reply("❌ Error\n\nIt's not from a valid Database Channel. Try again!", quote=True)
            continue

    # Generate the link using the first database channel
    db_channel = client.db_channels[0]  # Only use the first database channel for generating the link

    string = f"get-{f_msg_id * abs(db_channel.id)}-{s_msg_id * abs(db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


# Genlink command to generate a link for a single post
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    # Ask for the message to generate the link
    while True:
        try:
            channel_message = await client.ask(
                text="Forward Message from Database Channel (with Quotes)\nOr Send the Database Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded & filters.chat(CHANNEL_IDS)),  # Only forwarded messages from the specified channels
                timeout=60
            )
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id and is_valid_channel(channel_message, CHANNEL_IDS):
            break
        else:
            await channel_message.reply("❌ Error\n\nIt's not from a valid Database Channel. Try again!", quote=True)
            continue

    # Generate the link using the first database channel
    db_channel = client.db_channels[0]  # Only use the first database channel for generating the link

    base64_string = await encode(f"get-{msg_id * abs(db_channel.id)}")
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


# Ignore random messages and prevent unwanted link generation
@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['batch', 'genlink']))
async def ignore_messages(client: Client, message: Message):
    # This will ensure random messages do not generate links
    await message.reply_text("Please use /genlink or /batch to generate links.", quote=True)