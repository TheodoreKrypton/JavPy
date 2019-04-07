# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.BaseSource import IHistoryNames
import requests
import bs4
import re
from JavPy.utils.common import try_evaluate


class Etigoya(IHistoryNames):
    url_pattern = re.compile("http://etigoya955.+?blog-entry-.+?html")
    name_pattern = re.compile('<span style="color: .+?"><span style="font-size: medium">(.+?)</span>')
    purify_pattern = re.compile('<.+?>')

    @classmethod
    def get_history_names(cls, actress):
        url = "http://etigoya955.blog49.fc2.com/?q=" + actress + "&charset=utf-8"
        html = requests.get(url).text
        bs = bs4.BeautifulSoup(html, "lxml")
        main = bs.select("#main")[0]
        lis = main.select("li", limit=1)

        if len(lis) == 1:
            if "スポンサー広告" in str(lis[0]):
                return []

        for li in lis:
            if actress not in str(li):
                continue
            url = try_evaluate(lambda: re.search(Etigoya.url_pattern, str(li)).group(0))[0]
            if not url:
                return []

            html = requests.get(url).text
            names = [re.sub(Etigoya.purify_pattern, "", s) for s in re.findall(Etigoya.name_pattern, html)]
            return names

        return []


if __name__ == '__main__':
    print(Etigoya.get_history_names("水野あき"))
