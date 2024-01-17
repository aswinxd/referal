# your_script.py

import json
import telebot
from config import Config
import time
from telebot import types

# Accessing the variables
config = Config()
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
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊Statistics')
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
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markups = types.InlineKeyboardMarkup()
            markups.add(types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except Exception as e:
        bot.send_message(message.chat.id, f"This command has an error. Please wait for fixing the glitch by admin. Error: {e}")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\n Error on command: {message.text}")
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(callback_query_id=call.id, text='✅ You joined Now you can earn money')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True
                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1
                        bot.send_message(ref_id, f"*🏧 New Referral on Level 1, You Got : +{Per_Refer} {BOT_TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='❌ You not Joined')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"This command has an error. Please wait for fixing the glitch by admin. Error: {e}")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\n Error on command: {call.data}")
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('users.json', 'w'))
            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name, wallet, balance, BOT_TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        # ... (rest of your message handling)
    except Exception as e:
        bot.send_message(message.chat.id, f"This command has an error. Please wait for fixing the glitch by admin. Error: {e}")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\n Error on command: {message.text}")
        return

def trx_address(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if len(message.text) == 34:
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))
            data['wallet'][user] = message.text
            bot.send_message(message.chat.id, "*💹Your Trx wallet set to " +
                             data['wallet'][user]+"*", parse_mode="Markdown")
            json.dump(data, open('users.json', 'w'))
            return menu(message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "*⚠️ It's Not a Valid Trx Address!*", parse_mode="Markdown")
            return menu(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"This command has an error. Please wait for fixing the glitch by admin. Error: {e}")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\n Error on command: {message.text}")
        return

def amo_with(message):
    try:
        user_id = message.chat.id
        amo = message.text
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        json.dump(data, open('users.json', 'w'))
        bal = data['balance'][user]
        wall = data['wallet'][user]
        msg = message.text
        if msg.isdigit() == False:
            bot.send_message(
                user_id, "_📛 Invalid value. Enter only numeric value. Try again_", parse_mode="Markdown")
            return
        if int(message.text) < Mini_Withdraw:
            bot.send_message(
                user_id, f"_❌ Minimum withdraw {Mini_Withdraw} {BOT_TOKEN}_", parse_mode="Markdown")
            return
        if int(message.text) > bal:
            bot.send_message(
                user_id, "_❌ You Can't withdraw More than Your Balance_", parse_mode="Markdown")
            return
        amo = int(amo)
        data['balance'][user] -= int(amo)
        data['totalwith'] += int(amo)
        bot_name = bot.get_me().username
        json.dump(data, open('users.json', 'w'))
        bot.send_message(user_id, "✅* Withdraw is requested to our owner automatically\n\n💹 Payment Channel :- "+PAYMENT_CHANNEL +"*", parse_mode="Markdown")
        markupp = types.InlineKeyboardMarkup()
        markupp.add(types.InlineKeyboardButton(text='🍀 BOT LINK', url=f'https://telegram.me/{bot_name}?start={OWNER_ID}'))
        send = bot.send_message(PAYMENT_CHANNEL,  "✅* New Withdraw\n\n⭐ Amount - "+str(amo)+f" {BOT_TOKEN}\n🦁 User - @"+message.from_user.username+"\n💠 Wallet* - `"+data['wallet'][user]+"`\n☎️ *User Referrals = "+str(
            data['referred'][user])+"\n\n🏖 Bot Link - @"+bot_name+"\n⏩ Please wait our owner will confirm it*", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markupp)
    except Exception as e:
        bot.send_message(message.chat.id, f"This command has an error. Please wait for fixing the glitch by admin. Error: {e}")
        bot.send_message(OWNER_ID, f"Your bot got an error. Fix it fast!\n Error on command: {message.text}")
        return

if __name__ == '__main__':
    bot.polling(none_stop=True)
