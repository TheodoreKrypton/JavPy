import os


def in_build():
    if "DOCKER" in os.environ and os.environ["DOCKER"] == "1":
        return True
    return False
