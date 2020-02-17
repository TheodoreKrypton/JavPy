from six import with_metaclass
from JavPy.functions.sources import Sources
from JavPy.functions.datastructure import *


class RegisterInterface(type):
    def __init__(cls, name, bases, cls_dict):
        for base in bases:
            if base is INewlyReleased:
                Sources.NewlyReleased.append(cls)
            elif base is ISearchByCode:
                Sources.SearchByCode.append(cls)
            elif base is ISearchByActress:
                Sources.SearchByActress.append(cls)
            elif base is IGetBrief:
                Sources.Brief.append(cls)
            elif base is ISearchMagnet:
                Sources.Magnet.append(cls)
            elif base is IHistoryNames:
                Sources.HistoryNames.append(cls)
            elif base is ITranslateEn2Jp:
                Sources.TranslateEn2Jp.append(cls)
            elif base is IActressInfo:
                Sources.ActressInfo.append(cls)

        super(RegisterInterface, cls).__init__(name, bases, cls_dict)


class INewlyReleased(with_metaclass(RegisterInterface)):
    @classmethod
    def get_newly_released(cls, page: int) -> List[Brief]:
        pass

    @classmethod
    def priority(cls) -> int:
        pass

    @classmethod
    def test_newly_released(cls):
        assert cls.get_newly_released(2)


class ISearchByCode(with_metaclass(RegisterInterface)):
    @classmethod
    def search_by_code(cls, code: str) -> Optional[AV]:
        pass

    @classmethod
    def test_search_by_code(cls, code: str):
        assert cls.search_by_code(code).video_url


class ISearchByActress(with_metaclass(RegisterInterface)):
    @classmethod
    def search_by_actress(cls, actress: str, up_to: Optional[int]) -> List[Actress]:
        pass

    @classmethod
    def test_search_by_actress(cls, actress: str, up_to: Optional[int]):
        assert cls.search_by_actress(actress, up_to)


class IGetBrief(with_metaclass(RegisterInterface)):
    @classmethod
    def get_brief(cls, code: str) -> Optional[Brief]:
        pass

    @classmethod
    def test_get_brief(cls, code: str):
        assert cls.get_brief(code).title


class ISearchMagnet(with_metaclass(RegisterInterface)):
    @classmethod
    def search_magnet(cls, code: str) -> List[Magnet]:
        pass

    @classmethod
    def test_search_magnet(cls, code: str):
        assert cls.search_magnet(code)


class IHistoryNames(with_metaclass(RegisterInterface)):
    @classmethod
    def get_history_names(cls, actress: str) -> List[str]:
        pass

    @classmethod
    def test_history_names(cls, actress: str):
        assert cls.get_history_names(actress)


class ITranslateEn2Jp(with_metaclass(RegisterInterface)):
    @classmethod
    def translate2jp(cls, actress: str) -> Optional[str]:
        pass

    @classmethod
    def test_translate_en2jp(cls, actress: str):
        assert cls.translate2jp(actress)


class IActressInfo(with_metaclass(RegisterInterface)):
    @classmethod
    def get_actress_info(cls, actress: str) -> Optional[Actress]:
        pass

    @classmethod
    def test_actress_info(cls, actress: str):
        assert cls.get_actress_info(actress).height


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
