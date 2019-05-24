from ..protocol import Protocol
from .ms_protocol import MsProtocol


class UserMsProtocol(Protocol):
    def __init__(self):
        self.name = "UserMsProtocol"
        self.ms_protocol = MsProtocol()
        self.functions = {
            "download_ms": self.ms_protocol.download_ms,
            "get_ms_list": self.ms_protocol.get_ms_list,
        }
        super().__init__(self.name, self.functions)
