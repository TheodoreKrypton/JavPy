from __future__ import absolute_import, print_function, unicode_literals


from functions.search import Search
from functions.new import New
from functions.brief import Brief as GetBrief
from functions.datastructure import AV, Brief
from functions.magnet import Magnet
import gevent


class Functions:
    def __init__(self):
        pass

    search_service = Search()

    @classmethod
    def search_by_code(cls, code):
        av = gevent.spawn(cls.search_service.search_by_code, code)
        _brief = gevent.spawn(cls.get_brief, code)

        av.join()
        _brief.join()

        if av.value:
            res = av.value
            if _brief.value:
                res.actress = _brief.value.actress if _brief.value.actress else ""
            return res
        else:
            return None

    @classmethod
    def search_by_actress(cls, actress, allow_many_actresses, up_to):
        return cls.search_service.search_by_actress(actress, allow_many_actresses, up_to)

    @staticmethod
    def get_newly_released(allow_many_actresses, up_to):
        return New.get_newly_released(allow_many_actresses, up_to)

    @staticmethod
    def get_brief(code):
        return GetBrief.get_brief(code)

    @staticmethod
    def get_magnet(code):
        return Magnet.get_magnet(code)
