from six import with_metaclass
from JavPy.functions.sources import Sources


class RegisterInterface(type):
    def __init__(cls, name, bases, clsdict):
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

        super(RegisterInterface, cls).__init__(name, bases, clsdict)


class INewlyReleased(with_metaclass(RegisterInterface)):
    @classmethod
    def get_newly_released(cls, page):
        pass

    @classmethod
    def priority(cls):
        pass


class ISearchByCode(with_metaclass(RegisterInterface)):
    @classmethod
    def search_by_code(cls, code):
        pass


class ISearchByActress(with_metaclass(RegisterInterface)):
    @classmethod
    def search_by_actress(cls, actress, up_to):
        pass


class IGetBrief(with_metaclass(RegisterInterface)):
    @classmethod
    def get_brief(cls, code):
        pass


class ISearchMagnet(with_metaclass(RegisterInterface)):
    @classmethod
    def search_magnet(cls, code):
        pass


class IHistoryNames(with_metaclass(RegisterInterface)):
    @classmethod
    def get_history_names(cls, actress):
        pass


class ITranslateEn2Jp(with_metaclass(RegisterInterface)):
    @classmethod
    def translate2jp(cls, actress):
        pass


class IActressInfo(with_metaclass(RegisterInterface)):
    @classmethod
    def get_actress_info(cls, actress):
        pass


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
