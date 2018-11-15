from sources.javmost_com import JavMostCom


class New:
    def __init__(self):
        pass

    @staticmethod
    def get_newly_released(allow_many_actresses, up_to):
        return JavMostCom.get_newly_released(allow_many_actresses, up_to)