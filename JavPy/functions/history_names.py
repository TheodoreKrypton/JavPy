from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.etigoya import Etigoya


class HistoryNames:
    @staticmethod
    def get_history_names(actress):
        return Etigoya.get_history_names(actress)
