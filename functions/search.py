from sources.javmost_com import JavMostCom


class Search:
    def __init__(self):
        self.sources = [JavMostCom()]


    def search(self, code):
        for src in self.sources:
            res = src.search(code)
            if res:
                return res