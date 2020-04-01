from JavPy.functions.sources import Sources
import datetime
from typing import List
from functools import reduce

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
            if not len(cls.newly_released) >= which_page:
                cls.newly_released += [None] * (which_page - len(cls.newly_released))
            if not cls.newly_released[which_page - 1]:
                cls.newly_released[which_page - 1] = cls.__get_newly_released_from_sources(which_page)
            return cls.newly_released[which_page - 1]

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
                    cls.newly_released[page_cnt] = cls.__get_newly_released_from_sources(page_cnt + 1)
                lack -= len(cls.newly_released[page_cnt])
                page_cnt += 1

            return reduce(lambda x, y: x + y, cls.newly_released[:page_cnt])[:up_to]

    which_source = -1

    @classmethod
    def __find_usable_source(cls, page):
        cls.which_source = 0
        for i, source in enumerate(Sources.NewlyReleased):
            try:
                res = Sources.NewlyReleased[cls.which_source].get_newly_released(page)
                if not res:
                    continue
                else:
                    cls.which_source = i
                    return res
            except Exception:
                continue
        raise Exception("all sources are down")

    @classmethod
    def __get_newly_released_from_sources(cls, page):
        if cls.which_source != -1:
            try:
                res = Sources.NewlyReleased[cls.which_source].get_newly_released(page)
                if not res:
                    return cls.__find_usable_source(page)
                else:
                    return res
            except Exception:
                return cls.__find_usable_source(page)
        else:
            return cls.__find_usable_source(page)

    @classmethod
    def __merge_results(cls, results):
        pass


if __name__ == "__main__":
    print(New.get_newly_released(30, 2))
