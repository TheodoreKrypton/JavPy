from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.etigoya import Etigoya
from JavPy.sources.avhelp_memo_wiki import AVHelpMemoWiki
from JavPy.utils.requester import spawn_many, Task
from functools import reduce
from JavPy.utils.common import cache


class HistoryNames:
    @staticmethod
    @cache
    def get_history_names(actress):
        result = list(filter(lambda x: x, spawn_many((
            Task(Etigoya.get_history_names, actress),
            Task(AVHelpMemoWiki.get_history_names, actress)
        )).wait_for_all_finished()))
        if len(result) == 0:
            return []
        if len(result) == 1:
            return result[0]
        else:
            return list(reduce(lambda x, y: x.union(y), map(lambda z: set(z), result)))
