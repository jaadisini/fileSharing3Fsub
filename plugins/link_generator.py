# (©)CodeXBotz
# By @Codeflix_Bots

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

# Dictionary to store the cancellation status for each user
cancel_status = {}

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    user_id = message.from_user.id
    cancel_status[user_id] = False  # Initialize the cancel flag for this user

    while True:
        if cancel_status.get(user_id):
            await message.reply("🚫 Process canceled.")
            return
        try:
            first_message = await client.ask(
                text="Forward the First Message from Database Channel (with Quotes)..\n\nOr Send the Database Channel Post link", 
                chat_id=message.from_user.id, 
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)), 
                timeout=60
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nIt's not from the Database Channel. Try again!", quote=True)
            continue

    while True:
        if cancel_status.get(user_id):
            await message.reply("🚫 Process canceled.")
            return
        try:
            second_message = await client.ask(
                text="Forward the Last Message from Database Channel..! (with Quotes)\nOr Send the Database Channel Post link", 
                chat_id=message.from_user.id, 
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)), 
                timeout=60
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nIt's not from the Database Channel. Try again!", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    user_id = message.from_user.id
    cancel_status[user_id] = False  # Initialize the cancel flag for this user

    while True:
        if cancel_status.get(user_id):
            await message.reply("🚫 Process canceled.")
            return
        try:
            channel_message = await client.ask(
                text="Forward Message from Database Channel (with Quotes)\nOr Send the Database Channel Post link", 
                chat_id=message.from_user.id, 
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)), 
                timeout=60
            )
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nIt's not from the Database Channel. Try again!", quote=True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('cancel'))
async def cancel_process(client: Client, message: Message):
    user_id = message.from_user.id
    cancel_status[user_id] = True  # Set the cancel flag to True for this user
    await message.reply("🚫 Process has been canceled.")