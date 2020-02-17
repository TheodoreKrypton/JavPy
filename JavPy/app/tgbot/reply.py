import telegram
from uuid import uuid4
from JavPy.functions import Functions
import re
from JavPy.utils import chat_history


def _send_brief(bot, update, brief):
    if brief.preview_img_url:
        bot.send_photo(
            chat_id=update.message.chat_id,
            photo=brief.preview_img_url,
            caption=brief.code
            + (
                ("\n" + brief.release_date.strftime("%Y-%m-%d"))
                if brief.release_date
                else ""
            )
            + "\n"
            + brief.title,
        )

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=brief.code
            + (
                ("\n" + brief.release_date.strftime("%Y-%m-%d"))
                if brief.release_date
                else ""
            )
            + "\n"
            + brief.title,
        )


def send_brief(bot, update, brief):
    if not brief:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
        return

    if hasattr(brief, "__iter__"):
        for b in brief:
            _send_brief(bot, update, b)

    else:
        _send_brief(bot, update, brief)


def send_av(bot, update, av):
    if av is None:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Video Found")
        return

    reply_markup = telegram.InlineKeyboardMarkup(
        [[telegram.InlineKeyboardButton(av.code, url=av.video_url)]]
    )
    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=av.preview_img_url,
        reply_markup=reply_markup,
    )


def send_magnet(bot, update, magnets):
    if magnets is None:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, No Magnet Found")
        return

    for magnet in magnets:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="[" + magnet.description + "]\n" + magnet.magnet,
        )


def inline_query(bot, update):
    query = update.inline_query.query

    key_word = query.split()[0]

    if not re.search(r"\d", key_word):
        briefs = Functions.search_by_actress(key_word, 20)

    else:
        briefs = [Functions.get_brief(key_word)]

    if not briefs:
        return

    results = [
        telegram.InlineQueryResultPhoto(
            uuid4(),
            brief.preview_img_url,
            brief.preview_img_url,
            caption="\n".join(
                filter(lambda x: x, (brief.code, brief.title, brief.actress))
            ),
        )
        for brief in briefs
    ]

    update.inline_query.answer(results)


class Interactive:
    __init__ = None

    @staticmethod
    def start(bot, update):
        chat_history.clear_history(update.message.from_user.id)

        reply_markup = telegram.ReplyKeyboardMarkup(
            [["Search", "New", "Random"], ["Brief", "Magnet"]], resize_keyboard=True
        )

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Hi, how can I help you?",
            reply_markup=reply_markup,
        )

    @staticmethod
    def random(bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな",
        )

    @classmethod
    @chat_history.update_history
    def message(cls, bot, update):
        cmd_chat_history = chat_history.history[update.message.from_user.id][0]
        if len(cmd_chat_history) == 1:
            if cmd_chat_history[-1] == "Search":
                reply_markup = telegram.ReplyKeyboardRemove(selective=True)
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Search a code or an actress. e.g. ABP-231 or 桃乃木かな",
                    reply_markup=reply_markup,
                    reply_to_message_id=update.message.message_id,
                )
            elif cmd_chat_history[-1] == "New":
                bot.send_message(
                    chat_id=update.message.chat_id, text="How many results? [Integer]"
                )
            elif cmd_chat_history[-1] == "Random":
                cls.random(bot, update)
                chat_history.clear_history(update.message.from_user.id)
            elif cmd_chat_history[-1] == "Brief":
                bot.send_message(
                    chat_id=update.message.chat_id, text="Search a code. e.g. ABP-231"
                )
            elif cmd_chat_history[-1] == "Magnet":
                bot.send_message(
                    chat_id=update.message.chat_id, text="Search a code. e.g. ABP-231"
                )

        elif len(cmd_chat_history) == 2:
            if cmd_chat_history[-2] == "Search":
                if re.search(r"\d", update.message.text):
                    res = Functions.search_by_code(update.message.text)
                    send_av(bot, update, res)
                    chat_history.clear_history(update.message.from_user.id)

                else:
                    if cmd_chat_history[-2] == "Search":
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="How many results? [Integer]",
                        )

            elif cmd_chat_history[-2] == "New":
                send_brief(
                    bot,
                    update,
                    Functions.get_newly_released(int(cmd_chat_history[-1]), False),
                )
                chat_history.clear_history(update.message.from_user.id)

            elif cmd_chat_history[-2] == "Brief":
                send_brief(bot, update, Functions.get_brief(cmd_chat_history[-1]))
                chat_history.clear_history(update.message.from_user.id)

            elif cmd_chat_history[-2] == "Magnet":
                send_magnet(bot, update, Functions.get_magnet(cmd_chat_history[-1]))
                chat_history.clear_history(update.message.from_user.id)

        elif len(cmd_chat_history) == 3:
            if cmd_chat_history[-3] == "Search":
                res, _ = Functions.search_by_actress(
                    cmd_chat_history[-2], int(cmd_chat_history[-1])
                )
                send_brief(bot, update, res)
                chat_history.clear_history(update.message.from_user.id)

        return
