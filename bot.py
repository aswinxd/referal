# your_script.py

import time
import json
import telebot
from config import config

# Accessing the variables
BOT_TOKEN = config.BOT_TOKEN
PAYMENT_CHANNEL = config.PAYMENT_CHANNEL
OWNER_ID = config.OWNER_ID
CHANNELS = config.CHANNELS
Daily_bonus = config.DAILY_BONUS
Mini_Withdraw = config.MINI_WITHDRAW
Per_Refer = config.PER_REFER

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊 Statistics', '📢 Broadcast')  # Added 'Broadcast' option
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            # ... (rest of your existing /start logic)
        else:
            # ... (rest of your existing /start logic)
    except:
        handle_error(message)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            # ... (rest of your existing /check logic)
        else:
            # ... (rest of your existing /check logic)
    except:
        handle_error(call.message)

@bot.message_handler(content_types=['text', 'document'])  # Added 'document' content type
def send_text(message):
    try:
        if message.text == '🆔 Account':
            # ... (rest of your existing /account logic)
        elif message.text == '📢 Broadcast':  # Added 'Broadcast' option
            broadcast(message)
        else:
            # ... (rest of your existing logic)
    except:
        handle_error(message)

def broadcast(message):
    try:
        if message.chat.id == OWNER_ID:
            bot.send_message(message.chat.id, "Send me the media file you want to broadcast.")
            bot.register_next_step_handler(message, handle_broadcast)
        else:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")
    except:
        handle_error(message)

def handle_broadcast(message):
    try:
        if message.chat.id == OWNER_ID:
            data = json.load(open('users.json', 'r'))
            users = [int(user) for user in data['id'].keys()]

            for user_id in users:
                try:
                    bot.send_chat_action(user_id, 'upload_document')
                    bot.send_document(user_id, message.document.file_id)
                except Exception as e:
                    print(f"Error broadcasting to user {user_id}: {str(e)}")

            bot.send_message(OWNER_ID, "Broadcast completed successfully.")
        else:
            bot.send_message(message.chat.id, "You are not authorized to use this command.")
    except:
        handle_error(message)

# ... (rest of your existing functions)

def handle_error(message, exception=None):
    bot.send_message(OWNER_ID, f"Error occurred in the bot:\n\n{str(exception)}")
    bot.send_message(message.chat.id, "An error occurred. The administrator has been notified.")
    print(f"Error occurred: {str(exception)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
