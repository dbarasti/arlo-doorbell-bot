from dotenv import load_dotenv
import arlo
import telegram_bot

from time import sleep

load_dotenv()

try:
    telegram_bot.launch()
except:
    arlo.shutdown()
