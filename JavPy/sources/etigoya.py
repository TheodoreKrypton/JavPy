from JavPy.sources.BaseSource import IHistoryNames
import requests
import bs4
import re
from JavPy.utils.common import noexcept
from JavPy.utils.requester import submit, wait_until
from JavPy.utils.config import proxy


class Etigoya(IHistoryNames):
    url_pattern = re.compile("http://etigoya955.+?blog-entry-.+?html")
    name_pattern = re.compile(
        '<span style="color: .+?"><span style="font-size: medium">(.+?)</span>'
    )
    purify_pattern = re.compile("<.+?>")

    @classmethod
    def get_history_names(mcs, actress):
        url = "http://etigoya955.blog49.fc2.com/?q=" + actress + "&charset=utf-8"
        html = requests.get(url, proxies=proxy).text
        bs = bs4.BeautifulSoup(html, "lxml")
        main = bs.select("#main")[0]
        lis = main.select("li", limit=1)

        if len(lis) == 1 and "スポンサー広告" in str(lis[0]):
            return []

        res = wait_until(
            [submit(mcs.get_history_names_by_li, li) for li in lis],
            condition=lambda rsp: actress in rsp
        )

        return res

    @classmethod
    def get_history_names_by_li(mcs, li):
        url = noexcept(lambda: re.search(Etigoya.url_pattern, str(li)).group(0))
        if not url:
            return []
        html = requests.get(url, proxies=proxy).text
        names = [
            re.sub(Etigoya.purify_pattern, "", s).strip()
            for s in re.findall(Etigoya.name_pattern, html)
        ]
        return names

    @classmethod
    def test(mcs):
        mcs.test_history_names("水野あき")


if __name__ == "__main__":
    Etigoya.test()
