

from JavPy.sources.BaseSource import IHistoryNames
import requests
from JavPy.utils.common import urlencode
import re
import bs4
from JavPy.utils.config import proxy


class AVHelpMemoWiki(IHistoryNames):
    @classmethod
    def match_history_names(mcs, html):
        bs = bs4.BeautifulSoup(html, "lxml")
        # like 川合まゆ
        table = bs.select("table#content_block_2")
        if table:
            tbody = str(table[0].tbody)
            names = [
                re.sub("（.+?）", "", name)
                for name in re.search("名前.+?<td>(.+?)</td>", tbody, re.S)
                .group(1)
                .split("／")
            ]
            return names

        # like 唯川みさき
        pre = bs.select("pre")
        if not pre:
            # like 原更紗
            content_block_1 = bs.select("#content_block_1")
            if not content_block_1:
                return []
            content_block_1 = content_block_1[0]
            moved_to = re.search('<span.+?href="(.+?)".+?へ移動する', str(content_block_1), re.S)
            moved_to = moved_to.group(1)
            rsp = requests.get(moved_to, proxies=proxy)
            pre = re.search(r"<pre.+?</pre>", rsp.text, re.S).group(0)

        else:
            pre = str(pre[0])

        names_str = re.search("別名.*?：(.*?)\n", pre).group(1)
        names = []
        if names_str:
            # like 原更紗
            names_str = re.sub("[（(].+?[)）]", "／", names_str)
            # ・ like 瀬奈まお,笹倉杏
            names.extend(filter(lambda x: x, re.split("[／・]|&amp;", names_str)))

        current_name = re.search("名前.*?：(.+?)\n", pre)
        if current_name:
            current_name = list(filter(lambda x: x, [
                name.strip() for name in re.split("[（(／)）]", current_name.group(1))
            ]))
            names.extend(current_name)

        return names

    @classmethod
    def get_history_names(mcs, actress):
        names = set()
        names.add(actress)
        url = "https://av-help.memo.wiki/d/" + urlencode(actress, "EUC-JP")
        rsp = requests.get(url, proxies=proxy)
        html = rsp.text
        names.update(mcs.match_history_names(html))
        return list(names)

    @classmethod
    def test(mcs):
        super().test_history_names("唯川みさき")
        super().test_history_names("原更紗")
        super().test_history_names("瀬奈まお")
        super().test_history_names("天海こころ")
        super().test_history_names("笹倉杏")


if __name__ == "__main__":
    # AVHelpMemoWiki.test()
    print(AVHelpMemoWiki.get_history_names("夏希のあ"))