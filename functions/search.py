from sources.javmost_com import JavMostCom
from sources.youav_com import YouAVCom


class Search:
    def __init__(self):
        self.sources = [JavMostCom(), YouAVCom()]


    def search(self, code):
        for src in self.sources:
            res = src.search(code)
            if res:
                return res
        return None