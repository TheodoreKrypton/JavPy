from JavPy.sources.BaseSource import ISearchByCode, INewlyReleased
import re
import bs4
import json
from JavPy.embed import decode
from JavPy.functions.datastructure import AV, Brief
from JavPy.utils.common import noexcept
import datetime
import cloudscraper
from JavPy.utils.config import proxy
from urllib.parse import urlencode, quote_plus
from JavPy.utils.requester import submit, wait_until
import requests


class JavMostCom(ISearchByCode, INewlyReleased):
    __client = cloudscraper.create_scraper()

    @classmethod
    def priority(mcs):
        return 0

    @classmethod
    def __try_one_button(mcs, button, value, main_rsp):
        params = re.search(
            r"select_part\((.+?)\)", button.a.attrs["onclick"]
        ).group(1)
        tokens = params.split(",")
        group = tokens[1].replace("'", "")
        part = tokens[0].replace("'", "")
        _code = tokens[4].replace("'", "")
        code2 = tokens[5].replace("'", "")
        code3 = tokens[6].replace("'", "")
        sound = re.search("'sound':'(.+?)'", main_rsp.text).group(1)

        data = urlencode({
            'group': group,
            'part': part,
            'code': _code,
            'code2': code2,
            'code3': code3,
            'value': value,
            'sound': sound
        }, quote_via=quote_plus)

        rsp = mcs.__client.post(
            "https://www5.javmost.com/get_movie_source/",
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            data=data,
            proxies=proxy
        )

        json_obj = json.loads(rsp.text)
        url = json_obj["data"][0].strip()
        url = decode(url)
        if not url:
            return None

        if "avgle" in "url":
            if "This video is not available on this platform." in requests.get(url).text:
                return None

        if url.endswith(".m3u8") or url.endswith(".mp4"):
            return url

        if requests.head(url).status_code == 200:
            return url

        return None

    @classmethod
    def search_by_code(mcs, code):
        url = "http://www5.javmost.com/" + code + "/"
        main_rsp = mcs.__client.get(url, proxies=proxy)
        if main_rsp.status_code != 200:
            return None

        img = noexcept(
            lambda: re.search(
                r"<meta property=\"og:image\" content=\"(.+?)\"", main_rsp.text
            ).group(1)
        )

        if not img:
            return None

        # Nov. 13 adding: https://www5.javmost.com/IENE-623/
        if not img.startswith("http:"):
            img = "http:" + img

        bs = bs4.BeautifulSoup(main_rsp.text, "lxml")

        buttons = bs.select(".tab-overflow")[0].find_all(name="li")[1:-1]

        var_value = re.search("'value':(.+?),", main_rsp.text).group(1)
        value = re.search("var %s = '(.+?)'" % var_value, main_rsp.text).group(1)

        url = wait_until([submit(mcs.__try_one_button, button, value, main_rsp) for button in buttons])

        if not url:
            return None

        av = AV()
        av.preview_img_url = img
        av.video_url = url
        av.code = code

        return av

    @staticmethod
    def get_cards_from_newly_released_page(page):
        url = "http://www5.javmost.com/showlist/new/" + str(page) + "/release"
        rsp = JavMostCom.__client.get(url, proxies=proxy)

        json_obj = json.loads(rsp.text)
        html = json_obj["data"]

        bs = bs4.BeautifulSoup(html, "lxml")
        cards = bs.find_all(name="div", attrs={"class": "card"})

        return cards

    @staticmethod
    def get_brief_from_a_card(card_tag):
        release_date = noexcept(
            lambda: datetime.datetime.strptime(
                re.search(r"\d\d\d\d-\d\d-\d\d", card_tag.text).group(0), "%Y-%m-%d"
            )
        )

        actress = list(map(
            lambda x: x.text,
            card_tag.find_all(name="a", attrs={"class": "btn-danger"})
        ))

        img = noexcept(lambda: card_tag.find(name="img").attrs["data-src"])
        if not img.startswith("http"):
            img = "http:" + img

        brief = Brief()
        brief.preview_img_url = img
        brief.title = noexcept(lambda: card_tag.find(name="h5").text.strip(), "")
        brief.actress = ", ".join(actress)
        brief.release_date = release_date
        brief.code = card_tag.find(name="h4").text.strip()

        return brief

    @classmethod
    def get_newly_released(mcs, page):
        cards = JavMostCom.get_cards_from_newly_released_page(str(page))
        return list(map(lambda x: JavMostCom.get_brief_from_a_card(x), cards))

    @classmethod
    def test(mcs):
        mcs.test_newly_released()
        mcs.test_search_by_code("SSNI-351")


if __name__ == "__main__":
    # JavMostCom.test()
    print(JavMostCom.search_by_code("ABP-123").to_dict())