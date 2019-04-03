import requests
import json
import six


class fembed:
    @staticmethod
    def decode(url):
        code = url.split("/")[-1]
        if six.PY2:
            code = code.encode("ascii")
        url = "http://www.fembed.com/api/source/" + code
        rsp = requests.post(url)
        json_obj = json.loads(rsp.text)
        url = "http://www.fembed.com" + json_obj["data"][0]["file"]
        rsp = requests.get(url, allow_redirects=False)
        return rsp.headers["Location"]
