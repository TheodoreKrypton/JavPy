from sources.javmost_com import JavMostCom
from sources.youav_com import YouAVCom
from sources.xopenload_video import XOpenloadVideo
from sources.indexav_com import IndexAVCom


class Search:
    def __init__(self):
        self.sources_by_code = [XOpenloadVideo, JavMostCom, YouAVCom]
        self.sources_by_actress = {
            "indexav.com": IndexAVCom
        }

    def search_by_code(self, code):
        for src in self.sources_by_code:
            res = src.search_by_code(code)
            if res:
                return res
        return None


    @staticmethod
    def guess_lang(text):
        if isinstance(text, str):
            text = text.decode("utf-8")

        if all(map(lambda c: ord(c) < 128, text)):
            lang = "en"

        else:
            if any(map(lambda c: 0x0800 <= ord(c) <= 0x4e00, text)):
                lang = "jp"
            else:
                lang = "zh"

        return lang

    def search_by_actress(self, actress, allow_many_actresses, up_to):
        lang = self.guess_lang(actress)

        if lang == "jp":
            return self.sources_by_actress["indexav.com"].search_by_actress(actress, allow_many_actresses, up_to)

        else:
            return None