# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from JavPy.utils.requester import spawn_many, Task
from functools import reduce
from JavPy.utils.common import cache
from JavPy.functions.sources import Sources


class HistoryNames:
    @staticmethod
    @cache
    def get_history_names(actress):
        result = list(
            filter(
                lambda x: x,
                spawn_many(
                    (
                        Task(source.get_history_names, actress)
                        for source in Sources.HistoryNames
                    )
                ).wait_for_all_finished(),
            )
        )
        if len(result) == 0:
            return []
        if len(result) == 1:
            return result[0]
        else:
            return list(reduce(lambda x, y: x.union(y), map(lambda z: set(z), result)))


if __name__ == '__main__':
    print(HistoryNames.get_history_names("天海こころ"))
