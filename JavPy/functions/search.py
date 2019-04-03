from JavPy.sources.javmost_com import JavMostCom
from JavPy.sources.youav_com import YouAVCom
from JavPy.sources.xopenload_video import XOpenloadVideo
from JavPy.sources.indexav_com import IndexAVCom
from JavPy.utils.requester import spawn_many, Task
from JavPy.utils.common import sum_up


class Search:
    def __init__(self):
        self.sources_by_code = [XOpenloadVideo, JavMostCom, YouAVCom]
        self.sources_by_actress = {
            "indexav.com": IndexAVCom
        }

    def search_by_code(self, code):
        return sum_up(spawn_many(
            (Task(source.search_by_code, code) for source in self.sources_by_code)
        ).wait_until(lambda x: x.preview_img_url))

    @staticmethod
    def guess_lang(text):
        if all(map(lambda c: ord(c) < 128, text)):
            lang = "en"

        else:
            if any(map(lambda c: 0x0800 <= ord(c) <= 0x4e00, text)):
                lang = "jp"
            else:
                lang = "zh"

        return lang

    def search_by_actress(self, actress, up_to):
        lang = self.guess_lang(actress)

        if lang == "jp" or lang == "zh":
            return self.sources_by_actress["indexav.com"].search_by_actress(actress, up_to)

        else:
            return None
