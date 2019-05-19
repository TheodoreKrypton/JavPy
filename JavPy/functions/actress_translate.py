# encoding: utf-8

from JavPy.sources.javmodel_com import JavModelCom
from JavPy.sources.warashi_asian_pornstars_fr import WarashiAsianPornStarsFr
from JavPy.utils.requester import spawn_many, Task
from future.builtins import filter


class ActressTranslate:
    sources_en2jp = [JavModelCom, WarashiAsianPornStarsFr]

    @staticmethod
    def translate2jp(actress):
        return list(filter(lambda x: x, spawn_many(
            [Task(source.translate2jp, actress) for source in ActressTranslate.sources_en2jp]
        ).wait_for_one_finished()))[0]


if __name__ == '__main__':
    print(ActressTranslate.translate2jp('Arina Hashimoto'))