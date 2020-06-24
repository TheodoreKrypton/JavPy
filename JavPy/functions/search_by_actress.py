import JavPy.sources  # do not remove this line
from JavPy.functions.sources import Sources
from JavPy.functions.actress_translate import ActressTranslate
from JavPy.functions.history_names import HistoryNames
from JavPy.utils.requester import submit, wait_until
from JavPy.functions.actress_info import ActressInfo
from JavPy.functions.datastructure import Actress


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
    def search(cls, actress, up_to, with_profile=False):
        lang = cls.__guess_lang(actress)

        if lang == "en":
            actress = ActressTranslate.translate2jp(actress)
        if actress:
            videos = [
                submit(source.search_by_actress, actress, up_to)
                for source in Sources.SearchByActress
            ]
            if with_profile:
                profile = submit(ActressInfo.get_actress_info, actress)
                names = submit(HistoryNames.get_history_names, actress)
                names = names.result()
                profile = profile.result()
                if profile is None:
                    profile = Actress()
                    profile.other["history_names"] = names
                else:
                    profile.other["history_names"] = list(
                        set(names).union(set(profile.other["history_names"]))
                    )
                return wait_until(videos), profile
            else:
                return wait_until(videos), None

        return [], None


if __name__ == "__main__":
    print(SearchByActress.search("Eimi Fukada", None, True))
