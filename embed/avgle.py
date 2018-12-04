import requests
import re
import six

if six.PY2:
    import urllib
elif six.PY3:
    import urllib.parse as urllib


class avgle:
    @staticmethod
    def decode(url):
        rsp = requests.get(url, verify=False)
        video_hkey = re.search("video_hkey = '(.+?)';", rsp.text).group(1)
        title = re.search("video_title = '(.+?)'", rsp.text).group(1)
        url = "https://avgle.com/video/" + video_hkey + "/" + urllib.quote(title.encode('utf-8'))
        return url
