from JavPy.functions.sources import Sources
from JavPy.functions.datastructure import *
from abc import ABCMeta, abstractmethod


class RegisterInterface(type):
    def __init__(cls, name, bases, cls_dict):
        for base in bases:
            if base.__name__ == 'INewlyReleased':
                Sources.NewlyReleased.append(cls)
            elif base.__name__ == 'ISearchByCode':
                Sources.SearchByCode.append(cls)
            elif base.__name__ == 'ISearchByActress':
                Sources.SearchByActress.append(cls)
            elif base.__name__ == 'IGetBrief':
                Sources.Brief.append(cls)
            elif base.__name__ == 'ISearchMagnet':
                Sources.Magnet.append(cls)
            elif base.__name__ == 'IHistoryNames':
                Sources.HistoryNames.append(cls)
            elif base.__name__ == 'ITranslateEn2Jp':
                Sources.TranslateEn2Jp.append(cls)
            elif base.__name__ == 'IActressInfo':
                Sources.ActressInfo.append(cls)

        super(RegisterInterface, cls).__init__(name, bases, cls_dict)


class INewlyReleased(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def get_newly_released(mcs, page: int) -> List[Brief]:
        pass

    @classmethod
    @abstractmethod
    def priority(mcs) -> int:
        pass

    @classmethod
    @abstractmethod
    def test_newly_released(mcs):
        assert mcs.get_newly_released(2)


class ISearchByCode(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def search_by_code(mcs, code: str) -> Optional[AV]:
        pass

    @classmethod
    @abstractmethod
    def test_search_by_code(mcs, code: str):
        assert mcs.search_by_code(code).video_url


class ISearchByActress(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def search_by_actress(mcs, actress: str, up_to: Optional[int]) -> List[Actress]:
        pass

    @classmethod
    @abstractmethod
    def test_search_by_actress(mcs, actress: str, up_to: Optional[int]):
        assert mcs.search_by_actress(actress, up_to)


class IGetBrief(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def get_brief(mcs, code: str) -> Optional[Brief]:
        pass

    @classmethod
    @abstractmethod
    def test_get_brief(mcs, code: str):
        assert mcs.get_brief(code).title


class ISearchMagnet(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def search_magnet(mcs, code: str) -> List[Magnet]:
        pass

    @classmethod
    @abstractmethod
    def test_search_magnet(mcs, code: str):
        assert mcs.search_magnet(code)


class IHistoryNames(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def get_history_names(mcs, actress: str) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def test_history_names(mcs, actress: str):
        assert mcs.get_history_names(actress)


class ITranslateEn2Jp(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def translate2jp(mcs, actress: str) -> Optional[str]:
        pass

    @classmethod
    @abstractmethod
    def test_translate_en2jp(mcs, actress: str):
        assert mcs.translate2jp(actress)


class IActressInfo(ABCMeta, metaclass=RegisterInterface):
    @classmethod
    @abstractmethod
    def get_actress_info(mcs, actress: str) -> Optional[Actress]:
        pass

    @classmethod
    @abstractmethod
    def test_actress_info(mcs, actress: str):
        assert mcs.get_actress_info(actress).height


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
