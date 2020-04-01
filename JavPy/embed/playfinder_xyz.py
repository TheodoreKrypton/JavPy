import requests
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.embed.fvs_io import fvs_io
import json
from JavPy.utils.config import proxy


class playfinder_xyz(BaseEmbed):
    @staticmethod
    def decode(url):
        video_id = url.split("#")[0].split("/v/").pop().split("/")[0]
        rsp = requests.post(
            "https://playfinder.xyz/api/source/%s" % video_id,
            r'{r: "", d: "smartshare.tv"}',
            proxies=proxy
        )
        obj = json.loads(rsp.text)
        url = fvs_io.decode(obj["data"][-1]["file"])
        return url

    @staticmethod
    def pattern(url):
        if "playfinder.xyz" in url:
            return True
        return False


if __name__ == '__main__':
    print(playfinder_xyz.decode("https://playfinder.xyz/v/7q970kx-wog#poster=https://findercdn.me/cdn/movie/s1no-1style-ssni-351-yoshitaka-nene-the-adviser-of-the-bad-female-teacher-was-a-humiliation-tennis-club-with-only-devil-pupils_1542526435.png"))