import requests
import re
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.utils.config import proxy
import urllib.parse


class avgle(BaseEmbed):
    @staticmethod
    def decode(url):
        rsp = requests.get(url, proxies=proxy)
        matched = re.search("video_hkey = '(.+?)';", rsp.text)
        if not matched:
            return None
        video_hkey = matched.group(1)
        title = re.search("video_title = '(.+?)'", rsp.text).group(1)
        url = (
            "https://avgle.com/video/"
            + video_hkey
            + "/"
            + urllib.parse.quote(title.encode("utf-8"))
        )

        return url

    @staticmethod
    def pattern(url):
        if "avgle" in url:
            return True
        return False


if __name__ == "__main__":
    print(avgle.decode("https://avgle.com/embed/f2839fcc751e7f12679c"))
