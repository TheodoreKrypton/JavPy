from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.javbus_com import JavBusCom


class Magnet:
    @staticmethod
    def get_magnet(code):
        return JavBusCom.search_magnet(code)
