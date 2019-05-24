from __config__.protocol_code_config import server_error


class MainException(Exception):
    def __init__(self, msg, level=None, error_code=server_error):
        self.level = level
        self.error_code = error_code
        super().__init__(msg)
