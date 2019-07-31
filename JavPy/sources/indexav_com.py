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
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        tbody = bs.find(name='tbody')
        trs = tbody.find_all(name='tr')

        res = []

        cnt = 0

        for tr in trs:
            brief = cls.__get_brief_by_tr(tr)
            res.append(brief)
            cnt += 1

            if up_to and cnt >= up_to:
                return res
        return res

    @classmethod
    def get_brief(cls, code):
        url = "https://indexav.com/search?keyword=" + code
        rsp = requests.get(url)

        if rsp.status_code != 200:
            return None

        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        tbody = bs.find(name='tbody')
        if not tbody:
            return None
        tr = tbody.find(name='tr')
        if not tr:
            return None
        return cls.__get_brief_by_tr(tr)

    @staticmethod
    def __get_brief_by_tr(tr):
        code = tr.find(name='span', attrs={'class': 'video_id'}).text
        actress = ", ".join((x.text for x in tr.select(".video_actor")))
        a = tr.find(name='a', attrs={'class': 'video_title'})
        title = a.text
        img, _ = try_evaluate(lambda: a.attrs['rel'])
        release_date = tr.td.text

        brief = Brief()
        brief.title = title.strip()
        brief.preview_img_url = img
        brief.code = code.strip()
        brief.actress = actress.strip()
        brief.set_release_date(release_date)
        return brief


if __name__ == '__main__':
    print(try_evaluate(lambda: IndexAVCom.get_brief("JUY-805")))
    print(IndexAVCom.search_by_actress("深田えいみ", 30))
