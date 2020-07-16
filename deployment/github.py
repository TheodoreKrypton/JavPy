import os
import requests
import json
from JavPy.utils.common import version
from deployment.docker import generate_version


def in_publish():
    if "GITHUB_WORKFLOW" in os.environ and \
            os.environ["GITHUB_WORKFLOW"] == "Publish Python Package":
        return True
    return False


def in_release():
    if "GITHUB_WORKFLOW" in os.environ and \
            os.environ["GITHUB_WORKFLOW"] == "Make Release" and \
            "GITHUB_RUN_NUMBER" in os.environ:
        return True
    return False


def make_release():
    primary, secondary = version.split(".")
    build_id = os.environ["GITHUB_RUN_NUMBER"]
    release_tag = "%s.%s.%s" % (primary, secondary, build_id)

    rsp = requests.post("https://api.github.com/repos/TheodoreKrypton/JavPy/releases", data=json.dumps({
        "tag_name": "v%s" % release_tag,
        "target_commitish": "release",
        "name": "Enjoy Driving!",
        "body": "",
        "draft": False,
        "prerelease": False
    }), headers={
        "Authorization": "token %s" % os.environ["GITHUB_TOKEN"]
    })

    if rsp.status_code != 201:
        exit(-1)


def merge_to_release():
    with open(os.environ["GITHUB_EVENT_PATH"]) as fp:
        obj = json.loads(fp.read())
        pull_number = obj["pull_request"]["number"]
    rsp = requests.put(
        "https://api.github.com/repos/TheodoreKrypton/JavPy/pulls/{}/merge".format(pull_number),
        data=json.dumps({"merge_method": "squash"}),
        headers={"Authorization": "token %s" % os.environ["GITHUB_TOKEN"]}
    )

    if rsp.status_code != 200:
        exit(-1)


def delete_branch():
    print("https://api.github.com/repos/octocat/Hello-World/git/{}".format(os.environ["GITHUB_REF"]))
    requests.delete(
        "https://api.github.com/repos/octocat/Hello-World/git/{}".format(os.environ["GITHUB_REF"]),
        headers={"Authorization": "token %s" % os.environ["GITHUB_TOKEN"]}
    )


def publish():
    requests.post("https://api.github.com/repos/TheodoreKrypton/JavPy/dispatches", data={
        "event_type": "publish",
    })
