import praw
import telebot

from bot import Bot
from utils import load_config


def main():
    config = load_config()

    praw_instance = praw.Reddit(
        client_id=config.get("praw", "client_id"),
        client_secret=config.get("praw", "client_secret"),
        user_agent=config.get("praw", "user_agent"),
    )

    telegram_instance = telebot.TeleBot(token=config.get("telebot", "token"))

    bot = Bot(config=config, reddit=praw_instance, telegram=telegram_instance)

    while True:
        try:
            bot.start()
        except KeyboardInterrupt:
            print("[Exiting]")
            exit(0)


if __name__ == "__main__":
    main()
