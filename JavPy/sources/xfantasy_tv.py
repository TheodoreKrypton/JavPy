from JavPy.sources.BaseSource import ISearchByCode
import requests
import bs4
from JavPy.utils.config import proxy
from JavPy.functions.datastructure import AV


class XFantasyTV(ISearchByCode):
    @classmethod
    def search_by_code(mcs, code):
        url = "https://xfantasy.tv/search/" + code
        rsp = requests.get(url, proxies=proxy)
        html = rsp.text
        bs = bs4.BeautifulSoup(html, "lxml")
        card = bs.select(".MuiGrid-item")
        if not card:
            return None
        card = card[0].a
        title = card.text
        if code in title:
            av = AV()
            av.code = code
            av.preview_img_url = card.img.attrs['src']
            av.video_url = "https://xfantasy.tv" + card.attrs["href"]
            return av
        return None

    @classmethod
    def test(mcs):
        XFantasyTV.test_search_by_code("n0753")


if __name__ == "__main__":
    XFantasyTV.test()
