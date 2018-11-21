import subprocess
import os

node = None


def start():
    global node
    node = subprocess.Popen(['node', os.path.abspath(".")[:os.path.abspath(".").find("JavPy")] + "JavPy/node/app.js"])


def exec_node(cmd):
    return node.communicate(cmd)


def kill_node():
    if node:
        node.kill()
