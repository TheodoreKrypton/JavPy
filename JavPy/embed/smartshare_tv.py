import requests
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.embed.fvs_io import fvs_io
import json
from JavPy.utils.config import proxy


class smartshare_tv(BaseEmbed):
    @staticmethod
    def decode(url):
        video_id = url.split("/v/").pop().split("/")[0]
        rsp = requests.post(
            "https://smartshare.tv/api/source/%s" % video_id,
            r'{r: "", d: "smartshare.tv"}',
            verify=False,
            proxies=proxy
        )
        obj = json.loads(rsp.text)
        url = fvs_io.decode(obj["data"][-1]["file"])
        return url

    @staticmethod
    def pattern(url):
        if "smartshare" in url:
            return True
        return False


if __name__ == "__main__":
    print(smartshare_tv.decode("https://smartshare.tv/v/kdrx7f3z2ernewj"))
