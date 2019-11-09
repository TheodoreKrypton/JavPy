import time
from collections import defaultdict
import threading


history = defaultdict(lambda: [[], time.time()])


def update_history(func):
    def _wrapper(*args, **kwargs):
        _, update = args[-2:]
        history[update.message.from_user.id][0].append(update.message.text)
        history[update.message.from_user.id][1] = time.time()
        func(*args, **kwargs)

    return _wrapper


def clear_history(user_id):
    if user_id in history:
        del history[user_id]


def clear_died_session_thread():
    while True:
        time.sleep(0.5)
        now = time.time()
        for k in history.keys():
            if now - history[k][1] > 3600:
                del history[k]


__clear_died_session_thread_started = False


def start_clear_died_session():
    global __clear_died_session_thread_started
    if __clear_died_session_thread_started:
        return
    __clear_died_session_thread_started = True
    t = threading.Thread(target=clear_died_session_thread)
    t.setDaemon(True)
    t.start()
