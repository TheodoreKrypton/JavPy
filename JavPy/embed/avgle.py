import requests
import re
import six
from JavPy.embed.BaseEmbed import BaseEmbed

if six.PY2:
    import urllib
elif six.PY3:
    import urllib.parse as urllib


class avgle(BaseEmbed):
    @staticmethod
    def decode(url):
        rsp = requests.get(url)
        video_hkey = re.search("video_hkey = '(.+?)';", rsp.text).group(1)
        title = re.search("video_title = '(.+?)'", rsp.text).group(1)
        url = (
            "https://avgle.com/video/"
            + video_hkey
            + "/"
            + urllib.quote(title.encode("utf-8"))
        )
        return url

    @staticmethod
    def pattern(url):
        if "avgle" in url:
            return True
        return False


if __name__ == "__main__":
    print(avgle.decode("https://avgle.com/embed/f2839fcc751e7f12679c"))
