from pprint import pprint
import base64
import os

from .client import Client, Request
from __client_config__ import connection_config


class ClientError(Exception):
    def __init__(self, msg=""):
        super().__init__(msg)


class EasyClient(Client):
    def __init__(self, server_address=None):
        self.recv_count = connection_config.recv_package_size
        self.default_download_size = connection_config.download_package_size
        self.default_upload_size = connection_config.upload_package_size
        self.ms_list = None
        super().__init__(server_address)

    def _printProgressBar(
        self, iteration, total, prefix="", suffix="", decimals=1, length=100, fill="█"
    ):
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")

    def _activate(self, request):
        self.send(request)
        res = self.recv(self.recv_count)
        if "Error" in res:
            return ClientError(str(res["Error"]))
        return res["Response"]

    def _upload(self, protocol, func, path, name, **kwargs):
        if "info" not in kwargs:
            kwargs["info"] = {}

        file = open(path, "rb")

        file_info = os.stat(path)
        file_size = file_info.st_size

        upload_count = 0
        while True:
            upload_count += 1
            data = file.read(self.default_upload_size)
            upload_count += len(data)
            data = base64.b64encode(data).decode()
            req = Request(
                protocol, func, name=name, data=data, info=kwargs["info"], close=False
            )
            if not data:
                req["close"] = True
            res = self._activate(req)
            self._printProgressBar(
                upload_count,
                file_size,
                prefix="Progress:",
                suffix="Upload Complete",
                length=50,
            )
            if req["close"]:
                break
        file.close()

    def _download(
        self, protocol, func, name, size=None, save_filename=None, file_total_size=None
    ):
        if not save_filename:
            save_filename = name
        if not size:
            size = self.default_download_size
        req = Request(
            protocol, func, name=name, size=size + 300
        )  # 300 for the json info

        file = open(save_filename, "wb")
        file_size = 0
        download_count = 0
        while True:
            download_count += 1
            res = self._activate(req)
            if not res["data"]:
                break
            file_size += size - 300
            file.write(base64.b64decode(res["data"].encode()))
            if file_total_size:
                self._printProgressBar(
                    file_size,
                    file_total_size,
                    prefix="Progress:",
                    suffix="Download Complete",
                    length=50,
                )
        file.close()

    def login(self, name, password):
        func = "login"
        protocol = "UserProtocol"
        res = Request(protocol, func, name=name, password=password)
        return self._activate(res)

    def logout(self):
        func = "logout"
        protocol = "UserProtocol"
        res = Request(protocol, func)
        return self._activate(res)

    def admin_login(self, name, password):
        func = "admin_login"
        protocol = "UserProtocol"
        res = Request(protocol, func, name=name, password=password)
        return self._activate(res)

    def register(self, name, password, email):
        func = "register"
        protocol = "UserProtocol"
        res = Request(protocol, func, name=name, password=password, email=email)
        return self._activate(res)

    def run_command(self, command):
        protocol = "AdminProtocol"
        func = "run_command"
        res = Request(protocol, func, command=command)
        return self._activate(res)

    def get_ms_list(self):
        protocol = "UserMsProtocol"
        func = "get_ms_list"
        res = Request(protocol, func)
        ms_list = self._activate(res)
        self.ms_list = ms_list["list"]
        return ms_list

    def download_ms(self, name, size=None, save_filename=None):
        protocol = "UserMsProtocol"
        func = "download_ms"

        total_size = None
        if self.ms_list:
            try:
                file = self.ms_list[name]
            except:
                pass
            if file:
                total_size = file["size"]
        return self._download(
            protocol, func, name, size, save_filename, file_total_size=total_size
        )

    def upload_log(self, name, path, **kwargs):
        protocol = "UserLogsProtocol"
        func = "upload_log"
        return self._upload(protocol, func, path, name, **kwargs)

    def upload_ms(self, path, name, **kwargs):
        protocol = "MsProtocol"
        func = "upload_ms"
        return self._upload(protocol, func, path, name, **kwargs)

    def create_db(self):
        protocol = "VirtualDBProtocol"
        func = "create_db"
        res = Request(protocol, func)
        return self._activate(res)

    def delete_db(self, db_id):
        protocol = "VirtualDBProtocol"
        func = "delete_db"
        res = Request(protocol, func, db_id=db_id)
        return self._activate(res)

    def create_key(self, db_id, key, value):
        protocol = "VirtualDBProtocol"
        func = "create_key"
        res = Request(protocol, func, db_id=db_id, key=key, value=value)
        return self._activate(res)

    def get_key(self, db_id, key):
        protocol = "VirtualDBProtocol"
        func = "get_key"
        res = Request(protocol, func, db_id=db_id, key=key)
        return self._activate(res)

    def update_key(self, db_id, key, value, action=None):
        protocol = "VirtualDBProtocol"
        func = "update_key"
        res = Request(protocol, func, db_id=db_id, key=key, value=value, action=action)
        return self._activate(res)

    def delete_key(self, db_id, key):
        protocol = "VirtualDBProtocol"
        func = "delete_key"
        res = Request(protocol, func, db_id=db_id, key=key)
        return self._activate(res)

    def get_user_info(self):
        protocol = "UserProtocol"
        func = "get_user_info"
        res = Request(protocol, func)
        return self._activate(res)

    def castom_request(self, protocol, function, **kwargs):
        res = Request(protocol, function, **kwargs)
        return self._activate(res)


def main():
    client = EasyClient(("127.0.0.1", 84))
    client.connect()

    name = input("Name: ")
    pwd = input("Password: ")

    print(client.login(name, pwd))

    pprint(client.get_ms_list())

    ms_name = input("ms name: ")

    print(client.download_ms(ms_name))


if __name__ == "__main__":
    main()
