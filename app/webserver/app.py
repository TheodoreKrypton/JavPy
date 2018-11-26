from flask import Flask, make_response, jsonify


app = Flask(__name__)


@app.route("/search", methods=['GET'])
def search():
    rsp = jsonify({"text": "Hello World!"})
    rsp.headers["Access-Control-Allow-Origin"] = "*"
    return rsp
