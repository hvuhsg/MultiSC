from ..protocol import Protocol
from global_objects import ManagementServerDB


class LogsProtocol(Protocol):
    def __init__(self):
        self.name = "LogsProtocol"
        self.functions = {
            "download_log": self.download_log,
            "upload_log": self.upload_log,
            "delete_log": self.delete_log,
        }
        self.db = ManagementServerDB
        self.fs_name = "ms_logs"
        super().__init__(self.name, self.functions)

    def download_log(self, query):
        log_name = query["name"]
        size_to_read = query["size"]
        file_state = "down_log_{}".format(log_name)

        if not self.db.file_exist(self.fs_name, log_name):
            res = {"message": "file not exist"}
            query.add_response(res)
            return

        if file_state in query.state:
            file = query.state[file_state]
        else:
            file = self.db.get_file(self.fs_name, log_name)
            query.state[file_state] = file

        close = False
        data = file.read(size_to_read)
        if not data:
            close = True

        res = {"size": size_to_read, "data": data.decode()}
        query.add_response(res)

        if close:
            file.close()

    def upload_log(self, query):
        log_name = query["name"]
        log_data = query["data"].encode()
        log_close = query["close"]
        client_address = query.other["client_address"]

        log_info = {}
        if "info" in query:
            log_info = query["info"]
        user_name = query.state["user"]["name"]
        log_info["uploader"] = user_name
        log_info["file_type"] = self.fs_name
        log_info["client_address"] = client_address

        state_file = "up_{}".format(log_name)

        if (
            not self.db.file_exist(self.fs_name, log_name)
            and state_file not in query.state
        ):
            file_info = {"filename": log_name, "version": 1}
            file_info.update(log_info)
            file = self.db.create_file(self.fs_name, file_info)
            query.state[state_file] = file
            query.state["create_now"] = True
        elif "create_now" in query.state:
            file = query.state[state_file]
        else:
            res = {"message": "file name already exist"}
            query.add_response(res)
            return
        self.db.write_file(file, log_data, log_close)
        res = {"message": "ok save data", "closed": log_close}
        query.add_response(res)
        if log_close:
            del query.state[state_file]

    def delete_log(self, query):
        log_name = query["name"]
        self.db.delete_file(self.fs_name, log_name)
        res = {"message": "ms deleted"}
        query.add_response(res)
