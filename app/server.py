# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

import logging
from telegram.ext import Updater, CommandHandler
from functions import Functions
import telegram
from telegram.utils.request import Request
import time
import getopt
import re


request = Request(connect_timeout=1000, read_timeout=5000)

helps = {
    "search-by-actress":
        """
            Search by name of an actress
            
            Usage: /search name [-m|--many-actresses,[allow|deny/1/0]] [-u|--upto,[number]]
            
            Description
                -m,--many-actresses Whether a movie of many actresses allowed. "allow", "deny", "1" or "0". default=0
                -u,--upto	        Max number of the results. default=10
            
            for example:
                /search 桃乃木かな -m 1 -u 15
        """,
    "get-new":
        """
            Get newly released videos

            Usage: /new [-m|--many-actresses,[allow|deny/1/0]] [-u|--upto,[number]]

            Description
                -m,--many-actresses Whether a movie of many actresses allowed. "allow", "deny", "1" or "0". default=0
                -u,--upto	        Max number of the results. default=10

            for example:
                /new -m 1 -u 15
        """,
    "get-brief":
        """
            Get brief info of a video

            Usage: /brief code [-l|--lang,[en/jp/zh]]
            
            Description
                -l,--lang specify language type of the result. default=en

            for example:
                /brief ABP-123 -l en
        """,
}


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def search(bot, update, args):
    """
    search command like this:
        1. /search ABP-123
        2. /search 桃乃木かな
            -m, --many-actresses [allow|deny/1/0]  default=0
            -u, --upto           [20]              default=10
    :param bot:
    :param update:
    :param args:
    :return:
    """

    start_time = time.clock()

    first = args[0]
    if re.search("\d", first):
        # /search ABP-123
        if len(args) != 1:
            bot.send_message(chat_id=update.message.chat_id, text="Sorry, Wrong Usage")
            return

        res = Functions.search_by_code(first)

        if res is None:
            bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
            return

        reply_markup = telegram.InlineKeyboardMarkup([[
            telegram.InlineKeyboardButton(res.code, url=res.video_url)
        ]])
        bot.send_photo(chat_id=update.message.chat_id, photo=res.preview_img_url, reply_markup=reply_markup)
        # bot.send_video_note(chat_id=update.message.chat_id, video_note=res)
        # bot.send_video(chat_id=update.message.chat_id, video=res, request=request, supports_streaming=True, timeout=5000)
        # bot.send_message(chat_id=update.message.chat_id, text="<video><source src=\"" + res +  "\" type=\"video/mp4\"></video>", parse_mode="HTML")

    else:
        # /search 桃乃木かな [-m/--many-actresses] [on/off] [-u/--upto] [20]
        try:
            actress = first
            options, remainder = getopt.getopt([x.replace(u"—", u"--") for x in args[1:]], 'm:u:', ['many-actress=', 'upto='])

            allow_many_actresses = False
            up_to = 10

            for o, a in options:
                if o in ("-m","--many-actresses") and a in ("allow", "deny", "1", "0"):
                    if a in ("allow", "1"):
                        allow_many_actresses = True
                    continue
                if o in ("-u", "--upto"):
                    try:
                        up_to = int(a)
                        continue
                    except ValueError:
                        bot.send_message(chat_id=update.message.chat_id, text=helps["search-by-actress"])
                        return
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=helps["search-by-actress"])
                    return

            briefs = Functions.search_by_actress(actress, allow_many_actresses, up_to)

            if not briefs:
                bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Actress Found")

            for brief in briefs:
                if brief.preview_img_url:
                    bot.send_photo(chat_id=update.message.chat_id, photo=brief.preview_img_url, caption=brief.code + "\n" + brief.title)
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=brief.code + "\n" + brief.title)

        except getopt.GetoptError:
            bot.send_message(chat_id=update.message.chat_id, text=helps["search-by-actress"])
            return


def get_new(bot, update, args):
    try:
        options, remainder = getopt.getopt([x.replace(u"—", u"--") for x in args], 'm:u:',
                                           ['many-actress=', 'upto='])

        allow_many_actresses = False
        up_to = 10

        for o, a in options:
            if o in ("-m", "--many-actresses") and a in ("allow", "deny", "1", "0"):
                if a in ("allow", "1"):
                    allow_many_actresses = True
                continue
            if o in ("-u", "--upto"):
                try:
                    up_to = int(a)
                    continue
                except ValueError:
                    bot.send_message(chat_id=update.message.chat_id, text=helps["get-new"])
                    return
            else:
                bot.send_message(chat_id=update.message.chat_id, text=helps["get-new"])
                return

        briefs = Functions.get_newly_released(allow_many_actresses, up_to)

        if not briefs:
            bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")

        for brief in briefs:
            if brief.preview_img_url:
                bot.send_photo(chat_id=update.message.chat_id, photo=brief.preview_img_url,
                               caption=brief.code + "\n" + brief.release_date.strftime("%Y-%m-%d") + "\n" + brief.title)
            else:
                bot.send_message(chat_id=update.message.chat_id, text=brief.code + "\n" + brief.title)

    except getopt.GetoptError:
        bot.send_message(chat_id=update.message.chat_id, text=helps["get-new"])
        return


def get_brief(bot, update, args):
    if len(args) != 1 and len(args) != 3:
        bot.send_message(chat_id=update.message.chat_id, text=helps["get-brief"])
        return

    if len(args) == 3:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, temporarily only English is supported")

    code = args[0]
    res = Functions.get_brief(code)

    if not res:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
        return

    if res.preview_img_url:
        bot.send_photo(
            chat_id=update.message.chat_id, photo=res.preview_img_url,
            caption=res.code + (
                ("\n" + res.release_date.strftime("%Y-%m-%d")) if res.release_date else ""
            ) + "\n" + res.title)

    else:
        bot.send_message(
            chat_id=update.message.chat_id, text=res.code + (
                ("\n" + res.release_date.strftime("%Y-%m-%d")) if res.release_date else ""
            ) + "\n" + res.title
        )


def run():
    updater = Updater(token=open("token.txt").read())
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    handlers = [
        CommandHandler('start', start),
        CommandHandler('search', search, pass_args=True),
        CommandHandler('new', get_new, pass_args=True),
        CommandHandler('brief', get_brief, pass_args=True)
    ]

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling(timeout=123)
