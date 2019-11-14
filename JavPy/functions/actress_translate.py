# encoding: utf-8

from JavPy.utils.requester import spawn_many, Task
from future.builtins import filter
from JavPy.utils.common import cache
from JavPy.functions.sources import Sources


class ActressTranslate:
    @staticmethod
    @cache
    def translate2jp(actress):
        res = list(
            filter(
                lambda x: x,
                spawn_many(
                    [
                        Task(source.translate2jp, actress)
                        for source in Sources.TranslateEn2Jp
                    ]
                ).wait_for_one_finished(),
            )
        )
        if not res:
            return None
        else:
            return res[0]


if __name__ == "__main__":
    print(Sources.TranslateEn2Jp)
    print(ActressTranslate.translate2jp("Eimi Fukada"))
