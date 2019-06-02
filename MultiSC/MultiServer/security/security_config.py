import rsa
import os

from .encryption import Fernet

from __config__ import security_config


def load_key(key_path):
    key_data = open(key_path, "rb").read()
    if b"PRIVATE" in key_data:
        return rsa.PrivateKey.load_pkcs1(key_data)
    return rsa.PublicKey.load_pkcs1(key_data)

def get_config():
    public_key = open(security_config.PUB_KEY_PATH, "r").read()
    sign_private_key = load_key(security_config.SIGN_PRIVATE_KEY_PATH)
    encryption_private_key = load_key(security_config.KEY_PATH)
    return Fernet, sign_private_key, public_key, encryption_private_key
