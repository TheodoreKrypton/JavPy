# encoding: utf-8

import requests
import bs4
import re
from JavPy.utils.common import try_evaluate


class Etigoya:
    url_pattern = re.compile("http://etigoya955.+?blog-entry-.+?html")
    name_pattern = re.compile('<span style="color: .+?"><span style="font-size: medium">(.+?)</span>')
    purify_pattern = re.compile('<.+?>')

    @staticmethod
    def get_history_names(actress):
        url = "http://etigoya955.blog49.fc2.com/?q=" + actress + "&charset=utf-8"
        html = requests.get(url).text
        bs = bs4.BeautifulSoup(html, "lxml")
        main = bs.select("#main")[0]
        li = main.select("li", limit=1)[0]
        if "スポンサー広告" in str(li):
            return None
        url = try_evaluate(lambda: re.search(Etigoya.url_pattern, str(li)).group(0))[0]
        if not url:
            return None

        html = requests.get(url).text
        names = [re.sub(Etigoya.purify_pattern, "", s) for s in re.findall(Etigoya.name_pattern, html)]
        return names


if __name__ == '__main__':
    print(Etigoya.get_history_names("水野あき"))
