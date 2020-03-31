from JavPy.utils.requester import executor, wait_until
from JavPy.functions.sources import Sources
from JavPy.utils.common import cache


class ActressTranslate:
    @staticmethod
    @cache
    def translate2jp(actress):
        return wait_until((executor.submit(source.translate2jp, actress) for source in Sources.TranslateEn2Jp))


if __name__ == "__main__":
    print(ActressTranslate.translate2jp("Eimi Fukada"))
