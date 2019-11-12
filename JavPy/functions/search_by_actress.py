import JavPy.sources
from JavPy.functions.sources import Sources
from JavPy.functions.actress_translate import ActressTranslate
from JavPy.functions.history_names import HistoryNames
from future.builtins import map
from JavPy.utils.requester import spawn, Task, spawn_many


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
            movies = spawn_many(
                Task(source.search_by_actress, actress, up_to)
                for source in Sources.SearchByActress
            )
            if history_name:
                names = spawn(HistoryNames.get_history_names, actress)
                result = movies.wait_for_one_finished(), names.wait_for_result()
            else:
                result = movies.wait_for_one_finished(), None

            return result[0][0], result[1]
        else:
            return [], None


if __name__ == '__main__':
    print(SearchByActress.search("Eimi Fukada", None, True))
