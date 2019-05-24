from threading import current_thread

__all__ = ["TempDB"]


class TempDB(dict):
    def __getitem__(self, item):
        return super().__getitem__(db_id())[item]

    def __setitem__(self, key, value):
        if not super().__contains__(db_id()):
            super().__setitem__(db_id(), {})
        super().__getitem__(db_id())[key] = value

    def __delitem__(self, key):
        del super().__getitem__(db_id())[key]

    def __contains__(self, item):
        if db_id() not in super().keys():
            return False
        return item in super().__getitem__(db_id())

    def __str__(self):
        st = ""
        for name, obj in super().__getitem__(db_id()).items():
            st += "{}: {}\n".format(name, obj)
        return st

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def is_init(self):
        return super().__contains__(db_id())


def db_id():
    return current_thread()
