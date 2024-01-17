# bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

import sqlite3
from config import BOT_TOKEN

# Connect to SQLite database
conn = sqlite3.connect('referral.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS referrals
             (referrer_id INTEGER, referred_id INTEGER)''')

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    referrer_id = context.args[0] if context.args else None

    if referrer_id:
        # Save referral to database
        c.execute("INSERT INTO referrals VALUES (?, ?)", (referrer_id, user_id))
        conn.commit()

    referral_count = get_referral_count(user_id)

    keyboard = [[InlineKeyboardButton("Share", switch_inline_query=f"referral {user_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f"You have {referral_count} referrals. Share this bot with your friends!", reply_markup=reply_markup)

def get_referral_count(user_id):
    # Retrieve the number of referrals for a given user
    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (user_id,))
    return c.fetchone()[0]

def button(update: Update, context: CallbackContext) -> None:
    # Define your button logic here
    pass

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
