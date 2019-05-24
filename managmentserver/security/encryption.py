from cryptography.fernet import Fernet as Fernet_class


class Encryption:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def new_key():
        pass

    def encrypt(self, data) -> bytes:
        pass

    def decrypt(self, data) -> bytes:
        pass


class Fernet(Fernet_class, Encryption):
    def __init__(self, key=None):
        self.have_key = False
        if key:
            self.have_key = True
            self.key = key
            super().__init__(self.key)

    def encrypt(self, data):
        if not self.have_key:
            raise ValueError("can't encrypt without key -> set key first")
        return super().encrypt(data)

    def decrypt(self, data):
        if not self.have_key:
            raise ValueError("can't decrypt without key -> set key first")
        return super().decrypt(data)

    def set_key(self, key):
        self.key = key
        self.have_key = True

    @staticmethod
    def new_key():
        return super().generate_key()
