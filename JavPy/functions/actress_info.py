from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.warashi_asian_pornstars_fr import WarashiAsianPornStarsFr
from JavPy.utils.requester import spawn_many, Task


class ActressInfo:
    sources = [WarashiAsianPornStarsFr]

    @staticmethod
    def get_actress_info(actress):
        return spawn_many(
            (Task(source.get_actress_info, actress) for source in ActressInfo.sources)
        ).wait_for_one_finished()
