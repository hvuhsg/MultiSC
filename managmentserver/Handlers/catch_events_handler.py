import logging

from __config__.logging_config import catch_event_level
from global_objects import ManagementServerDB


class CatchEventsHandler(logging.Handler):
    def __init__(self, level=catch_event_level):
        self.db = ManagementServerDB.db
        self.event_col = None
        self.level = level
        super().__init__(self.level)

    def emit(self, record):
        self.event_col = self.db["Events"]
        event = {
            "logger name": record.name,
            "thread_name": record.threadName,
            "module": record.module,
            "created": record.created,
            "exc text": record.exc_text,
            "args": record.args,
            "levelname": record.levelname,
            "msg": str(record.msg),
            "funcName": record.funcName,
        }
        if record.levelno <= self.level:
            self.event_col.insert_one(event)
