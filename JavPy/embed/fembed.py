from JavPy.embed.BaseEmbed import BaseEmbed
import requests
import json
from JavPy.utils.config import proxy


class fembed(BaseEmbed):
    @staticmethod
    def decode(url):
        code = url.split("/")[-1]
        url = "http://www.fembed.com/api/source/" + code
        rsp = requests.post(url, proxies=proxy)
        json_obj = json.loads(rsp.text)
        url = json_obj["data"][0]["file"]
        rsp = requests.get(url, allow_redirects=False, proxies=proxy)
        return rsp.headers["Location"]

    @staticmethod
    def pattern(url):
        if "fembed" in url:
            return True
        else:
            return False
