from JavPy.utils.requester import submit, wait_for_all
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
                wait_for_all([submit(src.get_history_names, actress)
                              for src in Sources.HistoryNames])
            )
        )
        if len(result) == 0:
            return []
        if len(result) == 1:
            return result[0]
        else:
            return list(reduce(lambda x, y: x.union(y), map(lambda z: set(z), result)))


if __name__ == '__main__':
    print(HistoryNames.get_history_names("夏希のあ"))
