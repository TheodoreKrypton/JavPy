import requests
import bs4


class Etigoya:
    @staticmethod
    def get_history_names(actress):
        url = "http://etigoya955.blog49.fc2.com/?q=" + actress + "&charset=utf-8"
        html = requests.get(url).text
        bs = bs4.BeautifulSoup(html, "lxml")
        main = bs.select("#main")[0]
        li = main.select("li", limit=1)[0]
        if "スポンサー広告" in str(li):
            return None
        else:
            names = li.select('a')[1].string.split("＝")
            return names


if __name__ == '__main__':
    print(Etigoya.get_history_names("川合まゆ"))
