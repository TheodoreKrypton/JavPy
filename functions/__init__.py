from search import Search
from new import New
from brief import Brief as GetBrief
from datastructure import AV, Brief


class Functions:
    def __init__(self):
        pass

    search_service = Search()

    @classmethod
    def search_by_code(cls, code):
        return cls.search_service.search_by_code(code)

    @classmethod
    def search_by_actress(cls, actress, allow_many_actresses, up_to):
        return cls.search_service.search_by_actress(actress, allow_many_actresses, up_to)

    @staticmethod
    def get_newly_released(allow_many_actresses, up_to):
        return New.get_newly_released(allow_many_actresses, up_to)

    @staticmethod
    def get_brief(code):
        return GetBrief.get_brief(code)