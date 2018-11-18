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
