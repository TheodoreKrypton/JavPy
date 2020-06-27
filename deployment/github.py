import os
from JavPy.utils.common import version
import requests
import json
import subprocess


def in_publish():
    if "GITHUB_WORKFLOW" in os.environ and \
            os.environ["GITHUB_WORKFLOW"] == "Publish Python Package" and \
            "GITHUB_RUN_NUMBER" in os.environ:
        return True
    return False


def in_release():
    if "GITHUB_WORKFLOW" in os.environ and \
            os.environ["GITHUB_WORKFLOW"] == "Release" and \
            "GITHUB_RUN_NUMBER" in os.environ:
        return True
    return False


def generate_version():
    primary, secondary = version.split(".")
    build_id = os.environ["GITHUB_RUN_NUMBER"]
    return "%s.%s.%s" % (primary, secondary, build_id)


def get_current_tag():
    output = subprocess.check_output("git tag --points-at HEAD")
    if not output.startswith("v"):
        exit(-1)
    return output


def make_release():
    rsp = requests.post("https://api.github.com/repos/TheodoreKrypton/JavPy/releases", data=json.dumps({
        "tag_name": "v%s" % generate_version(),
        "target_commitish": "master",
        "name": "Enjoy Driving!",
        "body": "",
        "draft": False,
        "prerelease": False
    }), headers={
        "Authorization": "token %s" % os.environ["GITHUB_TOKEN"]
    })

    if rsp.status_code != 201:
        exit(-1)
