# bot.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import base64
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, ADMINS

app = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def generate_referral_code(user_id: int) -> str:
    # Replace this with your logic to generate a unique referral code for the user
    return f"REF{user_id}"


async def save_referral(user_id: int, referred_by: int):
    # Replace this with your logic to save referral information in your database
    pass


@app.on_message(filters.private & filters.command("genlink"))
async def genlink_command_handler(_, message: Message):
    user_id = message.from_user.id
    referral_code = await generate_referral_code(user_id)

    link = f"https://t.me/{(await app.get_me()).username}?start={referral_code}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Get Referral Link", url=link)]])
    await message.reply_text(f"Your referral link is: {link}", reply_markup=reply_markup)


@app.on_message(filters.private & filters.command("start"))
async def start_command_handler(_, message: Message):
    # Check if the user started the bot using a referral link
    if len(message.command) > 1 and message.command[1].startswith("REF"):
        referred_by = int(message.command[1][3:])
        user_id = message.from_user.id

        # Save referral information
        await save_referral(user_id, referred_by)

        # Get videos from the DB channel and send them to the referral owner
        async for msg in app.get_chat_history(chat_id=DB_CHANNEL_ID, limit=5):
            if msg.video:
                await app.copy_message(chat_id=referred_by, from_chat_id=DB_CHANNEL_ID, message_id=msg.message_id)

    await message.reply_text("Welcome to the bot!")


if __name__ == "__main__":
    app.run()
