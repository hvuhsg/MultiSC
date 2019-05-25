import base64
from ..protocol import Protocol
from ...global_objects import ManagementServerDB


class MsProtocol(Protocol):
    def __init__(self):
        self.name = "MsProtocol"
        self.functions = {
            "get_ms_list": self.get_ms_list,
            "upload_ms": self.upload_ms,
            "download_ms": self.download_ms,
            "delete_ms": self.delete_ms,
        }
        self.db = ManagementServerDB
        self.fs_name = "ms"
        super().__init__(self.name, self.functions)

    def get_ms_list(self, query):
        ms_list = self.db.get_file_list(self.fs_name)
        res = {"list": ms_list}
        query.add_response(res)

    def upload_ms(self, query):
        ms_name = query["name"]
        ms_data = query["data"].encode()
        if ms_data:
            ms_data = base64.b64decode(ms_data)
        ms_close = query["close"]

        ms_info = {}
        ms_info["download_number"] = 0
        if "info" in query:
            ms_info = query["info"]

        if "user" in query.state:
            ms_info["uploader"] = query.state["user"]["name"]
            ms_info["is_admin"] = query.state["user"]["is_admin"]
        if "company" in query.state:
            ms_info["uploader"] = query.state["company"]["name"]
            ms_info["is_admin"] = False

        state_file = "up_{}".format(ms_name)

        if (
            not self.db.file_exist(self.fs_name, ms_name)
            and state_file not in query.state
        ):
            model_info = {"filename": ms_name, "version": 1}
            model_info.update(ms_info)
            file = self.db.create_file(self.fs_name, model_info)
            query.state[state_file] = file
            query.state["create_now"] = True
            if "company" in query.state:
                company = query.state["company"]
                company_name = company["name"]
                self.db.update_company(
                    action="$addToSet",
                    company_name=company_name,
                    company_info={"ms_list": ms_name},
                )
        elif "create_now" in query.state:
            file = query.state[state_file]
        else:
            res = {"message": "file name already exist"}
            query.add_response(res)
            return
        self.db.write_file(file, ms_data, ms_close)
        res = {"message": "ok save data", "closed": ms_close}
        query.add_response(res)
        if ms_close:
            del query.state[state_file]

    def download_ms(self, query):
        ms_name = query["name"]
        size_to_read = query["size"]
        file_state = "down_{}".format(ms_name)

        if not self.db.file_exist(self.fs_name, ms_name):
            res = {"message": "file not exist"}
            query.add_response(res)
            return

        if file_state in query.state:
            file = query.state[file_state]
        else:
            file = self.db.get_file(self.fs_name, ms_name)
            query.state[file_state] = file
            self.db.update_file_info(ms_name, "$inc", {"download_number": 1})
            if "user" in query.state:
                self.db.update_user(
                    "$addToSet", query.state["user"]["name"], {"download_list": ms_name}
                )

        close = False
        data = file.read(size_to_read)
        if not data:
            close = True

        res = {
            "size": size_to_read,
            "data": base64.b64encode(data).decode(),
            "close": close,
        }
        query.add_response(res)

        if close:
            file.close()

    def delete_ms(self, query):
        ms_name = query["name"]
        self.db.delete_file(self.fs_name, ms_name)
        res = {"message": "ms deleted"}
        query.add_response(res)
