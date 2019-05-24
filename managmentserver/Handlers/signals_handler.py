import signal
from global_objects.Workspace import WorkspaceManager


class SignalHandler(object):
    def __init__(self):
        self.workspace_manager = WorkspaceManager()
        self.name = "SignalHandler"

        self.call_sigint = False
        self.call_sigabrt = False
        self.call_sigterm = False

    def __setup__(self):
        signal.signal(signal.SIGINT, self.sigint)
        signal.signal(signal.SIGABRT, self.sigabrt)
        signal.signal(signal.SIGTERM, self.sigterm)

    def __finish__(self):
        pass

    def sigint(self, signum, frame):
        print("SIGINT called with signal number", signum)
        print("frame:", frame)
        # DO SOMETHING
        self._kill_runner()
        self.call_sigint = True

    def sigabrt(self, signum, frame):
        print("SIGABRT called with signal number", signum)
        print("frame:", frame)
        # DO SOMETHING
        self._kill_runner()
        self.call_sigabrt = True

    def sigterm(self, signum, frame):
        print("SIGTERM called with signal number", signum)
        print("frame:", frame)
        # DO SOMETHING
        self._kill_runner()
        self.call_sigterm = True

    def _kill_runner(self):
        self.workspace_manager.global_objects["Runner"].option_object.stop()
