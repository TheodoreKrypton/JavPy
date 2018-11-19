# encoding: utf-8

import telegram
from uuid import uuid4
from functions import Functions
import re
from utils import history


def _send_brief(bot, update, brief):
    if brief.preview_img_url:
        bot.send_photo(
            chat_id=update.message.chat_id, photo=brief.preview_img_url,
            caption=brief.code + (
                ("\n" + brief.release_date.strftime("%Y-%m-%d")) if brief.release_date else ""
            ) + "\n" + brief.title)

    else:
        bot.send_message(
            chat_id=update.message.chat_id, text=brief.code + (
                ("\n" + brief.release_date.strftime("%Y-%m-%d")) if brief.release_date else ""
            ) + "\n" + brief.title
        )


def send_brief(bot, update, brief):
    if not brief:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
        return

    if hasattr(brief, '__iter__'):
        for b in brief:
            _send_brief(bot, update, b)

    else:
        _send_brief(bot, update, brief)


def send_av(bot, update, av):
    if av is None:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
        return

    reply_markup = telegram.InlineKeyboardMarkup([[
        telegram.InlineKeyboardButton(av.code, url=av.video_url)
    ]])
    bot.send_photo(chat_id=update.message.chat_id, photo=av.preview_img_url, reply_markup=reply_markup)


def inline_query(bot, update):
    query = update.inline_query.query

    key_word = query.split()[0]

    if not re.search("\d", key_word):
        briefs = Functions.search_by_actress(key_word, allow_many_actresses=False, up_to=20)

    else:
        briefs = [Functions.get_brief(key_word)]

    if not briefs:
        return

    results = [
        telegram.InlineQueryResultPhoto(
            uuid4(), brief.preview_img_url, brief.preview_img_url,
            caption="\n".join(filter(lambda x: x, (brief.code, brief.title, brief.actress)))
        ) for brief in briefs
    ]

    update.inline_query.answer(results)


class Interactive:
    __init__ = None

    @staticmethod
    @history.update_history
    def start(bot, update):
        # reply_markup = telegram.InlineKeyboardMarkup([[
        #     telegram.InlineKeyboardButton("Search", callback_data='{"jump_to": "search"}')
        # ]])
        reply_markup = telegram.ReplyKeyboardMarkup([
            ["Search", "New", "Random"],
            ["Brief", "Magnet"]
        ], resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text="Hi, what can I help you?", reply_markup=reply_markup)

    @staticmethod
    @history.update_history
    def search(bot, update):
        reply_markup = telegram.ReplyKeyboardRemove(selective=True)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな",
            reply_markup=reply_markup,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    @history.update_history
    def new(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな")

    @staticmethod
    @history.update_history
    def random(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな")

    @staticmethod
    @history.update_history
    def brief(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな")

    @staticmethod
    @history.update_history
    def magnet(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな")

    @classmethod
    def message(cls, bot, update):
        if update.message.text == "Search":
            cls.search(bot, update)
        elif update.message.text == "New":
            cls.new(bot, update)
        elif update.message.text == "Random":
            cls.random(bot, update),
        elif update.message.text == "Brief":
            cls.brief(bot, update)
        elif update.message.text == "Magnet":
            cls.magnet(bot, update)

        else:
            last_cmd = history.history[update.message.from_user.id][0][-1]

            if last_cmd == "Search":
                res = Functions.search_by_code(update.message.text)
                send_av(bot, update, res)

        return