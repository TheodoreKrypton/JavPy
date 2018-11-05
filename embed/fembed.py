import requests
import json


class fembed:
    @staticmethod
    def decode(url):
        code = url.split("/")[-1]
        url = "https://www.fembed.com/api/sources/" + code
        rsp = requests.post(url, verify=False)
        json_obj = json.loads(rsp.text)
        return json_obj["data"][0]["file"]