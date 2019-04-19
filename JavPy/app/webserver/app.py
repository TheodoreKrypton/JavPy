from __future__ import absolute_import, print_function, unicode_literals
from flask import Flask, make_response, jsonify, request, render_template, send_from_directory, abort
from flask_cors import CORS
from JavPy.functions import Functions
import json
import os
from JavPy.utils.requester import spawn
from JavPy.utils.buggyauth import check_ip, check_password, generate_cookie, cookie_exists


base_path = "/".join(os.path.abspath(__file__).replace("\\", "/").split("/")[:-3])
web_dist_path = base_path + "/app/web/dist"
app = Flask(__name__, template_folder=web_dist_path)
CORS(app, resources=r'/*')


@app.before_first_request
def before_first_request():
    pass


@app.before_request
def before_request():
    ip = request.remote_addr
    if not check_ip(ip):
        abort(400)

    if 'userpass' in request.cookies and not cookie_exists(request.cookies['userpass']):
        abort(400)


@app.route("/auth_by_password", methods=['POST'])
def auth_by_password():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    if check_password(params['password']):
        cookie = generate_cookie(request)
        rsp = make_response("")
        rsp.set_cookie('userpass', cookie)
        return rsp
    else:
        abort(400)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(web_dist_path, path)


@app.route("/search_by_code", methods=['POST'])
def search_by_code():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    res = {
        'videos': None,
        'other': None
    }
    if params["code"]:
        try:
            res['videos'] = [Functions.search_by_code(params["code"]).to_dict()]
            rsp = jsonify(res)
        except AttributeError:
            rsp = make_response("")
    else:
        rsp = make_response("")
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/search_by_actress", methods=['POST'])
def search_by_actress():
    params = json.loads(request.data.decode('utf-8'))
    print(params)

    res = {}

    actress = params['actress']
    history_name = params['history_name'] == "true"
    briefs = spawn(Functions.search_by_actress, actress, 30)

    if history_name:
        names = spawn(Functions.search_history_names, actress)
        res = {
            'other': {
                'history_name': names.wait_for_result()
            }
        }

    res['videos'] = [x.to_dict() for x in briefs.wait_for_result()]
    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/new", methods=['POST'])
def new():
    params = json.loads(request.data.decode('utf-8'))
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


@app.route("/search_magnet_by_code", methods=['POST'])
def search_magnet_by_code():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    res = []

    if params["code"]:
        res = Functions.get_magnet(params["code"])
        if res:
            res = [x.to_dict() for x in res]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp
