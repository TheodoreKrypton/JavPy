from sources.indexav_com import IndexAVCom
from sources.avsox_net import AVSoxNet
from utils.common import sum_up
from utils.requester import spawn_many, Task


class Brief:
    sources = [IndexAVCom, AVSoxNet]

    @staticmethod
    def get_brief(code):
        return sum_up(spawn_many(
            (Task(source.get_brief, code) for source in Brief.sources)
        ).wait_until(lambda res: res.preview_img_url))
