import telebot
from telebot import types

TOKEN = '6520550784:AAEUC8Itct_VMe4cbJbUXVZxE-rw8PM0REQ'
bot = telebot.TeleBot(TOKEN)

referral_points = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    referral_link = f"https://t.me/{bot.get_me().username}?start={message.chat.id}"
    referral_button = types.InlineKeyboardButton(text='Click here to join', url=referral_link)
    markup.add(referral_button)
    bot.send_message(message.chat.id, "Welcome to the referral bot!", reply_markup=markup)

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
    if message.text.startswith('/start'):
        referred_by = message.text.split(' ')[1]
        referral_points.setdefault(referred_by, 0)
        referral_points[referred_by] += 1
        bot.send_message(referred_by, f"You have been referred by {message.chat.id} and earned 1 point!")

bot.polling()
