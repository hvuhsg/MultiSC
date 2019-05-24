from .MainException import MainException


class CloseConnection(MainException):
    def __init__(self, message=""):
        self.level = 0
        super(CloseConnection, self).__init__(message, self.level)
