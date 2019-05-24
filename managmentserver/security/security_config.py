import rsa
import os

try:
    from .encryption import Fernet
except ModuleNotFoundError as MNFE:
    if __name__ == "__main__":
        Fernet = "Fernet Encryption class cannot import"
    else:
        raise MNFE

path = os.path.dirname(__file__)

path += r"\\keys\\"  # keys folder

KEY_PATH = path + r"private_key.rsa"
VERIFY_PUBLIC_KEY_PATH = path + r"public_verify_key.rsa"  # use on the client
SIGN_PRIVATE_KEY_PATH = path + r"private_verify_key.rsa"
PUB_KEY_PATH = path + r"public_key.rsa"


def load_key(key_path):
    key_data = open(key_path, "rb").read()
    if b"PRIVATE" in key_data:
        return rsa.PrivateKey.load_pkcs1(key_data)
    return rsa.PublicKey.load_pkcs1(key_data)


public_key = open(PUB_KEY_PATH, "r").read()
sign_private_key = load_key(SIGN_PRIVATE_KEY_PATH)
encryption_private_key = load_key(KEY_PATH)


def get_config():
    return Fernet, sign_private_key, public_key, encryption_private_key


if __name__ == "__main__":
    print(get_config())
