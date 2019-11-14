import subprocess


def evaluate_js(code):
    pipe = subprocess.Popen(["node", "-e", code])
    pipe.wait()
    return pipe.returncode, pipe.stdout, pipe.stderr
