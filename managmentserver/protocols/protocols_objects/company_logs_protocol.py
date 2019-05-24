from ..protocol import Protocol
from .logs_protocol import LogsProtocol


class CompanyLogsProtocol(Protocol):
    def __init__(self):
        self.name = "CompanyLogsProtocol"
        self.logs_protocol = LogsProtocol()
        self.functions = {"download_log": self.logs_protocol.download_log}
        super().__init__(self.name, self.functions)
