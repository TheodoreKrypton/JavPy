import requests
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.utils.config import proxy
import json


class xfantasy_tv(BaseEmbed):
    @staticmethod
    def decode(url):
        video_id = url.split("?")[0].split("/")[-1]

        payload = '{"operationName": "Query","variables": {"id": "%s"},' \
                  '"query": "query Query($id: String!){getVideoSources(id:$id){sources{src}}}"}' % video_id
        headers = {
            'content-type': "application/json"
        }

        response = requests.post("https://xfantazy.com/graphql", data=payload, headers=headers, proxies=proxy)
        obj = json.loads(response.text)

        sources = obj["data"]["getVideoSources"]["sources"]
        for source in sources:
            if "https://" in source["src"]:
                return source['src']

    @staticmethod
    def pattern(url):
        if "xfantasy.tv" in url or "xfantazy.tv" in url:
            return True
        return False


if __name__ == '__main__':
    print(xfantasy_tv.decode("https://xfantazy.com/video/5eb39eba7e2bee182b8e3610"))