# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import map
import requests
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief
import bs4
from JavPy.functions.datastructure import Brief
from JavPy.utils.common import try_evaluate


class IndexAVCom(ISearchByActress, IGetBrief):
    @classmethod
    def search_by_actress(cls, actress, up_to):
        url = "https://indexav.com/actor/" + actress
        rsp = requests.get(url, verify=False)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        cards = bs.select(".card")[:-1]

        res = []

        cnt = 0

        for card in cards:
            brief = cls.__get_brief_by_card(card)
            res.append(brief)
            cnt += 1

            if up_to and cnt >= up_to:
                return res
        return res

    @classmethod
    def get_brief(cls, code):
        url = "https://indexav.com/search?keyword=" + code
        rsp = requests.get(url, verify=False)

        if rsp.status_code != 200:
            return None

        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        cards = bs.select(".card")
        if not cards:
            return None
        if "Sad, cannot find any video in database" in cards[0].text:
            return None
        return cls.__get_brief_by_card(cards[0])

    @staticmethod
    def __get_brief_by_card(card):
        columns = card.select(".column")
        code = columns[4].next.strip()
        actress = ", ".join((x.text.strip() for x in columns[2].find_all(name="span")))
        title = columns[3].text.strip()
        img, _ = try_evaluate(lambda: columns[3].a.attrs["rel"][0])
        release_date = columns[1].text.strip()

        brief = Brief()
        brief.title = title
        brief.preview_img_url = img
        brief.code = code
        brief.actress = actress
        brief.set_release_date(release_date)
        return brief


if __name__ == "__main__":
    # print(try_evaluate(lambda: IndexAVCom.get_brief("JUY-805")))
    print(IndexAVCom.search_by_actress("神宮寺ナオ", None))
    # print(IndexAVCom.search_by_actress("深田えいみ", 30)[0].to_dict())
