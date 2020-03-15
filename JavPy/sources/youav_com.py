from JavPy.sources.BaseSource import ISearchByCode
import requests
import bs4
from JavPy.functions.datastructure import AV
from JavPy.utils.config import proxy
from JavPy.embed.youav_com import youav_com


class YouAVCom(ISearchByCode):
    @classmethod
    def search_by_code(mcs, code):
        url = "https://www.youav.com/search/videos/" + code
        response = requests.get(url, proxies=proxy)
        bs = bs4.BeautifulSoup(response.text, "lxml")

        try:
            divs = bs.find_all(name="div", attrs={"class": "content-row"})[-1].find_all(name='div')
            if not divs:
                return None
            div = divs[0]
            img = div.find(name='img').attrs['src']

        except (AttributeError, IndexError):
            return None

        url = "https://www.youav.com" + div.a.attrs["href"]
        url = youav_com.decode(url)

        av = AV()
        av.code = code
        av.video_url = url
        av.preview_img_url = img

        return av

    @classmethod
    def test(mcs):
        mcs.test_search_by_code("SSNI-351")


if __name__ == '__main__':
    YouAVCom.test()
