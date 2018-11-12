import logging
from telegram.ext import Updater, CommandHandler
from functions import Functions
import telegram
from telegram.utils.request import Request
import time


request = Request(connect_timeout=1000, read_timeout=5000)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def search(bot, update, args):
    """
    search command like this:
        1. /search ABP-123
    :param bot:
    :param update:
    :param args:
    :return:
    """
    res = "Sorry, Wrong Usage"

    start_time = time.clock()

    if len(args) == 1:
        res = Functions.search(args[0])

    reply_markup = telegram.InlineKeyboardMarkup([[
        telegram.InlineKeyboardButton(res.code, url=res.video_url)
    ]])
    # bot.send_video_note(chat_id=update.message.chat_id, video_note=res)
    bot.send_photo(chat_id=update.message.chat_id, photo=res.preview_img_url, reply_markup=reply_markup)
    # bot.send_video(chat_id=update.message.chat_id, video=res, request=request, supports_streaming=True, timeout=5000)
    # bot.send_message(chat_id=update.message.chat_id, text="<video><source src=\"" + res +  "\" type=\"video/mp4\"></video>", parse_mode="HTML")

def run():
    updater = Updater(token=open("token.txt").read())
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


    handlers = [
        CommandHandler('start', start),
        CommandHandler('search', search, pass_args=True)
    ]

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling(timeout=123)
