from JavPy.sources.BaseSource import ISearchByCode
import bs4
from JavPy.functions.datastructure import AV
from JavPy.utils.config import proxy
import cloudscraper


class JavFullNet(ISearchByCode):
    __client = cloudscraper.create_scraper()

    @classmethod
    def search_by_code(mcs, code):
        url = "https://javfull.net/?s=" + code
        html = mcs.__client.get(url, proxies=proxy).text
        bs = bs4.BeautifulSoup(html, "lxml")
        item = bs.select(".item")[0]

        av = AV()
        av.code = code
        av.preview_img_url = item.find(name="img").attrs["src"]
        av.video_url = item.find(name="a").attrs["href"]

        return av

    @classmethod
    def test(mcs):
        mcs.test_search_by_code("n1056")


if __name__ == "__main__":
    JavFullNet.test()
