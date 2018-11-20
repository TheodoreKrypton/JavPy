import time
from collections import defaultdict
import threading


history = defaultdict(lambda: [[], time.time()])


def update_history(func):
    def _wrapper(*args, **kwargs):
        bot, update = args[-2:]
        history[update.message.from_user.id][0].append(update.message.text)
        history[update.message.from_user.id][1] = time.time()
        func(*args, **kwargs)
    return _wrapper


def clear_history(user_id):
    if user_id in history:
        del history[user_id]


def clear_died_session():
    while True:
        time.sleep(3600)
        now = time.time()
        for k in history.keys():
            if now - history[k][1] > 3600:
                del history[k]


t = threading.Thread(target=clear_died_session)
t.start()
