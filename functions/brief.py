from sources.indexav_com import IndexAVCom


class Brief:
    def __init__(self):
        pass

    @staticmethod
    def get_brief(code):
        return IndexAVCom.get_brief(code)
