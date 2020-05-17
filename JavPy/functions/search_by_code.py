from JavPy.functions.sources import Sources
from JavPy.utils.requester import submit, wait_until
from JavPy.functions.datastructure import AV


class SearchByCode:
    @classmethod
    def search(cls, code) -> AV:
        return wait_until(
            [submit(x.search_by_code, code) for x in Sources.SearchByCode],
            condition=lambda x: x.video_url
        )


if __name__ == "__main__":
    # print(Search.search_by_code("DFE-023").to_dict())
    # print(Search.search_by_actress("原更紗", 30))
    print(SearchByCode.search("SSNI-790").to_dict())
