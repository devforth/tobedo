

import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import json
import hashlib
import os
import sqlite3
import asyncio

DB_NAME = 'tobedo.sqlite3'

def gen_db():
    # table: Replies
    # message_and_chat_id, reply_id, created_at
    # unique index on message_id
    with sqlite3.connect(DB_NAME) as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS Replies (
                message_and_chat_id VARCHAR(255) NOT NULL,
                reply_id VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (message_and_chat_id)
            )
        ''')

        db.commit()

def get_reply_by_message_id(message_id, chat_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.execute('''
            SELECT reply_id FROM Replies WHERE message_and_chat_id = ?
        ''', (f"{chat_id}_{message_id}",))

        row = cursor.fetchone()
        if row:
            return row[0]
        return None

def insert_reply(message_id, reply_id, chat_id):
    with sqlite3.connect(DB_NAME) as db:
        db.execute('''
            INSERT INTO Replies (message_and_chat_id, reply_id) VALUES (?, ?)
        ''', (f"{chat_id}_{message_id}", reply_id))

        db.commit()



logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TG_TOKEN')
if not TOKEN:
    print('TG_TOKEN not specified in env, please set TG_TOKEN with your bot token generated by @BotFather')
    exit(1)

def button_click(update, context):
    query = update.callback_query

    if query.data.startswith('toggle__'):
        hash = query.data.replace('toggle__', '')

        for i, btn in enumerate(query.message.reply_markup.inline_keyboard):
            checked = btn[0].text.startswith('☑️')
            btn_text = btn[0].text.replace('🟨 ', '').replace('☑️ ', '')
            if md5hash(
                f'{btn_text}_{i}'
            ) == hash:
                print('found a btn', btn_text)
                new_text = f'☑️ {btn_text}' if not checked else f'🟨 {btn_text}'
                btn[0].text = new_text
                break

        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=f'Click to toggle',
            reply_markup=query.message.reply_markup
        )
       


def md5hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()



def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """

    print('upd 🟨', update)
    
    msg = None
    update_object = None

    if update.channel_post:
        msg = update.channel_post.text
        update_object = update.channel_post
    elif update.message:
        msg = update.message.text
        update_object = update.message
    elif update.edited_message:
        msg = update.edited_message.text
        update_object = update.edited_message

    elif update.edited_channel_post:
        msg = update.edited_channel_post.text
        update_object = update.edited_channel_post

    if not msg:
        print('Unrecognized update')
        return
    
    print('msg', msg)
    # Print to console

    lines = msg.split('\n')
    keyboard = []

    index = 0
    for line in lines:
        if line.strip() == '':
            continue
        keyboard.append([InlineKeyboardButton(
            f"🟨 {line}", 
            callback_data=f"toggle__{md5hash(f'{line}_{index}')}"
        )])
        index += 1


    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.channel_post or update.message:
        reply = update_object.reply_text('Click to toggle', reply_markup=reply_markup)
        reply_id = reply.message_id
        message_id = update_object.message_id
        chat_id = update_object.chat_id
        insert_reply(message_id, reply_id, chat_id)

    else:
        # find previous reply to same message and edit it
        # this is a workaround for editing messages in channels
        #
        print('context', context)
        message_id = update_object.message_id
        reply_id = get_reply_by_message_id(message_id, update_object.chat_id)
        context.bot.edit_message_reply_markup(
            chat_id=update_object.chat_id,
            message_id=reply_id,
            reply_markup=reply_markup
        )
        



def main() -> None:
    gen_db()
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(button_click))


    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
