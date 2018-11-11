import requests
import json


class fembed:
    @staticmethod
    def decode(url):
        code = url.split("/")[-1].encode("ascii")
        url = "http://www.fembed.com/api/source/" + code
        rsp = requests.post(url)
        json_obj = json.loads(rsp.text)
        return "http://www.fembed.com" + json_obj["data"][0]["file"]