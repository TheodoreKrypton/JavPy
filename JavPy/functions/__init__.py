from __future__ import absolute_import, print_function, unicode_literals
from JavPy.functions.search_by_code import SearchByCode
from JavPy.functions.search_by_actress import SearchByActress
from JavPy.functions.new import New
from JavPy.functions.brief import Brief as GetBrief
from JavPy.functions.datastructure import AV, Brief
from JavPy.functions.magnet import Magnet
from JavPy.functions.history_names import HistoryNames
from JavPy.functions.actress_info import ActressInfo
from JavPy.utils.common import cache
from JavPy.utils.requester import spawn_many, Task, spawn
import os
import json


class Functions:
    @staticmethod
    @cache
    def search_by_code(code):
        av, brief_info = spawn_many(
            (Task(SearchByCode.search, code), Task(Functions.get_brief, code))
        ).wait_for_all_finished()
        if av:
            res = av
            if brief_info:
                res.actress = brief_info.actress if brief_info.actress else ""
                res.set_release_date(brief_info.release_date)
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
    def search_by_actress(actress, up_to, history_name=False):
        return SearchByActress.search(actress, up_to, history_name)

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
        return spawn(Magnet.get_magnet, code).wait_for_result()

    @staticmethod
    @cache
    def translate2jp(actress):
        return

    tags = None

    @staticmethod
    @cache
    def get_tags():
        if not Functions.tags:
            curdir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
            with open(curdir + "/../sources/categories.json") as fp:
                content = fp.read()
                obj = json.loads(content)
                Functions.tags = obj["javmost"]
        return Functions.tags

    @staticmethod
    @cache
    def get_actress_info(actress):
        return ActressInfo.get_actress_info(actress)



