from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.BaseSource import ISearchByCode
import requests
import re
import bs4
from JavPy.functions.datastructure import AV
import subprocess


class XOpenloadVideo(ISearchByCode):
    def __init__(self):
        pass

    @classmethod
    def search_by_code(cls, code):
        url = "https://www.xopenload.video/search.php?s=" + code
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        try:
            div = bs.find(name='div', attrs={'class': 'poster'})

            img = div.a.img.attrs['src']
            url = div.a.attrs['href']
        except AttributeError:
            return None

        rsp = requests.get(url)
        _hash = re.search(r"https://www\.xopenload\.video/links\.php\?hash=(.+?)\"", rsp.text).group(1)
        url = "https://www.xopenload.video/links.php?hash=" + _hash

        rsp = requests.get(url)

        js = re.search(r"<script language=\"javascript\">(.+?)</script>", rsp.text, re.S).group(1)\
            .replace("document", "console")\
            .replace("write", "log")

        response = subprocess.Popen(["node", "-e", "%s" % js], stdout=subprocess.PIPE).stdout.read().decode()

        url = re.findall(r"https://.+?\"", response)[0][:-1]

        av = AV()
        av.code = code
        av.preview_img_url = img
        av.video_url = url

        return av
