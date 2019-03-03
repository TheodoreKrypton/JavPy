from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from functions import Functions
import json


app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route("/search_by_code", methods=['POST'])
def search_by_code():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    res = []
    if params["code"]:
        res = [Functions.search_by_code(params["code"]).to_dict()]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/search_by_actress", methods=['POST'])
def search_by_actress():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    res = []

    if params["actress"]:
        res = Functions.search_by_actress(params["actress"], False, 30)
        if res:
            res = [x.to_dict() for x in res]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/new", methods=['POST'])
def new():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    res = Functions.get_newly_released(False, 30)
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
