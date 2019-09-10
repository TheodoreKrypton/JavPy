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
    def check_name_in_box(cls, name, box):
        title = box.find(name='p').text.lower()
        if name in title:
            name = title.split("-")[1].strip()
            if name:
                return name
        return None

    @classmethod
    def translate2jp(cls, actress):
        rsp = requests.post("http://warashi-asian-pornstars.fr/en/s-12/search", {
            'recherche_critere': 'f',
            'recherche_valeur': actress
        })
        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        actress_lower = actress.lower()

        box = bs.select("#bloc-resultats-conteneur-pornostars", limit=1)[0].find(attrs={'class': 'resultat-pornostar'})
        name = cls.check_name_in_box(actress_lower, box)
        if name:
            return name
        box = bs.select("#bloc-resultats-conteneur-castings", limit=1)[0].find(attrs={'class': 'resultat-pornostar'})
        return cls.check_name_in_box(actress_lower, box)

    @classmethod
    def get_actress_info(cls, actress):
        pass


if __name__ == '__main__':
    print(WarashiAsianPornStarsFr.translate2jp(u'Riana Yuzuki'))
