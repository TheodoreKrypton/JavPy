from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.javmost_com import JavMostCom
from JavPy.sources.javlibrary_com import JavLibraryCom
import datetime
try:
    from typing import List
except ImportError:
    pass
from functools import reduce


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
                cls.newly_released += [None] * (which_page + 1 - len(cls.newly_released))
            if not cls.newly_released[which_page]:
                cls.newly_released[which_page] = cls.get_newly_released_from_sources(which_page)
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
                    cls.newly_released[page_cnt] = cls.get_newly_released_from_sources(which_page)
                lack -= len(cls.newly_released[page_cnt])
                page_cnt += 1

            return reduce(lambda x, y: x + y, cls.newly_released[:page_cnt])[:up_to]

    source = JavMostCom

    @classmethod
    def get_newly_released_from_sources(cls, page):
        try:
            res = cls.source.get_newly_released(page)
            if res:
                return res
        finally:
            cls.source = JavLibraryCom
            return cls.source.get_newly_released(page)  # fallback choice

    @classmethod
    def merge_results(cls, results):
        pass


if __name__ == '__main__':
    print(New.get_newly_released(None, 1))

