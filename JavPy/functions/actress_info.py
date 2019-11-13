from __future__ import absolute_import, print_function, unicode_literals
from JavPy.functions.sources import Sources
from JavPy.utils.requester import spawn_many, Task


class ActressInfo:
    @staticmethod
    def get_actress_info(actress):
        return spawn_many(
            (Task(source.get_actress_info, actress) for source in Sources.ActressInfo)
        ).wait_for_one_finished()[0]


if __name__ == "__main__":
    print(ActressInfo.get_actress_info("Eimi Fukada")[0].to_dict())
