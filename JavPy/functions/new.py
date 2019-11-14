from __future__ import absolute_import, print_function, unicode_literals
from JavPy.functions.sources import Sources
import datetime

try:
    from typing import List
except ImportError:
    pass
from functools import reduce
from JavPy.utils.common import try_evaluate

Sources.NewlyReleased.sort(key=lambda x: x.priority())


class New:
    newly_released = []  # type: List[List]
    record_date = datetime.datetime.today().date()

    @classmethod
    def get_newly_released(cls, up_to, which_page):
        today = datetime.datetime.today().date()
        if cls.record_date < today:
            cls.record_date = today
            cls.newly_released = []

        if not up_to:
            if not len(cls.newly_released) >= which_page + 1:
                cls.newly_released += [None] * (
                    which_page + 1 - len(cls.newly_released)
                )
            if not cls.newly_released[which_page]:
                cls.newly_released[which_page] = cls.get_newly_released_from_sources(
                    which_page
                )
            return cls.newly_released[which_page]

        else:
            total_len = 0
            page_cnt = 0
            for page in cls.newly_released:
                if not page:
                    break
                total_len += len(page)
                page_cnt += 1

            lack = up_to - total_len
            while lack >= 0:
                if len(cls.newly_released) < page_cnt + 1:
                    cls.newly_released.append([])
                if not cls.newly_released[page_cnt]:
                    cls.newly_released[page_cnt] = cls.get_newly_released_from_sources(
                        which_page
                    )
                lack -= len(cls.newly_released[page_cnt])
                page_cnt += 1

            return reduce(lambda x, y: x + y, cls.newly_released[:page_cnt])[:up_to]

    which_source = 0

    @classmethod
    def get_newly_released_from_sources(cls, page):
        res, ex = try_evaluate(
            lambda: Sources.NewlyReleased[cls.which_source].get_newly_released(page)
        )
        if (not res) or ex:
            cls.which_source += 1
            if cls.which_source == len(Sources.NewlyReleased):
                raise Exception("all sources are down")
            return cls.get_newly_released_from_sources(page)  # fallback choice
        else:
            return res

    @classmethod
    def merge_results(cls, results):
        pass


if __name__ == "__main__":
    print(New.get_newly_released(None, 1))
