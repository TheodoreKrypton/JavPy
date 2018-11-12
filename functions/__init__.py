from search import Search
from datastructure import AV

_search = Search()

class Functions:
    def __init__(self):
        pass

    @staticmethod
    def search(code):
        return _search.search(code)