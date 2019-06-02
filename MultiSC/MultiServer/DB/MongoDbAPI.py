import pymongo
import gridfs
from .AbsDb import AbsDb

from __config__ import db_config as config


class MongoDB(AbsDb):
    def __init__(self, db_name=None, db_username=None, db_password=None):
        if not db_name:
            db_name = config.db_name

        if not (db_username or db_password):
            self.default_name = config.default_name
            self.default_password = config.default_password
        else:
            self.default_name = db_username
            self.default_password = db_password

        self.client = None
        self.ip = config.ip
        self.port = config.port

        self.db_name = db_name
        self.db = None
        self.fs = None
        self.lfs = None  # logs file stream

        self.user_col = None
        self.users_info_col = None
        self.file_info_col = None
        self.companys_col = None
        self.file_col = None
        self.servers_col = None

        self.timeout = config.timeout

        super().__init__()

    def connect(self, name=None, password=None):
        c_name = self.default_name
        c_password = self.default_password
        if name and password:
            c_name = name
            c_password = password

        self.client = pymongo.MongoClient(
            self.ip,
            self.port,
            username=c_name,
            password=c_password,
            authSource=self.db_name,
            serverSelectionTimeoutMS=self.timeout,
        )
        self.connect_init()

    def connect_init(self):
        self.db = self.client[self.db_name]
        self.fs = gridfs.GridFS(self.db, collection=config.MS_TABLE_NAME)
        self.lfs = gridfs.GridFS(self.db, collection=config.LOGS_TABLE_NAME)
        self.file_col = {"ms": self.fs, "ms_logs": self.lfs}
        self.user_col = self.db[config.USERS_TABLE_NAME]
        self.users_info_col = self.db[config.USERS_INFO_TABLE_NAME]
        self.file_info_col = self.db[config.FILE_INFO_TABLE]
        self.companys_col = self.db[config.COMPANYS_TABLE_NAME]
        self.companys_info_col = self.db[config.COMPANYS_INFO_TABLE_NAME]
        self.servers_col = self.db[config.SERVERS_TABLE]

    def search(self, col, db_query, values=None):
        if values is None:
            values = {}
        col = self.db[col]
        return list(col.find(db_query, values))

    def close_connection(self):
        self.client.close()

    def get_user_info(self, user_name):
        return self.users_info_col.find_one({"_id": user_name})

    def create_user(self, user_info):
        basic_info = {"name": user_info["name"], "password": user_info["password"]}
        user_info.pop("name")
        user_info.pop("password")
        user_info["_id"] = basic_info["name"]
        self.user_col.insert_one(basic_info)
        self.users_info_col.insert_one(user_info)

    def get_user(self, user_name, password):
        user = None
        find_query = {"name": user_name, "password": password}
        users = self.search("users", find_query, {"password": 0})
        if users:
            user = users[0]  # just one result
        return user

    def delete_user(self, user_name):
        delete_query = {"user_name": user_name}
        user_info_query_delete = {"_id": user_name}
        res = self.user_col.delete_one(
            delete_query
        )  # return True if success else False
        res = res and self.users_info_col.delete_one(user_info_query_delete)
        return res

    def update_user(self, action, user_name, new_user_info):
        new_values = {action: new_user_info}
        my_user = {"_id": user_name}
        self.users_info_col.update_one(my_user, new_values)

    def get_admin(self, user_name, password):
        find_query = {"name": user_name, "password": password}
        return self.search("admins", find_query, {"password": 0})

    def create_file(self, fs_name, file_info):
        fs = self.file_col[fs_name]
        self.file_info_col.insert_one(file_info)
        return fs.new_file(filename=file_info["filename"])

    def file_exist(self, table, file_name):
        model_id = {"filename": file_name}
        fs = self.file_col[table]
        return fs.exists(model_id)

    def write_file(self, file, data, close=False):
        file.write(data)
        if close:
            file.close()

    def delete_file(self, table, file_name):
        model_id = {"filename": file_name}
        ids = self.search(table + ".files", model_id, {"_id": 1})
        file_id = ids[0]["_id"]
        fs = self.file_col[table]
        fs.delete(file_id)
        self.file_info_col.delete_one(model_id)

    def get_file(self, table, model_name):
        model_id = {"filename": model_name}
        file_id = self.search(table + ".files", model_id, {"_id": 1})[0]["_id"]
        fs = self.file_col[table]
        file = fs.get(file_id)
        return file

    def get_file_info(self, filename):
        search = {"filename": filename}
        dont_get = {"_id": 0}
        return self.search(config.FILE_INFO_TABLE, db_query=search, values=dont_get)[0]

    def update_file_info(self, filename, action, new_values):
        self.file_info_col.update_one({"filename": filename}, {action: new_values})

    def get_file_list(self, table):
        fs = self.file_col[table]
        file_list = fs.list()
        files_and_info = {}
        for filename in file_list:
            file = self.get_file(table, filename)
            file_info = self.get_file_info(file.filename)
            file_info["size"] = file.length
            files_and_info[file_info["filename"]] = file_info
        return files_and_info

    def get_company(self, company_name, password):
        company = None
        find_query = {"name": company_name, "password": password}
        companys = self.search("companys", find_query, {"password": 0})
        if companys:
            company = companys[0]  # just one result
        return company

    def create_company(self, company_info):
        basic_info = {
            "name": company_info["name"],
            "password": company_info["password"],
        }
        company_info.pop("name")
        company_info.pop("password")
        company_info["_id"] = basic_info["name"]
        self.companys_col.insert_one(basic_info)
        self.companys_info_col.insert_one(company_info)

    def delete_company(self, company_name):
        delete_query = {"name": company_name}
        user_info_query_delete = {"_id": company_name}
        res = self.user_col.delete_one(
            delete_query
        )  # return True if success else False
        res = res and self.users_info_col.delete_one(user_info_query_delete)
        return res

    def get_company_info(self, company_name):
        return self.companys_info_col.find_one({"_id": company_name})

    def update_company(self, action, company_name, company_info):
        new_values = {action: company_info}
        my_company = {"_id": company_name}
        self.users_info_col.update_one(my_company, new_values)

    def new_client(self, server_address):
        self.servers_col.update_one(
            {"server_address": server_address}, {"$inc": {"connection_count": 1}}
        )

    def close_client(self, server_address):
        self.servers_col.update_one(
            {"server_address": server_address}, {"$inc": {"connection_count": -1}}
        )

    def open_server(self, server_address):
        self.servers_col.insert_one(
            {"server_address": server_address, "connection_count": 0, "active": True}
        )

    def close_server(self, server_address):
        self.servers_col.delete_one({"server_address": server_address})


#  TODO finish company options
