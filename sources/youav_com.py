from sources.BaseSource import ISearchByCode, SourceException
import requests
import re
import bs4
import json
from embed.decode import decode
from functions.datastructure import AV


class YouAVCom(ISearchByCode):
    def __init__(self):
        pass

    @classmethod
    def search_by_code(cls, code):
        url = "https://www.youav.com/search/videos?search_query=" + code

        response = requests.request("GET", url, verify=False)

        bs = bs4.BeautifulSoup(response.text, "lxml")

        try:

            div = bs.find_all(name='div', attrs={'class': 'well-sm'})[1]
            img = div.find(name='img').attrs['src']

        except (AttributeError, IndexError):
            return None

        url = "https://www.youav.com" + div.a.attrs['href']

        av = AV()
        av.code = code
        av.video_url = url
        av.preview_img_url = img

        return av
