from __future__ import absolute_import, print_function, unicode_literals
from JavPy.utils.common import sum_up
from JavPy.utils.requester import spawn_many, Task
from JavPy.functions.sources import Sources


class Brief:
    @staticmethod
    def get_brief(code):
        return sum_up(
            spawn_many(
                (Task(source.get_brief, code) for source in Sources.Brief)
            ).wait_until(lambda res: res.preview_img_url)
        )


if __name__ == '__main__':
    print(Brief.get_brief("ABP-123").to_dict())