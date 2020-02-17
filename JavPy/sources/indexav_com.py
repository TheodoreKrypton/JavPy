import requests
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief
import bs4
from JavPy.functions.datastructure import Brief
from JavPy.utils.common import try_evaluate
from JavPy.utils.config import proxy


class IndexAVCom(ISearchByActress, IGetBrief):
    @classmethod
    def search_by_actress(cls, actress, up_to):
        url = "https://indexav.com/actor/" + actress
        rsp = requests.get(url, verify=False, proxies=proxy)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        cards = bs.select(".card")[:-1]

        res = []

        cnt = 0

        for card in cards:
            brief = cls.__get_brief_by_card(card)
            if brief:
                res.append(brief)
                cnt += 1

            if up_to and cnt >= up_to:
                return res
        return res

    @classmethod
    def get_brief(cls, code):
        url = "https://indexav.com/search?keyword=" + code
        rsp = requests.get(url, verify=False, proxies=proxy)

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
        if not columns:  # like 飯岡かなこ
            return None
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
        brief.release_date = release_date
        return brief

    @classmethod
    def test(cls):
        cls.test_get_brief("JUY-805")
        cls.test_search_by_actress("飯岡かなこ", None)


if __name__ == "__main__":
    IndexAVCom.test()
