# bot.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, ADMINS

app = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def generate_referral_code(user_id: int) -> str:
    # Replace this with your logic to generate a unique referral code for the user
    return f"REF{user_id}"


async def save_referral(user_id: int, referred_by: int):
    # Replace this with your logic to save referral information in your database
    pass


async def get_referred_users():
    # Replace this with your logic to retrieve the list of users who joined using a referral link from your database
    return []


async def send_messages_to_user(user_id: int, messages: list):
    for message in messages:
        await app.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)


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

    await message.reply_text("Welcome to the bot!")


@app.on_message(filters.private & filters.user(ADMINS) & filters.command("send"))
async def send_command_handler(_, message: Message):
    # Get the message text after "/send"
    text = message.text.split("/send", 1)[1].strip()

    # Get the referred user IDs from your database
    referred_users = await get_referred_users()  # Add 'await' here

    for user_id in referred_users:
        await send_messages_to_user(user_id, [message])


if __name__ == "__main__":
    app.run()
