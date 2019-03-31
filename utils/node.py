import subprocess
import os
import sys
import tempfile


def use_node(script):
    try:
        with tempfile.NamedTemporaryFile('w') as tmp:
            tmp.write(script)
            tmp.seek(0)
            return subprocess.getoutput("node " + tmp.name)
    except Exception as ex:
        print(ex)


class Node:
    def __init__(self):
        pass

    node = None

    @classmethod
    def start_node(cls):
        cls.node = subprocess.Popen(
            ['node', os.path.abspath(".")[:os.path.abspath(".").find("JavPy")] + "JavPy/node/app.js"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=False
        )
        cls.node.kill()

    @classmethod
    def pass_cmd(cls, cmd):
        cls.node.stdin.write(cmd)
        cls.node.stdout.flush()
        res = cls.node.stdout.readline()
        return res

    @classmethod
    def pass_cmd_v3(cls, cmd):
        cmd = cmd.encode('utf-8')
        cls.node.stdin.write(cmd)
        cls.node.stdout.flush()
        res = cls.node.stdout.readline()
        return res.decode('utf-8')

    if sys.version_info.major == 3:
        pass_cmd = pass_cmd_v3

    @classmethod
    def kill_node(cls):
        if cls.node:
            cls.node.kill()


if __name__ == '__main__':
    print(use_node(open("../test.js").read()))