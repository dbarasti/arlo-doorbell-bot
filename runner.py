from dotenv import load_dotenv
import arlo
import telegram_bot

load_dotenv()


def main():
    try:
        telegram_bot.launch()
    except:
        arlo.shutdown()


if __name__ == "__main__":
    main()
