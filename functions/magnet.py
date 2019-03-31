from sources.javbus_com import JavBusCom


class Magnet:
    @staticmethod
    def get_magnet(code):
        return JavBusCom.search_magnet(code)
