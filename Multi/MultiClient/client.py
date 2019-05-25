import socket
import json
from .secure_connection import secure_connection
from .DNSClient import DNSClient

__all__ = ["Client", "Request"]


class Client(object):
    def __init__(self, server_address=None):
        if not server_address:
            server_address = DNSClient().get_server_ip()
        self.server_address = server_address
        self.sock = socket.socket()
        self.SEC = None
        self.encryption_key = None
        self.address = server_address
        self.connected = False
        self.secure = False

    def connect(self):
        self.sock.connect(self.address)
        if self.secure:
            self.SEC = secure_connection()
            self.SEC(self.sock)
        self.connected = True

    def direct_connect(self, address):
        self.sock.connect(address)
        # self.secure_connection()
        self.connected = True

    def secure_connection(self):
        self.encryption_key = self.SEC(self.sock)

    def recv(self, num):
        if not self.connected:
            raise Exception("client isn't connected")
        recv_data = self.sock.recv(num)
        if not recv_data:
            raise ConnectionError("connection closed")
        if self.secure:
            recv_data = self.encryption_key.decrypt(recv_data)
        dict_obj = json.loads(recv_data)
        return Response(dict_obj)

    def send(self, message):
        if not self.connected:
            raise Exception("client isn't connected")
        if not type(message) == dict:
            if hasattr(message, "to_dict"):
                message = message.to_dict()
            else:
                raise TypeError(
                    "message type must have to_dict method or be dict object"
                )
        if self.secure:
            return self.sock.send(
                self.encryption_key.encrypt(json.dumps(message).encode())
            )
        else:
            encoded_message = json.dumps(message).encode()
            num_of_send = self.sock.send(encoded_message)

    def close(self):
        self.sock.close()
        self.connected = False


class Request(object):
    def __init__(self, protocol=None, function=None, **kwargs):
        if protocol is None:
            self.protocol = ""
        else:
            self.protocol = protocol

        if function is None:
            self.function = ""
        else:
            self.function = function

        self.function_arguments = kwargs

    def to_dict(self):
        dict_obj = dict()
        dict_obj["protocol"] = self.protocol
        dict_obj["function"] = self.function
        dict_obj.update(self.function_arguments)
        return dict_obj

    def __setitem__(self, key, value):
        self.function_arguments[key] = value

    def __getitem__(self, item):
        return self.function_arguments[item]

    def __delitem__(self, key):
        del self.function_arguments[key]


class Response(object):
    def __init__(self, data):
        self.data = data
        self.has_error = "Error" in data

    def __contains__(self, item):
        return item in self.data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        if self.has_error:
            return str(self.data["Error"])
        return str(self.data["Response"])
