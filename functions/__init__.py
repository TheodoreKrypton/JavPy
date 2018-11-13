from search import Search
from datastructure import AV


search_service = Search()

class Functions:
    def __init__(self):
        pass

    @staticmethod
    def search_by_code(code):
        return search_service.search_by_code(code)


    @staticmethod
    def search_by_actress(actress, allow_many_actresses, up_to):
        return search_service.search_by_actress(actress, allow_many_actresses, up_to)