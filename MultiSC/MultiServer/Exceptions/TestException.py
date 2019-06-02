from __config__.protocol_code_config import server_error
from .MainException import MainException


class TestException(MainException):
    def __init__(self, msg=""):
        self.level = 1
        self.error_code = server_error
        super().__init__(msg, self.level)
