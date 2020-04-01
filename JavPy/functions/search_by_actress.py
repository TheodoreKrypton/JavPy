import JavPy.sources  # do not remove this line
from JavPy.functions.sources import Sources
from JavPy.functions.actress_translate import ActressTranslate
from JavPy.functions.history_names import HistoryNames
from JavPy.utils.requester import submit, wait_until


class SearchByActress:
    @staticmethod
    def __guess_lang(text):
        if all(map(lambda c: ord(c) < 128, text)):
            lang = "en"

        else:
            if any(map(lambda c: 0x0800 <= ord(c) <= 0x4E00, text)):
                lang = "jp"
            else:
                lang = "zh"

        return lang

    @classmethod
    def search(cls, actress, up_to, history_name=False):
        lang = cls.__guess_lang(actress)

        if lang == "en":
            actress = ActressTranslate.translate2jp(actress)
        if actress:
            videos = [submit(source.search_by_actress, actress, up_to)
                      for source in Sources.SearchByActress]
            if history_name:
                names = submit(HistoryNames.get_history_names, actress)
                return wait_until(videos), names.result()
            else:
                return wait_until(videos), None


if __name__ == '__main__':
    print(SearchByActress.search("飯岡かなこ", None, True))
