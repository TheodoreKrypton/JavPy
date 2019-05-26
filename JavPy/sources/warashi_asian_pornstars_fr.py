# encoding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief, ITranslateEn2Jp
import requests
import bs4


class WarashiAsianPornStarsFr(ISearchByActress, IGetBrief, ITranslateEn2Jp):
    @classmethod
    def search_by_actress(cls, actress, up_to):
        pass

    @classmethod
    def get_brief(cls, code):
        pass

    @classmethod
    def translate2jp(cls, actress):
        rsp = requests.post("http://warashi-asian-pornstars.fr/en/s-12/search", {
            'recherche_critere': 'f',
            'recherche_valeur': actress
        })
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        url = "http://warashi-asian-pornstars.fr" + bs.select(".resultat-pornostar")[0].a.attrs['href']
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        names = [elem.text.lower() for elem in
                 bs.find_all(name='span', attrs={'itemprop': 'name'}) +
                 bs.find_all(attrs={'itemprop': 'additionalName'})]
        if actress.lower() not in names:
            return None
        return bs.find('h1').text.split(' - ')[1]


if __name__ == '__main__':
    print(WarashiAsianPornStarsFr.translate2jp(u'夏目彩春'))
