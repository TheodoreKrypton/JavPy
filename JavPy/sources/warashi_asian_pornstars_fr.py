from JavPy.sources.BaseSource import (
    ISearchByActress,
    IGetBrief,
    ITranslateEn2Jp,
    IActressInfo
)
import requests
import bs4
from JavPy.functions.datastructure import Actress, Brief
from JavPy.utils.common import try_evaluate
import datetime
from JavPy.utils.config import proxy


class WarashiAsianPornStarsFr(ITranslateEn2Jp, IActressInfo):
    __actress_detail_url = {}

    @classmethod
    def search_by_actress(mcs, actress, up_to):
        pass

    @classmethod
    def get_brief(mcs, code):
        pass

    @classmethod
    def __check_name_in_box(mcs, name, box):
        if name not in box.text.lower():
            return None
        title = box.find(name="p").text.lower()
        jp_name = title.split("-")[1].strip()
        if not jp_name:
            return None

        # cache for later parsing actress info, None for no url
        url, _ = try_evaluate(lambda: box.a.attrs["href"])
        detail_url = "http://warashi-asian-pornstars.fr/%s" % url
        mcs.__actress_detail_url[name] = detail_url
        mcs.__actress_detail_url[jp_name] = detail_url
        return jp_name

    @classmethod
    def translate2jp(mcs, actress):
        rsp = requests.post(
            "http://warashi-asian-pornstars.fr/en/s-12/search",
            {"recherche_critere": "f", "recherche_valeur": actress},
            proxies=proxy
        )
        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        actress_lower = actress.lower()

        box = bs.select(".bloc-resultats", limit=1)
        if box:
            box = box[0]
            name = mcs.__check_name_in_box(actress_lower, box)
            if name:
                return name

        box = bs.select("#bloc-resultats-conteneur-pornostars", limit=1)[0].find(
            attrs={"class": "resultat-pornostar"}
        )
        name = mcs.__check_name_in_box(actress_lower, box)
        if name:
            return name
        box = bs.select("#bloc-resultats-conteneur-castings", limit=1)[0].find(
            attrs={"class": "resultat-pornostar"}
        )
        name = mcs.__check_name_in_box(actress_lower, box)
        if not name:  # actress not found
            mcs.__actress_detail_url[name] = None
        return name

    @classmethod
    def __parse_detail_page(mcs, url):
        rsp = requests.get(url, proxies=proxy)
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
    def get_actress_info(mcs, actress):
        actress = actress.lower()
        if actress not in mcs.__actress_detail_url:
            mcs.translate2jp(actress)
        if mcs.__actress_detail_url[actress] is None:
            return None
        return mcs.__parse_detail_page(mcs.__actress_detail_url[actress])

    @classmethod
    def test(mcs):
        mcs.test_actress_info("Riana Yuzuki")
        mcs.test_translate_en2jp("Eimi Fukada")


if __name__ == "__main__":
    WarashiAsianPornStarsFr.test()
