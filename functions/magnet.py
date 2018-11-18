from sources.javbus_com import JavBusCom


class Magnet:
    def __init__(self):
        pass

    @staticmethod
    def get_magnet(code):
        return JavBusCom.search_magnet(code)
