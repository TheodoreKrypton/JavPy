from JavPy.app.webserver.app import app
from JavPy.app.tgbot.server import run
import os
import time
import threading
import sys
import argparse

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
    time.sleep(3)
    url = "http://localhost:" + str(port)

    if "win32" in sys.platform:
        os.system('start "" "' + url + '"')
    elif "linux" in sys.platform:
        os.system("xdg-open " + url)
    else:
        os.system("open " + url)


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, nargs='?', default="0.0.0.0", help="specify which ip should the app listen to")
    parser.add_argument("--port", type=int, nargs='?', default=8081, help="specify which port should the app listen to")
    args = parser.parse_args()
    threading.Thread(target=open_browser, args=(args.port,)).start()
    app.run("0.0.0.0", args.port, threaded=True)


def serve_tg(token):
    run(token)
