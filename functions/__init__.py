from __future__ import absolute_import, print_function, unicode_literals
from functions.search import Search
from functions.new import New
from functions.brief import Brief as GetBrief
from functions.datastructure import AV, Brief
from functions.magnet import Magnet
from functions.history_names import HistoryNames
from utils.common import cache
from utils.requester import spawn_many, Task


class Functions:
    search_service = Search()

    @staticmethod
    @cache
    def search_by_code(code):
        av, brief_info = spawn_many((
            Task(Functions.search_service.search_by_code, code),
            Task(Functions.get_brief, code)
        )).wait_for_all_finished()
        if av:
            res = av
            if brief_info:
                res.actress = brief_info.actress if brief_info.actress else ""
                res.release_date = brief_info.release_date
                res.title = brief_info.title
            return res
        else:
            return None

    @staticmethod
    def search_history_names(actress):
        return HistoryNames.get_history_names(actress)

    @staticmethod
    def search_by_actress(actress, up_to):
        return Functions.search_service.search_by_actress(actress, up_to)

    @staticmethod
    def get_newly_released(up_to, which_page=False):
        return New.get_newly_released(up_to, which_page)

    @staticmethod
    @cache
    def get_brief(code):
        return GetBrief.get_brief(code)

    @staticmethod
    @cache
    def get_magnet(code):
        return Magnet.get_magnet(code)
