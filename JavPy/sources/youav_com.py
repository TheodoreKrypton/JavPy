from __future__ import absolute_import, print_function, unicode_literals
from JavPy.sources.BaseSource import ISearchByCode
import requests
import bs4
from JavPy.functions.datastructure import AV


class YouAVCom(ISearchByCode):
    def __init__(self):
        pass

    @classmethod
    def search_by_code(cls, code):
        url = "https://www.youav.com/search/videos?search_query=" + code

        response = requests.request("GET", url)

        bs = bs4.BeautifulSoup(response.text, "lxml")

        try:

            div = bs.find_all(name='div', attrs={'class': 'well-sm'})[1]
            img = ""  # div.find(name='img').attrs['src']

        except (AttributeError, IndexError):
            return None

        url = "https://www.youav.com" + div.a.attrs['href']

        av = AV()
        av.code = code
        av.video_url = url
        av.preview_img_url = img

        return av
