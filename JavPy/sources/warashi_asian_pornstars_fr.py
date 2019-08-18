# encoding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief, ITranslateEn2Jp, IActressInfo
import requests
import bs4


class WarashiAsianPornStarsFr(ISearchByActress, IGetBrief, ITranslateEn2Jp, IActressInfo):
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

        actress_lower = actress.lower()

        box = bs.select("#bloc-resultats-conteneur-pornostars", limit=1)[0].find(attrs={'class': 'resultat-pornostar'})
        if actress_lower in box.find(name='p').text.lower():
            url = "http://warashi-asian-pornstars.fr" + box.a.attrs['href']
            rsp = requests.get(url)
            bs = bs4.BeautifulSoup(rsp.text, "lxml")
            names = [elem.text.lower() for elem in
                     bs.find_all(name='span', attrs={'itemprop': 'name'}) +
                     bs.find_all(attrs={'itemprop': 'additionalName'})]
            if actress_lower not in names:
                return None
            return bs.find('h1').text.split(' - ')[1]

        else:
            box = bs.select("#bloc-resultats-conteneur-castings", limit=1)[0].find(attrs={'class': 'resultat-pornostar'})
            title = box.find(name='p').text.lower()
            if actress_lower in title:
                name = title.split("-")[1].strip()
                if name:
                    return name
            return None

    @classmethod
    def get_actress_info(cls, actress):
        pass


if __name__ == '__main__':
    print(WarashiAsianPornStarsFr.translate2jp(u'Riana Yuzuki'))
