import logging
from threading import Event

from ..__config__ import logging_config as config
from ..global_objects import setup_all
from ..monitors import monitorfactory  # do not delete!!

logging.basicConfig(
    level=config.level, format=config.loggin_format, filename=config.filename
)

start_event = Event()

__all__ = ["run", "start_event"]


def setup_global_objects():
    setup_all()


def run():
    setup_global_objects()
    start_event.set()
