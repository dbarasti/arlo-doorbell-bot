
import os
import telegram


def setup():
    BOT_SECRET = os.environ.get('BOT_SECRET')
    bot = telegram.Bot(token=BOT_SECRET)
    bot.get_me()
    return bot


def send_message(message):
    global bot
    bot.send_message(text=message, chat_id=os.environ.get('MY_CHAT_ID'))


def send_photo(photo):
    global bot
    bot.send_photo(photo=photo, chat_id=os.environ.get('MY_CHAT_ID'))


bot = setup()
