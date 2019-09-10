from JavPy.sources.BaseSource import ISearchByCode
import requests
import bs4


class XFantasyTV(ISearchByCode):
    def __init__(self):
        pass

    @classmethod
    def search_by_code(cls, code):
        url = "https://xfantasy.tv/search/" + code
        rsp = requests.get(url)
        html = rsp.text
        bs = bs4.BeautifulSoup(html, "lxml")
        card = bs.find(attrs={'data-stats': 'video:feed:1'})
        if not card:
            return None
        title = card.text
        if code in title:
            return "https://xfantasy.tv" + card.attrs['href']
        return None


if __name__ == '__main__':
    print(XFantasyTV.search_by_code("n0753"))
