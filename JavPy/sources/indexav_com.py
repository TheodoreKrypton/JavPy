import requests
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief
import bs4
from JavPy.functions.datastructure import Brief
from JavPy.utils.common import noexcept
from JavPy.utils.config import proxy
from JavPy.utils.requester import submit, wait_for_all
from functools import reduce


class IndexAVCom(ISearchByActress, IGetBrief):
    @classmethod
    def search_by_actress(mcs, actress, up_to):
        url = "https://indexav.com/actor/" + actress
        rsp = requests.get(url, verify=False, proxies=proxy)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        ul = bs.select(".pagination-list")
        if len(ul) == 0:
            return mcs.__search_by_actress_in_page(actress, 1)
        else:
            return reduce(
                lambda x1, x2: x1 + x2,
                filter(
                    lambda x: x,
                    wait_for_all(
                        [
                            submit(
                                mcs.__search_by_actress_in_page,
                                actress,
                                int(page.text.strip()),
                            )
                            for page in ul[0].find_all("li")
                        ]
                    ),
                ),
            )

    @classmethod
    def __search_by_actress_in_page(mcs, actress, n):
        url = "https://indexav.com/actor/{}?page={}".format(actress, n)
        rsp = requests.get(url, verify=False, proxies=proxy)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        cards = bs.select(".video_column")

        res = []
        for card in cards:
            brief = mcs.__get_brief_from_card(card)
            if brief:
                res.append(brief)
        return res

    @classmethod
    def get_brief(mcs, code):
        url = "https://indexav.com/search?keyword=" + code
        rsp = requests.get(url, proxies=proxy)

        if rsp.status_code != 200:
            return None

        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        cards = bs.select(".card")
        if not cards:
            return None
        if "Sad, cannot find any video in database" in cards[0].text:
            return None
        return mcs.__get_brief_from_card(cards[0])

    @staticmethod
    def __get_brief_from_card(card):
        code = card.select(".tag.is-link.is-light")[0].text.strip()
        actress = ", ".join(
            (x.text.strip() for x in card.select(".tag.is-primary.is-light"))
        )
        h5 = card.select(".title")[0]
        title = h5.text.strip()
        img = noexcept(lambda: h5.a.attrs["rel"][0])
        release_date = card.select("footer")[0].p.text.strip()

        brief = Brief()
        brief.title = title
        brief.preview_img_url = img
        brief.code = code
        brief.actress = actress
        brief.release_date = release_date
        return brief

    @classmethod
    def test(mcs):
        mcs.test_get_brief("JUY-805")
        mcs.test_search_by_actress("飯岡かなこ", None)


if __name__ == "__main__":
    # IndexAVCom.test()
    # print(IndexAVCom.get_brief("YMDD-192").to_dict())
    print(IndexAVCom.search_by_actress("波多野結衣", up_to=None))
