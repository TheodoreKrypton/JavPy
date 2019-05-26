from JavPy.sources.BaseSource import ISearchByCode
import requests
import bs4
from JavPy.functions.datastructure import AV


class JavFullNet(ISearchByCode):
    @classmethod
    def search_by_code(cls, code):
        url = "https://javfull.net/?s=" + code
        html = requests.get(url).text
        bs = bs4.BeautifulSoup(html, "lxml")
        item = bs.select(".item")[0]

        av = AV()
        av.code = code
        av.preview_img_url = item.find(name="img").attrs['src']
        av.video_url = item.find(name="a").attrs['href']

        return av


if __name__ == '__main__':
    print(JavFullNet.search_by_code("n1056").to_dict())