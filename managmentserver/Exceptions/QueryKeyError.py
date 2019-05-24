from .MainException import MainException
from __config__.protocol_code_config import arg_not_found


class QueryKeyError(KeyError, MainException):
    def __init__(self, key):
        msg = "argument {} is required".format(key)
        self.level = 1
        self.error_code = arg_not_found
        super().__init__(msg, self.level)
