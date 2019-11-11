import subprocess
import re
import platform
import os

devnull = open(os.devnull, "w")


def ping(host, n=1):
    if platform.platform().startswith("Windows"):
        p = subprocess.Popen(
            ["ping", "-n", str(n), host], stdout=subprocess.PIPE, stderr=devnull
        )
        stdout, _ = p.communicate()
        if b"=" not in stdout:
            return None
        return int(re.findall(r"\d+", str(stdout))[-1])
    else:
        p = subprocess.Popen(
            ["ping", "-c", str(n), host], stdout=subprocess.PIPE, stderr=devnull
        )
        stdout, _ = p.communicate()
        if not stdout:
            return None
        last_line = str(stdout).split("\\n")[-2]
        return int(float(last_line.split("=")[1].split("/")[1]))


if __name__ == "__main__":
    print(ping("www.google.com"))
