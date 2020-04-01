import requests
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.embed.fvs_io import fvs_io
import json
from JavPy.utils.config import proxy


class javcl_me(BaseEmbed):
    @staticmethod
    def decode(url):
        video_id = url.split("#")[0].split("/v/").pop().split("/")[0]
        rsp = requests.post(
            "https://javcl.me/api/source/%s" % video_id,
            r'{r: "", d: "javcl.me"}',
            proxies=proxy
        )
        obj = json.loads(rsp.text)
        url = fvs_io.decode(obj["data"][-1]["file"])
        return url

    @staticmethod
    def pattern(url):
        if "javcl.me" in url:
            return True
        return False


if __name__ == '__main__':
    print(javcl_me.decode("https://javcl.me/v/3j-yxamj7pxjw3n"))