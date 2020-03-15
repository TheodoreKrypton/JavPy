from JavPy.functions.sources import Sources
from JavPy.utils.requester import spawn_many, Task
from JavPy.utils.common import conclude
from JavPy.functions.datastructure import AV


class SearchByCode:
    @classmethod
    def search(cls, code) -> AV:
        res = spawn_many(
            (Task(source.search_by_code, code) for source in Sources.SearchByCode)
        ).wait_until(lambda x: x.preview_img_url)
        return conclude(res)


if __name__ == "__main__":
    # print(Search.search_by_code("DFE-023").to_dict())
    # print(Search.search_by_actress("原更紗", 30))
    print(SearchByCode.search("CHN-182").video_url)
