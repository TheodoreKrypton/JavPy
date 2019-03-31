from sources.indexav_com import IndexAVCom
from sources.avsox_net import AVSoxNet
from functions.datastructure import Brief as BriefInfo
from utils.common import update_object


class Brief:
    sources = [IndexAVCom, AVSoxNet]

    @staticmethod
    def get_brief(code):
        res = BriefInfo()
        i = 0
        while not res.preview_img_url:
            temp = Brief.sources[i].get_brief(code)
            if temp:
                update_object(res, temp)
            i += 1
        return res
