from __future__ import absolute_import, print_function, unicode_literals

from sources.BaseSource import ISearchByCode, SourceException
import requests
import re
import bs4
import json
from embed.decode import decode
from functions.datastructure import AV, Brief
from utils.common import try_evaluate
import datetime


class JavMostCom(ISearchByCode):
    def __init__(self):
        pass

    @classmethod
    def search_by_code(cls, code):
        url = "https://www5.javmost.com/" + code
        rsp = requests.get(url, verify=False)
        if rsp.status_code != 200:
            return None

        img = try_evaluate(lambda: re.search("<meta property=\"og:image\" content=\"(.+?)\"", rsp.text).group(1))

        # Nov. 13 adding: https://www5.javmost.com/IENE-623/
        if not img.startswith("http:"):
            img = "http:" + img

        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        button = bs.find(name='li', attrs={'class': 'active'})
        params = re.search(r"select_part\((.+?)\)", button.a.attrs['onclick']).group(1)
        e, t, a, o, l, r, d = [x.replace("\'", "") for x in params.split(",")]

        data = re.search(r"get_source/\",(.+?)\}", rsp.text, re.S).group(1)
        value = re.search(r"value: \"(.+?)\",", data).group(1)
        sound = re.search(r"sound: \"(.+?)\",", data).group(1)

        url = "https://www5.javmost.com/get_code/"
        rsp = requests.post(url, data={
            "code": value
        }, verify=False)
        _code = rsp.text

        url = "https://www5.javmost.com/get_source/"
        rsp = requests.post(url, data={
            "group": t,
            "part": e,
            "code": l,
            "code2": r,
            "code3": d,
            "value": value,
            "sound": sound,
            "code4": _code
        }, verify=False)

        json_obj = json.loads(rsp.text)
        url = json_obj["data"][0]

        url = decode(url)

        av = AV()
        av.preview_img_url = img
        av.video_url = url
        av.code = code

        return av

    @staticmethod
    def get_newly_released(allow_many_actresses, up_to):
        cnt = 0
        page = 1
        res = []

        while True:
            url = "http://www5.javmost.com/showlist/new/" + str(page) + "/release"
            print(url)
            rsp = requests.get(url)

            json_obj = json.loads(rsp.text)
            html = json_obj["data"]

            bs = bs4.BeautifulSoup(html, "lxml")
            cards = bs.find_all(name='div', attrs={'class': 'card'})

            today = datetime.datetime.today()

            for card in cards:
                release_date = try_evaluate(
                    lambda: datetime.datetime.strptime(
                        re.search("\d\d\d\d-\d\d-\d\d", card.text).group(0), "%Y-%m-%d"
                    )
                )
                if release_date and release_date > today:
                    continue

                actress = list(map(lambda x: x.text, card.find_all(name='a', attrs={'class': 'btn-danger'})))
                if not allow_many_actresses and len(actress) > 1:
                    continue

                img = try_evaluate(lambda: card.find(name='img').attrs['src'])
                if not img.startswith("http:"):
                    img = "http:" + img

                brief = Brief()
                brief.preview_img_url = img
                brief.title = card.find(name='h5').text.strip()
                brief.actress = ", ".join(actress)
                brief.release_date = release_date
                brief.code = card.find(name='h4').text.strip()
                res.append(brief)

                cnt += 1
                if cnt >= up_to:
                    return res

            page += 1
