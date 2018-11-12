from sources.javmost_com import JavMostCom
from sources.youav_com import YouAVCom
from sources.xopenload_video import XOpenloadVideo


class Search:
    def __init__(self):
        self.sources = [XOpenloadVideo(), JavMostCom(), YouAVCom()]


    def search(self, code):
        for src in self.sources:
            res = src.search(code)
            if res:
                return res
        return None
# https://www.xopenload.video/links.php?hash=ca310885d86885192cb106cc391e0252d1783d5ca5550e14688a36b864e9b51d