# bot.py
import telebot
from telebot import types
from config import TOKEN, CHANNEL_USERNAME

bot = telebot.TeleBot(TOKEN)

referral_points = {}
referral_forwardings = {}

async def forward_messages(from_chat_id, to_chat_id, message_id):
    try:
        await bot.forward_message(chat_id=to_chat_id, from_chat_id=from_chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error forwarding message: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup()

    # Construct referral link
    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"

    referral_button = types.InlineKeyboardButton(text='Click here to join', url=referral_link)
    markup.add(referral_button)

    bot.send_message(user_id, "Welcome to the referral bot!", reply_markup=markup)

@bot.message_handler(commands=['points'])
def points(message):
    user_id = message.chat.id
    if user_id in referral_points:
        points = referral_points[user_id]
        bot.send_message(user_id, f"You have {points} points.")
    else:
        bot.send_message(user_id, "You don't have any points yet.")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.chat.id
    if user_id in referral_points:
        referral_points.pop(user_id)
        bot.send_message(user_id, "Your points have been reset.")
    else:
        bot.send_message(user_id, "You don't have any points to reset.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Commands:\n"
                                      "/start - Get your referral link\n"
                                      "/points - Check your points\n"
                                      "/reset - Reset your points")

@bot.message_handler(func=lambda message: True)
def handle_referral(message):
    user_id = message.chat.id
    if message.text.startswith('/start'):
        referred_by = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

        if referred_by:
            referral_points.setdefault(referred_by, 0)
            referral_points[referred_by] += 1
            bot.send_message(referred_by, f"You have been referred by {user_id} and earned 1 point!")

            # Forward videos from the channel to the user who used the referral link
            forward_videos(referred_by)

            # Forward the last message from the channel to the user who used the referral link
            forward_last_message_from_channel(referred_by)

def forward_videos(referrer_id):
    try:
        # Assuming you have a variable 'CHANNEL_USERNAME' defined
        messages = bot.get_chat_history(CHANNEL_USERNAME, limit=5)
        for message in messages:
            if message.video:
                # Forward the last video message to the user
                forward_messages(CHANNEL_USERNAME, referrer_id, message.message_id)
    except Exception as e:
        print(f"Error forwarding videos: {e}")

def forward_last_message_from_channel(user_id):
    try:
        # Assuming you have a variable 'CHANNEL_USERNAME' defined
        messages = bot.get_chat_history(CHANNEL_USERNAME, limit=1)
        for message in messages:
            # Forward the last message to the user
            forward_messages(CHANNEL_USERNAME, user_id, message.message_id)
    except Exception as e:
        print(f"Error forwarding last message: {e}")

# Incorporate link generator and batch functions
@bot.message_handler(commands=['batch'])
def batch(message):
    # Add batch functionality logic here
    pass

@bot.message_handler(commands=['genlink'])
def link_generator(message):
    # Add link generator functionality logic here
    pass

bot.polling()
