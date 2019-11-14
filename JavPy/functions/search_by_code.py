# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from JavPy.functions.sources import Sources
from JavPy.utils.requester import spawn_many, Task
from JavPy.utils.common import sum_up


class SearchByCode:
    @classmethod
    def search(cls, code):
        res = spawn_many(
            (Task(source.search_by_code, code) for source in Sources.SearchByCode)
        ).wait_until(lambda x: x.preview_img_url)
        return sum_up(res)


if __name__ == "__main__":
    # print(Search.search_by_code("DFE-023").to_dict())
    # print(Search.search_by_actress("原更紗", 30))
    print(SearchByCode.search("ABP-123"))
