from sources.javmost_com import JavMostCom
import datetime


class New:
    def __init__(self):
        pass

    newly_released = []
    record_date = datetime.datetime.today().date()

    @classmethod
    def get_newly_released(cls, allow_many_actresses, up_to):
        today = datetime.datetime.today().date()
        if cls.record_date < today:
            cls.record_date = today
            cls.newly_released = []
            cls.newly_released_with_many_actresses = []

        if allow_many_actresses:
            if up_to <= len(cls.newly_released_with_many_actresses):
                return cls.newly_released_with_many_actresses[:up_to]

            else:
                cls.newly_released_with_many_actresses = JavMostCom.get_newly_released(allow_many_actresses, up_to)
                return cls.newly_released_with_many_actresses

        else:
            if up_to <= len(cls.newly_released):
                return cls.newly_released[:up_to]

            else:
                cls.newly_released = JavMostCom.get_newly_released(allow_many_actresses, up_to)
                return cls.newly_released
