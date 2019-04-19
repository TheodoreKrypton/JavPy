# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import str, filter
from JavPy.sources.BaseSource import IHistoryNames
import requests
import bs4
import re
from JavPy.utils.common import try_evaluate
from JavPy.utils.requester import Task, spawn_many


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

        if len(lis) == 1 and u"スポンサー広告" in str(lis[0]):
            return []

        res = spawn_many((Task(cls.get_history_names_by_li, li) for li in lis)).wait_until(lambda rsp: actress in rsp)
        res = next(filter(lambda names: names and actress in names, res))

        return res

    @classmethod
    def get_history_names_by_li(cls, li):
        url = try_evaluate(lambda: re.search(Etigoya.url_pattern, str(li)).group(0))[0]
        if not url:
            return []
        html = requests.get(url).text
        names = [re.sub(Etigoya.purify_pattern, "", s).strip() for s in re.findall(Etigoya.name_pattern, html)]
        return names


if __name__ == '__main__':
    print(Etigoya.get_history_names("水野あき"))
