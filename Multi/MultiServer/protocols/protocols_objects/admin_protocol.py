from ...__config__ import protocol_code_config as config
from ...global_objects import GLOBAL_OBJECTS
from ..protocol import Protocol


class AdminProtocol(Protocol):
    def __init__(self):
        self.name = type(self.__class__).__name__
        self.functions = {"run_command": self.run_command}

        self.workspace = GLOBAL_OBJECTS["WorkspaceManager"]
        super().__init__(self.name, self.functions)

    def run_command(self, query):
        command = query["command"]
        admin = query.state["user"]
        command_result, run_ok = self.workspace.run_command(command, admin["is_master"])
        query.add_response(
            {"result": command_result, "have error": not run_ok, "code": config.ok}
        )
