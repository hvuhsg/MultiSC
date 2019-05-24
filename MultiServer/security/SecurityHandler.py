import logging
import base64
import rsa

import __config__.security_config as config
from .encryption import Encryption
from .security_config import get_config
from global_objects import SERI, DE_SERI

CHECK_MESSAGE = config.CHECK_MESSAGE


class SecurityHandler:
    """
        security handler:
        class that allow to secure your connection

        connection -> request_handler object
        encryption_class -> Encryption class with simple interface
        sign_key -> key to sign on the asymmetric key
        asymmetric_key -> asymmetric key that allow to exchange keys

        secure_connection() -> start exchange keys protocol
            send_public_key() -> part of exchange keys protocol
            get_encryption_key() -> part of exchange keys protocol

        recv(num) -> recv data from socket and decrypt it
        send(message) -> encrypt message and send it
    """

    def __init__(self, connection):
        self.logger = logging.getLogger("SecurityHandler")
        encryption_class, sign_key, asymmetric_key, encryption_private_key = (
            get_config()
        )  # from security_config

        if not issubclass(encryption_class, Encryption):
            raise ValueError(
                "class {} is not sub class of Encryption".format(encryption_class)
            )

        self.encryption_private_key = encryption_private_key
        self.encryption_class = encryption_class
        self.sign_key = sign_key
        self.asymmetric_key = asymmetric_key
        self.connection = connection
        self.is_secure = False

    def secure_connection(self):
        self.logger.info("start secure connection")
        try:
            self.send_public_key()
            self.get_encryption_key()
        except ConnectionError as ex:
            self.logger.info("connection closed. (not secure)")
            raise ex
        self.logger.info("connection secured")

    def send_public_key(self):
        random_string = self.get_random_string()
        public_key_json = self.create_public_key_json(random_string)
        self.connection.send(public_key_json.encode())

    def get_encryption_key(self):
        json_key = self.connection.recv(2048)
        if not json_key:
            raise ConnectionError("connection closed")
        dict_key = self.de_json(json_key.decode())
        base64_key = dict_key["encryption_key"]
        encrypted_key = base64.b64decode(base64_key)
        key = rsa.decrypt(encrypted_key, self.encryption_private_key)
        self.encryption_key = self.encryption_class(key)
        self.is_secure = True
        self.connection.send(CHECK_MESSAGE)
        check = self.connection.recv(1024).decode()
        if not CHECK_MESSAGE == check:
            self.logger.error("connection not secure error")
            raise ConnectionError("secure error")
        self.connection.send("connection secured")

    def get_random_string(self):
        random_string_json = self.connection.recv(1024).decode()
        if not random_string_json:
            raise ConnectionError("connection closed")
        dict_obj = self.de_json(random_string_json)
        random_string = dict_obj["random_string"]
        return random_string

    def create_public_key_json(self, random_string):
        public_key_dict = dict()
        public_key_dict["key_file"] = self.asymmetric_key
        public_key_dict["random_string"] = random_string
        public_key_json = self.to_json(public_key_dict)
        sign = rsa.sign(public_key_json.encode(), self.sign_key, "SHA-256")
        sign = base64.b64encode(sign).decode()
        public_key_dict["sign"] = sign
        return self.to_json(public_key_dict)

    def decrypt(self, data):
        if self.is_secure:
            res = self.encryption_key.decrypt(data)
        else:
            res = data
        return res

    def encrypt(self, data):
        if self.is_secure:
            to_send = self.encryption_key.encrypt(data)
        else:
            to_send = data
        return to_send

    def de_json(self, json_obj):
        dict_obj = DE_SERI(json_obj)
        return dict_obj

    def to_json(self, some_dict):
        json_obj = SERI(some_dict).decode()
        return json_obj
