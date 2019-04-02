from flask import Flask, make_response, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from functions import Functions
import json
import os

base_path = "/".join(os.path.abspath(__file__).replace("\\", "/").split("/")[:-3])
web_dist_path = base_path + "/app/web/dist"

app = Flask(__name__, template_folder=web_dist_path)
CORS(app, resources=r'/*')


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(web_dist_path + '/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(web_dist_path + '/css', path)


@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory(web_dist_path + '/fonts', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(web_dist_path + '/img', path)


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
            # print(res)
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
    res = {
        'videos': None,
        'other': None
    }

    if params["actress"]:
        briefs = Functions.search_by_actress(params["actress"].strip(), 30)
        if briefs:
            res['videos'] = [x.to_dict() for x in sorted(briefs, key=lambda x: x.release_date, reverse=True)]

        if params["history_name"]:
            res['other'] = {
                'history_name': Functions.search_history_names(params['actress'])
            }

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
