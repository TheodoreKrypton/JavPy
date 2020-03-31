from JavPy.utils.common import conclude
from JavPy.utils.requester import executor, wait_until
from JavPy.functions.sources import Sources


class Brief:
    @staticmethod
    def get_brief(code):
        return conclude(wait_until(
            [executor.submit(source.get_brief, code) for source in Sources.Brief],
            lambda res: res.preview_img_url
        ))


if __name__ == '__main__':
    print(Brief.get_brief("ABP-123").to_dict())
