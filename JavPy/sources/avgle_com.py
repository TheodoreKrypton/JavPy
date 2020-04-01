from JavPy.sources.BaseSource import ISearchByCode
import json
from JavPy.functions.datastructure import AV
import requests
from JavPy.utils.config import proxy


class AVGleCom(ISearchByCode):
    @classmethod
    def search_by_code(mcs, code):
        url = "https://api.avgle.com/v1/search/" + code + "/0?limit=1"
        rsp = json.loads(requests.get(url, proxies=proxy).text)
        av = AV()
        av.title = rsp["response"]["videos"][0]["title"]
        av.video_url = rsp["response"]["videos"][0]["video_url"]
        av.code = code
        av.preview_img_url = rsp["response"]["videos"][0]["preview_url"]
        return av

    @classmethod
    def test(mcs):
        super().test_search_by_code("ABP-871")


if __name__ == "__main__":
    # AVGleCom.test()
    print(AVGleCom.search_by_code("SKSK-024").to_dict())