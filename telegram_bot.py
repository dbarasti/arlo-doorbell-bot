from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from logger import logging

import io
import arlo
import os


def start(update: Update, context: CallbackContext):
    if update.effective_chat.id == int(os.environ.get('MY_CHAT_ID')):
        if not arlo.is_running():
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Activating Arlo Doorbell system")
            arlo.launch()


def stop(update: Update, context: CallbackContext):
    if update.effective_chat.id == int(os.environ.get('MY_CHAT_ID')):
        if arlo.is_running():
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Shutting down Arlo Doorbell system")
            arlo.shutdown()


def trigger_snapshot(update: Update, context: CallbackContext):
    if update.effective_chat.id == int(os.environ.get('MY_CHAT_ID')):
        if arlo.is_running():
            snapshot = arlo.get_snapshot_file()
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=arlo.snapshot_source())
            context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=io.BytesIO(snapshot))


def launch():
    updater = Updater(token=os.environ.get('BOT_SECRET'), use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)
    trigger_snapshot_handler = CommandHandler('trigger', trigger_snapshot)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(trigger_snapshot_handler)

    updater.start_polling()
