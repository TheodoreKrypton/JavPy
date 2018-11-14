# encoding: utf-8

import requests
from BaseSource import ISearchByActress
import bs4
from functions.datastructure import Brief
from utils.common import try_evaluate


class IndexAVCom(ISearchByActress):
    def __init__(self):
        pass

    def search_by_actress(self, actress, allow_many_actresses, up_to):
        url = "https://indexav.com/actor/" + actress
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        boxes = bs.find_all(name='div', attrs={'class': 'bs-callout'})

        res = []

        cnt = 0

        for box in boxes:
            code = box.find(name='span', attrs={'class': 'video_id'}).text
            div = box.find(name='div', attrs={'class': 'col-sm-2'})
            release_date = div.span.text
            if u"予定" in release_date:
                continue
            div = box.find(name='div', attrs={'class': 'col-sm-7'})
            actress_cnt = len(div.find_all(name='div', attrs={'class': 'col-xs-6'}))

            if not allow_many_actresses and actress_cnt > 1:
                continue



            title = div.find(name='span', attrs={'class': 'video_title'}).text

            img = try_evaluate(lambda x: div.find(name='span', attrs={'class': 'preview_btn'}).attrs['rel'])

            brief = Brief()
            brief.title = title
            brief.preview_img_url = img
            brief.code = code
            brief.actress = actress

            res.append(brief)
            cnt += 1

            if cnt >= up_to:
                return res

        return res