#(©)Codeflix-Bots

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user = query.from_user  # Get the user who initiated the interaction
    
    if data == "about":
        await query.message.edit_text(
            text = (
                f"<b>○ Creator : Bot Father\n"
                f"○ My best Friend : <a href='tg://user?id={user.id}'>{user.first_name}</a>\n</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Close", callback_data="close"),
                        InlineKeyboardButton('Main Channel', url='https://t.me/OtakuFlix_Network/4639')
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass