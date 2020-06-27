import json
import requests
from JavPy.app.webserver.app import app, template_folder
import os
import hashlib
from JavPy.utils.config import proxy
import pytest

app.config["TESTING"] = True
password = ""
client = app.test_client()


def get_userpass():
    rv = client.post("/auth_by_password",
                     data=json.dumps({"password": hashlib.sha256(password.encode("utf-8")).hexdigest()}))
    return rv.data.decode("utf-8")


def test_static_files():
    if not os.path.exists(template_folder):
        os.mkdir(template_folder)
    with open(os.path.join(template_folder, "test_index.html"), "w") as fp:
        fp.write(str("<html></html>"))
    rv = client.get("/test_index.html")
    assert rv.data.decode("utf-8") == "<html></html>"


@pytest.mark.parametrize("code", ["ABP-231", "ABP-123", "SSNI-351"])
def test_search_by_code(code):
    rv = client.post("/search_by_code", data=json.dumps({"code": code, "userpass": get_userpass()}))
    rsp = json.loads(rv.data.decode("utf-8"))
    assert len(rsp["videos"]) == 1
    assert requests.get(rsp["videos"][0]["video_url"], proxies=proxy).status_code == 200


@pytest.mark.parametrize("actress", ["川合まゆ", "唯川みさき", "瀬奈まお", "原更紗", "Nao Jinguuji", "Eimi Fukada"])
def test_search_by_actress(actress):
    rv = client.post(
        "/search_by_actress",
        data=json.dumps({"actress": actress, "with_profile": "true", "userpass": get_userpass()})
    )
    rsp = json.loads(rv.data.decode("utf-8"))
    assert len(rsp["history_names"]) > 0
    assert len(rsp["videos"]) > 0


@pytest.mark.parametrize("code", ["ABP-231", "ABP-123", "SSNI-351", "n0753"])
def test_search_magnet_by_code(code):
    rv = client.post("/search_magnet_by_code", data=json.dumps({"code": code, "userpass": get_userpass()}))
    rsp = json.loads(rv.data.decode("utf-8"))
    assert len(rsp) > 0


@pytest.mark.parametrize("data", [{"up_to": 30}, {"page": 1}])
def test_newly_released(data):
    data["userpass"] = get_userpass()
    rv = client.post("/new", data=json.dumps(data))
    rsp = json.loads(rv.data.decode("utf-8"))
    assert len(rsp) > 0


if __name__ == "__main__":
    # test_static_files()
    # test_search_by_code()
    test_search_by_actress()
    # test_search_magnet_by_code()
    # test_newly_released()
