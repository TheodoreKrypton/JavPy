# encoding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
from JavPy.sources.BaseSource import (
    ISearchByActress,
    IGetBrief,
    ITranslateEn2Jp,
    IActressInfo,
    IHistoryNames,
)
import requests
import bs4
from JavPy.functions.datastructure import Actress, Brief
from JavPy.utils.common import try_evaluate
import datetime


class WarashiAsianPornStarsFr(
    ISearchByActress, IGetBrief, ITranslateEn2Jp, IActressInfo, IHistoryNames
):
    __actress_detail_url = {}

    @classmethod
    def search_by_actress(cls, actress, up_to):
        pass

    @classmethod
    def get_brief(cls, code):
        pass

    @classmethod
    def __check_name_in_box(cls, name, box):
        if name not in box.text.lower():
            return None
        title = box.find(name="p").text.lower()
        jp_name = title.split("-")[1].strip()
        if not jp_name:
            return None

        # cache for later parsing actress info, None for no url
        url, _ = try_evaluate(lambda: box.a.attrs["href"])
        detail_url = "http://warashi-asian-pornstars.fr/%s" % url
        cls.__actress_detail_url[name] = detail_url
        cls.__actress_detail_url[jp_name] = detail_url
        return jp_name

    @classmethod
    def translate2jp(cls, actress):
        rsp = requests.post(
            "http://warashi-asian-pornstars.fr/en/s-12/search",
            {"recherche_critere": "f", "recherche_valeur": actress},
        )
        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        actress_lower = actress.lower()

        box = bs.select(".bloc-resultats", limit=1)
        if box:
            box = box[0]
            name = cls.__check_name_in_box(actress_lower, box)
            if name:
                return name

        box = bs.select("#bloc-resultats-conteneur-pornostars", limit=1)[0].find(
            attrs={"class": "resultat-pornostar"}
        )
        name = cls.__check_name_in_box(actress_lower, box)
        if name:
            return name
        box = bs.select("#bloc-resultats-conteneur-castings", limit=1)[0].find(
            attrs={"class": "resultat-pornostar"}
        )
        name = cls.__check_name_in_box(actress_lower, box)
        if not name:  # actress not found
            cls.__actress_detail_url[name] = None
        return name

    @classmethod
    def __parse_detail_page(cls, url):
        rsp = requests.get(url)
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        actress_info = Actress()

        # get image
        image = bs.select("#pornostar-profil-photos")
        if image:
            image = image[0]
            actress_info.img = (
                "http://warashi-asian-pornstars.fr/"
                + image.find(name="img").attrs["src"]
            )

        info_field = bs.select("#pornostar-profil-infos")

        if not info_field:
            return None

        info_field = info_field[0]

        # get history names
        history_names = set()

        h1 = bs.find(name="h1")
        main_name = h1.find_all(name="span")[1].text
        history_names.add(main_name)

        also_known_as = info_field.select("#pornostar-profil-noms-alternatifs")
        if also_known_as:
            also_known_as = also_known_as[0]
            names = also_known_as.find_all(name="li")
            history_names.update((name.find_all(name="span")[1].text for name in names))

        actress_info.history_names = list(history_names)

        # get other info
        ps = info_field.find_all(name="p")
        for p in ps:
            p_str = str(p)
            if "birthdate" in p_str:
                actress_info.birth_date = datetime.datetime.strptime(
                    p.time.attrs["content"], "%Y-%m-%d"
                )
            if "itemprop" in p.attrs:
                if p.attrs["itemprop"] == "height":
                    actress_info.height = p.span.text
                elif p.attrs["itemprop"] == "weight":
                    actress_info.weight = p.span.text

        return actress_info

    @classmethod
    def get_actress_info(cls, actress):
        actress = actress.lower()
        if actress not in cls.__actress_detail_url:
            cls.translate2jp(actress)
        if cls.__actress_detail_url[actress] is None:
            return None
        return cls.__parse_detail_page(cls.__actress_detail_url[actress])


if __name__ == "__main__":
    # print(WarashiAsianPornStarsFr.translate2jp(u'Nao Jinguuji'))
    # print(WarashiAsianPornStarsFr.translate2jp(u'Riana Yuzuki'))
    # print(WarashiAsianPornStarsFr.get_actress_info("Eimi Fukada"))
    print(WarashiAsianPornStarsFr.get_actress_info("Misa Natsuki").to_dict())
