from threading import Event

from . import finish
from . import setup
from .ConnectionsHandler.server import Server
from .global_objects.Workspace import WorkspaceManager
from .global_objects.global_object import GlobalObject, GlobalObjectOptions


__all__ = ["Runner"]


class Runner(GlobalObject):
    def __init__(self):
        self.stop_event = Event()
        self.init_objects()
        self.option_object = RunnerOptions(self)
        super().__init__()

    def __setup__(self):
        pass

    def __finish__(self):
        pass

    def init_objects(self):
        # register to global object and run on setup
        Server()

        #  init workspace manager (cant init in global_objects because circular import)
        WorkspaceManager()

    def run(self):
        # setup all global objects and more...
        setup.run()

        self.wait_for_exit()

        # finish all global objects and more...
        finish.run()

    def wait_for_exit(self):
        self.stop_event.wait()


class RunnerOptions(GlobalObjectOptions):
    def __init__(self, runner):
        self.runner = runner
        super().__init__()

    def stop(self):
        self.runner.stop_event.set()


def main():
    print("Start MServer...")
    runner = Runner()
    runner.run()
    print("Stop MServer...")


if __name__ == "__main__":
    main()
