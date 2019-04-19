# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import str
import requests
import bs4
from JavPy.functions.datastructure import Brief
import re
from JavPy.utils.common import try_evaluate
from JavPy.sources.BaseSource import IGetBrief


class AVSoxNet(IGetBrief):
    __url_pattern = re.compile('movie-box.+?href="(.+?)"')
    __release_date_pattern = re.compile(u'发行时间:</span> (.+?)</p>')

    @classmethod
    def get_brief(cls, code):
        url = "https://avsox.net/cn/search/" + code
        rsp = requests.get(url)
        html = rsp.text

        url = re.search(cls.__url_pattern, html).group(1)
        rsp = requests.get(url)
        html = rsp.text

        bs = bs4.BeautifulSoup(html, "lxml")
        movie = bs.select(".movie")[0]

        brief = Brief()
        brief.code = code
        img = movie.select(".screencap", limit=1)[0].a.img
        brief.title = img.attrs['title']

        brief.set_release_date(try_evaluate(lambda: re.search(cls.__release_date_pattern, str(movie)).group(1), "")[0])
        brief.actress = ", ".join(x.text for x in bs.select("#avatar-waterfall", limit=1)[0].find_all('span'))

        rsp = requests.get(img.attrs['src'])
        if 300 <= rsp.status_code <= 400:
            if "location" in rsp.headers:
                brief.preview_img_url = rsp.headers['location']
        elif rsp.status_code == 200:
            brief.preview_img_url = img.attrs['src']

        return brief
