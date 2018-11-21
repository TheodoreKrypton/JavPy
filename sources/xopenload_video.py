from sources.BaseSource import ISearchByCode, SourceException
import requests
import re
import bs4
import json
from embed.decode import decode
from functions.datastructure import AV
import os
from utils import node


class XOpenloadVideo(ISearchByCode):
    def __init__(self):
        pass

    @classmethod
    def search_by_code(cls, code):
        url = "https://www.xopenload.video/search.php?s=" + code
        rsp = requests.get(url, verify=False)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        try:
            div = bs.find(name='div', attrs={'class': 'poster'})

            img = div.a.img.attrs['src']
            url = div.a.attrs['href']
        except AttributeError:
            return None

        rsp = requests.get(url, verify=False)
        _hash = re.search(r"https://www\.xopenload\.video/links\.php\?hash=(.+?)\"", rsp.text).group(1)
        url = "https://www.xopenload.video/links.php?hash=" + _hash

        rsp = requests.get(url, verify=False)

        js = re.search(r"<script language=\"javascript\">(.+?)</script>", rsp.text, re.S).group(1)\
            .replace("document", "console")\
            .replace("write", "log")

        res = node.exec_node(js)

        url = re.findall(r"https://.+?\"", res)[0][:-1]

        av = AV()
        av.code = code
        av.preview_img_url = img
        av.video_url = url

        return av
