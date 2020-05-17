import requests
import bs4
from JavPy.functions.datastructure import Brief
import re
from JavPy.utils.common import noexcept
from JavPy.sources.BaseSource import IGetBrief
from JavPy.utils.config import proxy


class AVSoxNet(IGetBrief):
    __url_pattern = re.compile('movie-box.+?href="(.+?)"')
    __release_date_pattern = re.compile("发行时间:</span> (.+?)</p>")

    @classmethod
    def get_brief(mcs, code):
        url = "https://avsox.host/cn/search/" + code
        rsp = requests.get(url, proxies=proxy)
        html = rsp.text

        match = re.search(mcs.__url_pattern, html)
        if not match:
            return None
        url = match.group(1)
        rsp = requests.get(url, proxies=proxy)
        html = rsp.text

        bs = bs4.BeautifulSoup(html, "lxml")
        movie = bs.select(".movie")[0]

        brief = Brief()
        brief.code = code
        img = movie.select(".screencap", limit=1)[0].a.img
        brief.title = img.attrs["title"]

        brief.release_date = noexcept(
            lambda: re.search(mcs.__release_date_pattern, str(movie)).group(1), ""
        )

        brief.actress = ", ".join(
            x.text for x in bs.select("#avatar-waterfall", limit=1)[0].find_all("span")
        )

        rsp = requests.get(img.attrs["src"], proxies=proxy)
        if 300 <= rsp.status_code <= 400:
            if "location" in rsp.headers:
                brief.preview_img_url = rsp.headers["location"]
        elif rsp.status_code == 200:
            brief.preview_img_url = img.attrs["src"]

        return brief

    @classmethod
    def test(mcs):
        mcs.test_get_brief("123118_790")


if __name__ == "__main__":
    # AVSoxNet.test()
    print(AVSoxNet.get_brief("ARM-868").to_dict())