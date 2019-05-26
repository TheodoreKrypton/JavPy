from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import map
from JavPy.sources.javmost_com import JavMostCom
from JavPy.sources.youav_com import YouAVCom
from JavPy.sources.avgle_com import AVGleCom
from JavPy.sources.xopenload_video import XOpenloadVideo
from JavPy.sources.javfull_net import JavFullNet
from JavPy.sources.indexav_com import IndexAVCom
from JavPy.utils.requester import spawn, spawn_many, Task
from JavPy.utils.common import sum_up
from JavPy.functions.actress_translate import ActressTranslate
from JavPy.functions.history_names import HistoryNames


class Search:
    sources_by_code = [JavMostCom, XOpenloadVideo, YouAVCom, AVGleCom, JavFullNet]
    sources_by_actress = {
        "indexav.com": IndexAVCom
    }

    @classmethod
    def search_by_code(cls, code):
        res = spawn_many(
            (Task(source.search_by_code, code) for source in cls.sources_by_code)
        ).wait_until(lambda x: x.preview_img_url)
        return sum_up(res)

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

    @classmethod
    def search_by_actress(cls, actress, up_to, history_name=False):
        lang = cls.guess_lang(actress)

        if lang == "en":
            actress = ActressTranslate.translate2jp(actress)
        if actress:
            res = spawn(cls.sources_by_actress["indexav.com"].search_by_actress, actress, up_to)
            if history_name:
                names = spawn(HistoryNames.get_history_names, actress)
                return res.wait_for_result(), names.wait_for_result()
            else:
                return res.wait_for_result(), None


if __name__ == '__main__':
    print(Search.search_by_actress("Arina Hashimoto", 30))
