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
import JavPy.utils.config as config
import JavPy.utils.buggyauth as auth
from copy import deepcopy
import requests
from JavPy.utils.config import proxy


base_path = "/".join(os.path.abspath(__file__).replace("\\", "/").split("/")[:-3])
static_folder = base_path + "/app/javpy-react/build/static"
template_folder = base_path + "/app/javpy-react/build"

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
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
    if auth.check_password(params["password"], request.remote_addr):
        cookie = auth.generate_cookie(request)
        return cookie
    else:
        return make_response("auth failed"), 400


@app.route("/get_config", methods=["POST"])
def get_config():
    cfg = deepcopy(config.Config.config)
    cfg["password"] = ""
    return json.dumps(cfg)


@app.route("/update_config", methods=["POST"])
def update_config():
    data = json.loads(request.data.decode("utf-8"))
    if data["password"]:
        config.Config.set_config("hashed-password", data["password"])
    config.Config.set_config("ip-blacklist", data["ip-blacklist"])
    config.Config.set_config("ip-whitelist", data["ip-whitelist"])
    config.Config.save_config()

    import importlib

    importlib.reload(config)
    importlib.reload(auth)
    return ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(template_folder, path)

#
# @app.route("/manifest.json")
# def manifest_json():
#     return send_from_directory(base_path + '/app/javpy-react/build/', 'manifest.json')


@app.route("/search_by_code", methods=["POST"])
def search_by_code():
    params = json.loads(request.data.decode("utf-8"))
    print(params)
    res = {"videos": None, "other": None}
    if params["code"]:
        try:
            videos = Functions.search_by_code(params["code"])
            if videos:
                res["videos"] = [videos.to_dict()]
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
    with_profile = params["with_profile"] == "true"
    briefs, profile = Functions.search_by_actress(actress, None, with_profile)

    if with_profile:
        history_names = profile.other["history_names"]

        res = {
            "videos": [brief.to_dict() for brief in briefs],
            "profile": profile.to_dict(),
            "history_names": history_names,
        }

    else:
        res = {"videos": [brief.to_dict() for brief in briefs]}

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
    if res is None:
        return ""
    rsp = jsonify(res.to_dict())
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


# dmm.co.jp blocks direct image request. so use this proxy when there is a loading error.
@app.route("/img")
def img():
    src = request.args["src"]
    content = requests.get(src, proxies=proxy).content
    if src.endswith("jpg") or src.endswith("jpeg"):
        return Response(content, mimetype="image/jpeg")
    if src.endswith("png"):
        return Response(content, mimetype="image/png")
    if src.endswith("bmp"):
        return Response(content, mimetype="image/bmp")
    return Response(content)


# avoid the main window being redirect to annoying ads pages.
@app.route("/redirect_to")
def open_url():
    rsp = redirect(request.args["url"])
    rsp.headers["origin"] = ""
    return rsp
