import logging
from telegram.ext import Updater, CommandHandler
from

updater = Updater(token='719173106:AAGTVUeGmOBlmww0zsyeiR-Yd-HJAvtVebs')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def search(bot, update, args):

    bot.send_message(chat_id=update.message.chat_id, text="")
    pass


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling(timeout=123)
