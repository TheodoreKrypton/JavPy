from .app.webserver.app import app
from .app.tgbot.server import run
import os
import time
import threading
import sys

print(
    r"""
                       __            ____       
                      / /___ __   __/ __ \__  __
                 __  / / __ `/ | / / /_/ / / / /
                / /_/ / /_/ /| |/ / ____/ /_/ / 
                \____/\__,_/ |___/_/    \__, /  
                                       /____/   
"""
)


def open_browser(port):
    time.sleep(5)
    url = "http://localhost:" + str(port)

    if "win32" in sys.platform:
        os.system('start "" "' + url + '"')
    elif "linux" in sys.platform:
        os.system("xdg-open " + url)
    else:
        os.system("open " + url)


def serve(port=8081):
    threading.Thread(target=open_browser, args=(port,)).start()
    app.run("0.0.0.0", port, threaded=True)


def serve_tg(token):
    run(token)
