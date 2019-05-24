from protocols.protocol import Protocol
from Exceptions.CloseConnection import CloseConnection
from Exceptions.TestException import TestException


class TestProtocol(Protocol):
    def __init__(self):
        self.name = "TestProtocol"
        self.function = {"test": self.test}
        super().__init__(self.name, self.function)

    def test(self, query):
        if query["message"] == "block":
            query.change_settings("block socket", True)
        elif query["message"] == "close":
            raise CloseConnection("client request to close socket")
        elif query["message"] == "error":
            raise TestException("Error by request")
        else:
            all_query = query.get_response(all=True)
            all_query.pop("Response")
            query.add_response(all_query)
