# encoding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
from JavPy.sources.BaseSource import ISearchByActress, IGetBrief, ITranslateEn2Jp, IActressInfo, IHistoryNames
from JavPy.functions.datastructure import Actress
import requests
import bs4
from JavPy.utils.common import cache


class WarashiAsianPornStarsFr(ISearchByActress, IGetBrief, ITranslateEn2Jp, IActressInfo, IHistoryNames):
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
    def parse_detail_page(cls, url):
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        actress_info = Actress()

        # get image
        image = bs.select("#pornostar-profil-photos")
        if image:
            image = image[0]
            actress_info.img = "http://warashi-asian-pornstars.fr/" + image.find(name="img").attrs['src']

        info_field = bs.select("#pornostar-profil-infos")[0]

        # get history names
        history_names = set()

        h1 = bs.find(name='h1')[0]
        main_name = h1.find_all(name='span')[1].text
        history_names.add(main_name)

        also_known_as = info_field.select("#pornostar-profil-noms-alternatifs")
        if also_known_as:
            names = also_known_as.find_all(name="li")
            history_names.update((name.find_all(name="span")[1].text for name in names))

        actress_info.history_names = list(history_names)

        # get other info
        ps = info_field.find_all(name='p')
        for p in ps:
            print(p)



    @classmethod
    def get_actress_info(cls, actress):

        pass


if __name__ == '__main__':
    # print(WarashiAsianPornStarsFr.translate2jp(u'Riana Yuzuki'))
    print(WarashiAsianPornStarsFr.get_actress_info("Eimi Fukada"))
