from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from functions import Functions
import json


app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route("/search_by_code", methods=['POST'])
def search():
    params = json.loads(request.data)

    res = []

    if params["code"]:
        res = [Functions.search_by_code(params["code"]).to_dict()]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp


@app.route("/search_by_actress", methods=['POST'])
def search():
    params = json.loads(request.data)
    res = []

    if params["actress"]:
        res = [Functions.search_by_actress(params["actress"], False, 30).to_dict()]

    rsp = jsonify(res)
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp
