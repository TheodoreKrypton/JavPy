from JavPy.utils.requester import submit, wait_for_all
from JavPy.functions.sources import Sources
from JavPy.utils.common import conclude


class Brief:
    @staticmethod
    def get_brief(code):
        return conclude(wait_for_all([submit(source.get_brief, code) for source in Sources.Brief]))


if __name__ == '__main__':
    print(Brief.get_brief("YST-217").to_dict())
