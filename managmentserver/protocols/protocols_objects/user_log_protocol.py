from ..protocol import Protocol
from .logs_protocol import LogsProtocol


class UserLogsProtocol(Protocol):
    def __init__(self):
        self.name = "UserLogsProtocol"
        self.logs_protocol = LogsProtocol()
        self.functions = {
            "upload_log": self.logs_protocol.upload_log,
            "delete_log": self.logs_protocol.delete_log,
        }
        super().__init__(self.name, self.functions)
