# bot.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, TOKEN, CHANNEL_USERNAME

bot = Client(
    "referral_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)

referral_points = {}

async def forward_messages(from_chat_id, to_chat_id, message_id):
    try:
        await bot.forward_messages(chat_id=to_chat_id, from_chat_id=from_chat_id, message_ids=message_id)
    except Exception as e:
        print(f"Error forwarding message: {e}")

@bot.on_message(filters.command('start'))
async def start(client, message):
    user_id = message.chat.id
    markup = InlineKeyboardMarkup()

    # Construct referral link
    referral_link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"

    referral_button = InlineKeyboardButton(text='Click here to join', url=referral_link)
    markup.add(referral_button)

    await message.reply_text("Welcome to the referral bot!", reply_markup=markup)

@bot.on_message(filters.command('points'))
async def points(client, message):
    user_id = message.chat.id
    if user_id in referral_points:
        await message.reply_text(f"You have {referral_points[user_id]} points.")
    else:
        await message.reply_text("You don't have any points yet.")

@bot.on_message(filters.command('reset'))
async def reset(client, message):
    user_id = message.chat.id
    if user_id in referral_points:
        referral_points.pop(user_id)
        await message.reply_text("Your points have been reset.")
    else:
        await message.reply_text("You don't have any points to reset.")

@bot.on_message(filters.command('help'))
async def help(client, message):
    await message.reply_text("Commands:\n"
                       "/start - Get your referral link\n"
                       "/points - Check your points\n"
                       "/reset - Reset your points")

@bot.on_message(filters.text & ~filters.command & ~filters.forwarded & ~filters.edited)
async def handle_referral(client, message):
    user_id = message.chat.id
    if message.text.startswith('/start'):
        referred_by = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

        if referred_by:
            referral_points.setdefault(referred_by, 0)
            referral_points[referred_by] += 1
            await bot.send_message(referred_by, f"You have been referred by {user_id} and earned 1 point!")

            # Forward videos from the channel to the user who used the referral link
            await forward_videos(referred_by)

            # Forward the last message from the channel to the user who used the referral link
            await forward_last_message_from_channel(referred_by)

async def forward_videos(referrer_id):
    try:
        # Assuming you have a variable 'CHANNEL_USERNAME' defined
        messages = await bot.get_chat_history(CHANNEL_USERNAME, limit=5)
        for message in messages:
            if message.video:
                # Forward the last video message to the user
                await forward_messages(CHANNEL_USERNAME, referrer_id, message.message_id)
    except Exception as e:
        print(f"Error forwarding videos: {e}")

async def forward_last_message_from_channel(user_id):
    try:
        # Assuming you have a variable 'CHANNEL_USERNAME' defined
        messages = await bot.get_chat_history(CHANNEL_USERNAME, limit=1)
        for message in messages:
            # Forward the last message to the user
            await forward_messages(CHANNEL_USERNAME, user_id, message.message_id)
    except Exception as e:
        print(f"Error forwarding last message: {e}")

# Incorporate link generator and batch functions
@bot.on_message(filters.command('batch'))
async def batch(client, message):
    user_id = message.chat.id

    # Check if the user is an admin (or add your own admin check logic)
    if user_id in [123456789, 987654321]:
        try:
            # Get the first and last messages from the DB Channel
            first_message = await bot.ask_text(
                text="Forward the First Message from DB Channel (with Quotes) or Send the DB Channel Post Link",
                chat_id=user_id,
                filters=filters.forwarded | filters.text,
                timeout=60
            )
            second_message = await bot.ask_text(
                text="Forward the Last Message from DB Channel (with Quotes) or Send the DB Channel Post Link",
                chat_id=user_id,
                filters=filters.forwarded | filters.text,
                timeout=60
            )

            # Extract message IDs
            f_msg_id = first_message.message_id
            s_msg_id = second_message.message_id

            # Generate a unique string based on message IDs
            batch_key = f"batch-{f_msg_id}-{s_msg_id}"

            # Perform batch processing using the batch_key
            # (Add your logic for batch processing here)

            await message.reply_text(f"Batch processing initiated with key: {batch_key}")
        except TimeoutError:
            await message.reply_text("Batch processing canceled due to timeout.")
    else:
        await message.reply_text("You are not authorized to use this command.")

@bot.on_message(filters.command('genlink'))
async def link_generator(client, message):
    user_id = message.chat.id

    try:
        # Get the message from the DB Channel
        channel_message = await bot.ask_text(
            text="Forward Message from the DB Channel (with Quotes) or Send the DB Channel Post Link",
            chat_id=user_id,
            filters=filters.forwarded | filters.text,
            timeout=60
        )

        # Extract message ID
        msg_id = channel_message.message_id

        # Generate a unique string based on message ID
        link_key = f"get-{msg_id}"

        # Perform link generation using the link_key
        # (Add your logic for link generation here)

        # Construct the referral link
        base64_string = await encode(link_key)
        referral_link = f"https://t.me/{(await bot.get_me()).username}?start={base64_string}"

        await message.reply_text(f"Here is your referral link:\n{referral_link}")
    except TimeoutError:
        await message.reply_text("Link generation canceled due to timeout.")

if __name__ == "__main__":
    bot.run()
