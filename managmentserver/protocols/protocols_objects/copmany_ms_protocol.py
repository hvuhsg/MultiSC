from ..protocol import Protocol
from .ms_protocol import MsProtocol


class CompanyMsProtocol(Protocol):
    def __init__(self):
        self.name = "CompanyMsProtocol"
        self.ms_protocol = MsProtocol()
        self.functions = {"upload_ms": self.ms_protocol.upload_ms}
        super().__init__(self.name, self.functions)
