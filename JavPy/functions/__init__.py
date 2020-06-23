from JavPy.functions.search_by_code import SearchByCode
from JavPy.functions.search_by_actress import SearchByActress
from JavPy.functions.new import New
from JavPy.functions.brief import Brief as GetBrief
from JavPy.functions.datastructure import AV, Brief
from JavPy.functions.magnet import Magnet
from JavPy.functions.history_names import HistoryNames
from JavPy.functions.actress_info import ActressInfo
from JavPy.utils.requester import submit, wait_for_all
import os
import json
from JavPy.utils.common import cache
from functools import lru_cache

LRU_CACHE_MAX_SIZE = None


sources = {
    
}


class Functions:
    @staticmethod
    @cache
    def search_by_code(code):
        av = submit(SearchByCode.search, code)
        brief_info = submit(Functions.get_brief, code)

        av = av.result()
        if av:
            res = av
            brief_info = brief_info.result()
            if brief_info:
                res.actress = brief_info.actress if brief_info.actress else ""
                res.release_date = brief_info.release_date
                res.title = brief_info.title
                res.preview_img_url = (
                    brief_info.preview_img_url if brief_info.preview_img_url else ""
                )
            return res
        else:
            return None

    @staticmethod
    @cache
    def search_history_names(actress):
        return HistoryNames.get_history_names(actress)

    @staticmethod
    @cache
    def search_by_actress(actress, up_to, with_profile=False):
        return SearchByActress.search(actress, up_to, with_profile)

    @staticmethod
    @cache
    def get_newly_released(up_to, which_page):
        if which_page:
            return New.get_newly_released(up_to, which_page)
        else:
            return New.get_newly_released(up_to, 0)

    @staticmethod
    @cache
    def get_brief(code):
        return GetBrief.get_brief(code)

    @staticmethod
    @cache
    def get_magnet(code):
        return submit(Magnet.get_magnet, code).result()

    @staticmethod
    @cache
    def translate2jp(actress):
        return

    @staticmethod
    @lru_cache(maxsize=None)
    def get_tags():
        pwd = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
        with open(pwd + "/../sources/categories.json") as fp:
            content = fp.read()
        obj = json.loads(content)
        return obj["javmost"]

    @staticmethod
    @cache
    def get_actress_info(actress):
        return ActressInfo.get_actress_info(actress)


if __name__ == '__main__':
    # print(Functions.search_by_code("SKSK-024").to_dict())
    print(Functions.search_by_actress("川合まゆ", None))