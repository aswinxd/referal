from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('referral.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS referrals
             (referrer text, referral text)''')

def start(update: Update, context: CallbackContext) -> None:
    referrer_id = update.message.from_user.id
    referral_id = context.args[0] if context.args else None

    if referral_id:
        # Save referral to database
        c.execute("INSERT INTO referrals VALUES (?, ?)", (referrer_id, referral_id))
        conn.commit()

    keyboard = [[InlineKeyboardButton("Share", switch_inline_query=f"referral {referrer_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Share this bot with your friends!', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    # Define your button logic here
    pass

def main() -> None:
    updater = Updater("bottoken", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))  # Make sure 'button' is defined before this line

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
