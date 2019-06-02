import rsa
import json
import base64
from cryptography.fernet import Fernet
from random import getrandbits

from __client_config__ import security_config


CHACK_MESSAGE = security_config.CHACK_MESSAGE

class secure_connection(object):
    def __init__(self):
        self.verify_key = self.load_key(security_config.VERIFY_PUBLIC_KEY_PATH)
        self.public_key = None
        self.fernet = None

    def load_key(self, key_path):
        pub_key_data = open(key_path, "rb").read()
        return rsa.PublicKey.load_pkcs1(pub_key_data)

    def __call__(self, connection):
        public_data, random_string = self.get_public_key(connection)
        self.create_send_peer_key(connection, public_data, random_string)
        recv = connection.recv(1024)
        recv = self.fernet.decrypt(recv).decode()
        if not CHACK_MESSAGE in recv:
            raise ConnectionError("connection not secure")
        connection.send(self.fernet.encrypt(str(CHACK_MESSAGE).encode()))
        connection.recv(10000)  # Do not delete!!
        return self.fernet

    def get_public_key(self, connection):
        random_string = getrandbits(100)
        json_random_string = self.to_json({"random_string": random_string})
        connection.send(json_random_string.encode())
        public_data = connection.recv(8600)
        if not public_data:
            raise ConnectionError("connection closed")
        dict_obj = self.de_json(public_data)
        sign = dict_obj["sign"]
        sign = base64.b64decode(sign.encode())
        dict_obj.pop("sign")
        json_obj = self.to_json(dict_obj)
        self.verify(json_obj.encode(), sign)
        if dict_obj["random_string"] != random_string:
            raise ConnectionError("not secure")
        return dict_obj, random_string

    def create_send_peer_key(self, connection, public_data, random_string):
        key_file, random = public_data["key_file"], public_data["random_string"]
        self.public_key = rsa.PublicKey.load_pkcs1(key_file)
        fernet_key = Fernet.generate_key()
        self.fernet = Fernet(fernet_key)
        encrypt_key = rsa.encrypt(fernet_key, self.public_key)
        base64_key = base64.b64encode(encrypt_key)
        dict_encrypt_key = {"encryption_key": base64_key.decode()}
        connection.send(self.to_json(dict_encrypt_key).encode())

    def to_json(self, dict_obj):
        json_obj = json.dumps(dict_obj)
        return json_obj

    def de_json(self, json_obj):
        dict_obj = json.loads(json_obj)
        return dict_obj

    def verify(self, msg, sign):
        return rsa.verify(msg, sign, self.verify_key)
