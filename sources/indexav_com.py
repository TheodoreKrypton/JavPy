# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

import requests
from sources.BaseSource import ISearchByActress
import bs4
from functions.datastructure import Brief
from utils.common import try_evaluate


class IndexAVCom(ISearchByActress):
    def __init__(self):
        pass

    @classmethod
    def search_by_actress(cls, actress, allow_many_actresses, up_to):
        url = "https://indexav.com/actor/" + actress
        rsp = requests.get(url, verify=False)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        boxes = bs.find_all(name='div', attrs={'class': 'bs-callout'})

        res = []

        cnt = 0

        for box in boxes:
            release_date = box.find(name='div', attrs={'class': 'col-sm-2'}).span.text
            if u"予定" in release_date:
                continue

            brief = cls.__get_brief_by_box(box)

            if not allow_many_actresses and len(brief.actress.split(", ")) > 1:
                continue

            res.append(brief)
            cnt += 1

            if cnt >= up_to:
                return res

        return res

    @classmethod
    def get_brief(cls, code):
        url = "https://indexav.com/search?keyword=" + code
        rsp = requests.get(url, verify=False)

        if rsp.status_code != 200:
            return None

        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        box = bs.find(name='div', attrs={'class': 'bs-callout'})
        return cls.__get_brief_by_box(box)

    @staticmethod
    def __get_brief_by_box(box):
        code = box.find(name='span', attrs={'class': 'video_id'}).text
        div = box.find(name='div', attrs={'class': 'col-sm-7'})
        actress = ", ".join(map(lambda x: x.text, div.find_all(name='div', attrs={'class': 'col-xs-6'})))
        title = div.find(name='span', attrs={'class': 'video_title'}).text
        img = try_evaluate(lambda: div.find(name='span', attrs={'class': 'preview_btn'}).attrs['rel'])

        brief = Brief()
        brief.title = title
        brief.preview_img_url = img
        brief.code = code
        brief.actress = actress

        return brief
