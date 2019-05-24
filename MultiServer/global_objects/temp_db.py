import logging
from threading import Thread
from time import sleep

from .global_object import GlobalObject, GlobalObjectOptions
from ..DB.TempDB import TempDB as TempDBLocal

class TempDB(GlobalObject):
    def __init__(self):
        self.logger = logging.getLogger("TempDB")
        self.db = TempDBLocal()
        self.stop = False
        self.active = False
        self.option_object = TempDbOptions(self)
        super().__init__()

    def __setup__(self):
        clean_thread = Thread(target=self.cleaner)
        clean_thread.setDaemon(True)
        clean_thread.setName("clean temp db thread")
        clean_thread.start()
        self.active = True
        super().__setup__()

    def __finish__(self):
        self.stop = True
        self.active = False
        super().__finish__()

    def cleaner(self):
        while not self.stop:
            remove_list = []
            sleep(2)
            for thread in self.db:
                if not thread.is_alive():
                    remove_list.append(thread)

            for thread in remove_list:
                self.logger.info("clean {}".format(thread))
                self.db.pop(thread)


class TempDbOptions(GlobalObjectOptions):
    def __init__(self, tempdb):
        self.tempdb = tempdb
        self.name = "[temp db]\n"
        super().__init__()

    def status(self):
        return self.name + """cleaner active: {}""".format(self.tempdb.active)
