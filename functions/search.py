from sources.javmost_com import JavMostCom
from sources.youav_com import YouAVCom
from sources.xopenload_video import XOpenloadVideo
from sources.indexav_com import IndexAVCom
import gevent


class Search:
    def __init__(self):
        self.sources_by_code = [XOpenloadVideo, JavMostCom, YouAVCom]
        self.sources_by_actress = {
            "indexav.com": IndexAVCom
        }

    def search_by_code(self, code):
        gls = []
        for src in self.sources_by_code:
            gls.append(gevent.Greenlet(src.search_by_code, code))
            gls[-1].run()
        res = None
        while True:
            ready_cnt = 0
            for gl in gls:
                if gl.successful():
                    if gl.value is not None:
                        res = gl.value
                        break
                    else:
                        ready_cnt += 1
                elif gl.ready():
                    ready_cnt += 1
            if ready_cnt == len(self.sources_by_code):
                break
            elif res:
                for gl in gls:
                    gl.kill()
                break

        return res

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
