import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from JavPy.functions import Functions
import getopt
import re
from JavPy.app.tgbot.reply import send_brief, Interactive, send_av, send_magnet
import urllib3
from JavPy.utils.chat_history import start_clear_died_session

start_clear_died_session()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


helps = {
    "search-by-actress": """
            Search by name of an actress
            
            Usage: /search name [-m|--many-actresses,[on|off/1/0]] [-u|--upto,[number]]
            
            Description
                -m,--many-actresses Whether a movie of many actresses allowed. "on", "off", "1" or "0". default=0
                -u,--upto	        Max number of the results. default=10
            
            for example:
                /search 桃乃木かな -m 1 -u 15
        """,
    "get-new": """
            Get newly released videos

            Usage: /new [-m|--many-actresses,[on|off/1/0]] [-u|--upto,[number]]

            Description
                -m,--many-actresses Whether a movie of many actresses allowed. "on", "off", "1" or "0". default=0
                -u,--upto	        Max number of the results. default=10

            for example:
                /new -m 1 -u 15
        """,
    "get-brief": """
            Get brief info of a video

            Usage: /brief code [-l|--lang,[en/jp/zh]]

            Description
                -l,--lang specify language type of the result. default=en

            for example:
                /brief ABP-123 -l en
        """,
}


def start(bot, update):
    Interactive.start(bot, update)


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
    first = args[0]
    if re.search("\\d", first):
        # /search ABP-123
        if len(args) != 1:
            bot.send_message(chat_id=update.message.chat_id, text="Sorry, Wrong Usage")
            return

        res = Functions.search_by_code(first)
        send_av(bot, update, res)

    else:
        # /search 桃乃木かな [-m/--many-actresses] [on/off] [-u/--upto] [20]
        try:
            actress = first
            options, _ = getopt.getopt(
                [x.replace("—", "--") for x in args[1:]],
                "m:u:",
                ["many-actress=", "upto="],
            )

            allow_many_actresses = False
            up_to = 10

            for o, a in options:
                if o in ("-m", "--many-actresses") and a in ("on", "off", "1", "0"):
                    if a in ("on", "1"):
                        allow_many_actresses = True
                    continue
                elif o in ("-u", "--upto"):
                    try:
                        up_to = int(a)
                        continue
                    except ValueError:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text=helps["search-by-actress"],
                        )
                        return

            briefs, _ = Functions.search_by_actress(actress, up_to)
            if not allow_many_actresses:
                briefs = list(filter(lambda x: "," not in x.actress, briefs))
            send_brief(bot, update, briefs)

        except getopt.GetoptError:
            bot.send_message(
                chat_id=update.message.chat_id, text=helps["search-by-actress"]
            )
            return


def get_new(bot, update, args):
    try:
        options, _ = getopt.getopt(
            [x.replace("—", "--") for x in args], "m:u:", ["many-actress=", "upto="]
        )

        allow_many_actresses = False
        up_to = 10

        for o, a in options:
            if o in ("-m", "--many-actresses") and a in ("on", "off", "1", "0"):
                if a in ("on", "1"):
                    allow_many_actresses = True
                continue
            elif o in ("-u", "--upto"):
                try:
                    up_to = int(a)
                    continue
                except ValueError:
                    bot.send_message(
                        chat_id=update.message.chat_id, text=helps["get-new"]
                    )
                    return

        briefs = Functions.get_newly_released(allow_many_actresses, up_to)
        send_brief(bot, update, briefs)

    except getopt.GetoptError:
        bot.send_message(chat_id=update.message.chat_id, text=helps["get-new"])
        return


def get_brief(bot, update, args):
    if len(args) != 1 and len(args) != 3:
        bot.send_message(chat_id=update.message.chat_id, text=helps["get-brief"])
        return

    if len(args) == 3:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Sorry, temporarily only English is supported",
        )

    code = args[0]
    res = Functions.get_brief(code)

    if not res:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
        return

    send_brief(bot, update, res)


def get_magnet(bot, update, args):
    send_magnet(bot, update, Functions.get_magnet(args[0]))


# def callback(bot, update):
#     print(update.message.chat_id, update.callback_query.data)


def run(token):
    updater = Updater(token)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    handlers = [
        CommandHandler("start", start),
        CommandHandler("search", search, pass_args=True),
        CommandHandler("new", get_new, pass_args=True),
        CommandHandler("brief", get_brief, pass_args=True),
        CommandHandler("magnet", get_magnet, pass_args=True),
        MessageHandler(filters.Filters.text, Interactive.message),
        # CallbackQueryHandler(callback),
        # InlineQueryHandler(inline_query)
    ]

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling(timeout=123)
    updater.idle()
