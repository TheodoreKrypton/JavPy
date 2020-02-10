from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import str, map
from JavPy.sources.BaseSource import ISearchByCode, INewlyReleased
import re
import bs4
import json
from JavPy.embed.decode import decode
from JavPy.functions.datastructure import AV, Brief
from JavPy.utils.common import try_evaluate
import datetime
import cloudscraper
from urllib.parse import urlencode, quote_plus


class JavMostCom(ISearchByCode, INewlyReleased):
    __client = cloudscraper.create_scraper()

    @classmethod
    def priority(cls):
        return 0

    @classmethod
    def search_by_code(cls, code):
        url = "http://www5.javmost.com/" + code + "/"
        main_rsp = cls.__client.get(url)
        if main_rsp.status_code != 200:
            return None

        img, _ = try_evaluate(
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
        success = False

        var_value = re.search("'value':(.+?),", main_rsp.text).group(1)
        value = re.search("var %s = '(.+?)'" % var_value, main_rsp.text).group(1)

        for button in buttons:
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

            rsp = cls.__client.post(
                "https://www5.javmost.com/get_movie_source/",
                headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
                data=data
            )

            json_obj = json.loads(rsp.text)
            url = json_obj["data"][0]

            url = decode(url)

            if not url:
                continue

            if cls.__client.get(url).status_code == 200:
                success = True
                break

        if not success:
            return None

        av = AV()
        av.preview_img_url = img
        av.video_url = url
        av.code = code

        return av

    @staticmethod
    def get_cards_from_newly_released_page(page):
        url = "http://www5.javmost.com/showlist/new/" + str(page) + "/release"
        rsp = JavMostCom.__client.get(url)

        json_obj = json.loads(rsp.text)
        html = json_obj["data"]

        bs = bs4.BeautifulSoup(html, "lxml")
        cards = bs.find_all(name="div", attrs={"class": "card"})

        return cards

    @staticmethod
    def get_brief_from_a_card(card_tag):
        release_date, _ = try_evaluate(
            lambda: datetime.datetime.strptime(
                re.search(r"\d\d\d\d-\d\d-\d\d", card_tag.text).group(0), "%Y-%m-%d"
            )
        )

        actress = list(
            map(
                lambda x: x.text,
                card_tag.find_all(name="a", attrs={"class": "btn-danger"}),
            )
        )

        img, _ = try_evaluate(lambda: card_tag.find(name="img").attrs["data-src"])
        if not img.startswith("http"):
            img = "http:" + img

        brief = Brief()
        brief.preview_img_url = img
        brief.title, _ = try_evaluate(lambda: card_tag.find(name="h5").text.strip(), "")
        brief.actress = ", ".join(actress)
        brief.set_release_date(release_date)
        brief.code = card_tag.find(name="h4").text.strip()

        return brief

    @classmethod
    def get_newly_released(cls, page):
        cards = JavMostCom.get_cards_from_newly_released_page(str(page))
        return list(map(lambda x: JavMostCom.get_brief_from_a_card(x), cards))


if __name__ == "__main__":
    # print(JavMostCom.get_newly_released(1))
    print(JavMostCom.search_by_code("SSNI-351").to_dict())