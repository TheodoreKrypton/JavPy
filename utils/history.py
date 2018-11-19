import time
from collections import defaultdict


history = defaultdict(lambda: [[], time.time()])


def update_history(func):
    def _wrapper(bot, update):
        history[update.message.from_user.id][0].append(update.message.text)
        history[update.message.from_user.id][1] = time.time()
        func(bot, update)
    return _wrapper
