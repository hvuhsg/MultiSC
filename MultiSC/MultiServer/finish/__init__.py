from threading import Event

from ..global_objects import finish_all

finish_event = Event()

__all__ = ["run", "finish_event"]


def finish_global_objects():
    finish_all()


def run():
    finish_event.set()
    finish_global_objects()
