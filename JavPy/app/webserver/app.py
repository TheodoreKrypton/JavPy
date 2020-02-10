from __future__ import absolute_import, print_function, unicode_literals
from flask import (
    Flask,
    make_response,
    jsonify,
    request,
    render_template,
    send_from_directory,
    abort,
    redirect,
    Response,
)
from flask_cors import CORS
from JavPy.functions import Functions
import json
import os
from JavPy.utils.requester import spawn
import JavPy.utils.config as config
import JavPy.utils.buggyauth as auth
from copy import deepcopy
import requests
from JavPy.utils.config import proxy


base_path = "/".join(os.path.abspath(__file__).replace("\\", "/").split("/")[:-3])
web_dist_path = base_path + "/app/web/dist"
app = Flask(__name__, template_folder=web_dist_path)
CORS(app, resources=r"/*")


@app.before_first_request
def before_first_request():
    pass


@app.before_request
def before_request():
    if request.full_path == "/auth_by_password?":
        return
    if not auth.check_request(request):
        abort(400)


@app.route("/auth_by_password", methods=["POST"])
def auth_by_password():
    params = json.loads(request.data.decode("utf-8"))
    print(params)
    if auth.check_password(params["password"]):
        cookie = auth.generate_cookie(request)
        return cookie
    else:
        return make_response("auth failed"), 400


@app.route("/get_config", methods=["POST"])
def get_config():
    cfg = deepcopy(config.Config.config)
    if "password" in cfg:
        del cfg["password"]
    return json.dumps(cfg)


@app.route("/update_config", methods=["POST"])
def update_config():
    data = json.loads(request.data.decode("utf-8"))
    if data["password"]:
        config.Config.set_config("password", data["password"])
    config.Config.set_config("ip-blacklist", data["ipBlacklist"])
    config.Config.set_config("ip-whitelist", data["ipWhitelist"])
    config.Config.save_config()

    try:
        import importlib

        _reload = importlib.reload
    except (ImportError, AttributeError):
        _reload = reload
    _reload(config)
    _reload(auth)
    return ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:path>")
def send_static(path):
    if not os.path.exists(web_dist_path + "/" + path):
        return render_template("index.html")
    else:
        return send_from_directory(web_dist_path, path)


@app.route("/search_by_code", methods=["POST"])
def search_by_code():
    params = json.loads(request.data.decode("utf-8"))
    print(params)
    res = {"videos": None, "other": None}
    if params["code"]:
        try:
            res["videos"] = [Functions.search_by_code(params["code"]).to_dict()]
            rsp = jsonify(res)
        except AttributeError:
            rsp = make_response("")
    else:
        rsp = make_response("")
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/search_by_actress", methods=["POST"])
def search_by_actress():
    params = json.loads(request.data.decode("utf-8"))
    print(params)
    actress = params["actress"]
    history_name = params["history_name"] == "true"
    briefs, names = spawn(
        Functions.search_by_actress, actress, None, history_name
    ).wait_for_result()

    res = {
        "videos": [brief.to_dict() for brief in briefs],
        "other": {"history_names": names},
    }
    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/new", methods=["POST"])
def new():
    params = json.loads(request.data.decode("utf-8"))
    print(params)

    if "up_to" in params:
        res = Functions.get_newly_released(params["up_to"], False)
    elif "page" in params:
        res = Functions.get_newly_released(False, params["page"])
    else:
        res = Functions.get_newly_released(30, False)

    if res:
        res = [x.to_dict() for x in res]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"

    return rsp


@app.route("/search_magnet_by_code", methods=["POST"])
def search_magnet_by_code():
    params = json.loads(request.data.decode("utf-8"))
    print(params)
    res = []

    if params["code"]:
        res = Functions.get_magnet(params["code"])
        if res:
            res = [x.to_dict() for x in res]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/get_tags", methods=["POST"])
def get_tags():
    params = json.loads(request.data.decode("utf-8"))
    print(params)

    res = Functions.get_tags()

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/actress_info", methods=["POST"])
def actress_info():
    params = json.loads(request.data.decode("utf-8"))
    print(params)

    res = Functions.get_actress_info(params["actress"])

    rsp = jsonify(res.to_dict())
    print(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


# dmm.co.jp blocks direct image request. so use this proxy when there is a loading error.
@app.route("/img")
def img():
    src = request.args['src']
    content = requests.get(src, proxies=proxy).content
    if src.endswith("jpg") or src.endswith("jpeg"):
        return Response(content, mimetype="image/jpeg")
    if src.endswith("png"):
        return Response(content, mimetype="image/png")
    if src.endswith("bmp"):
        return Response(content, mimetype="image/bmp")
    return Response(content)
