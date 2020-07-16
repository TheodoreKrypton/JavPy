import os
from JavPy.utils.common import version
import requests


def in_build():
    if "DOCKER" in os.environ and os.environ["DOCKER"] == "1":
        return True
    return False


def generate_version():
    if "VERSION" in os.environ:
        return os.environ["VERSION"]
    else:
        return version


def trigger_build():
    requests.get(os.environ["DOCKER_BUILD_URL"])
