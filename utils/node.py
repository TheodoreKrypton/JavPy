import subprocess

node = None


def start():
    global node
    node = subprocess.Popen(['node', "node/app.js"])


def exec_node(cmd):
    return node.communicate(cmd)
