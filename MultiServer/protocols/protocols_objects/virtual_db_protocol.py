from random import getrandbits
from ..protocol import Protocol
from global_objects import VirtualDB, ManagementServerDB
from __config__ import protocol_code_config as config


class VirtualDBProtocol(Protocol):
    def __init__(self):
        self.name = "VirtualDB"
        self.functions = {
            "create_db": self.create_db,
            "delete_db": self.delete_db,
            "create_key": self.create_key,
            "get_key": self.get_key,
            "update_key": self.update_key,
            "delete_key": self.delete_key,
        }
        self.virtual_db = VirtualDB.db
        self.server_db = ManagementServerDB
        super().__init__(self.name, self.functions)

    def create_db(self, query):
        col_id = str(getrandbits(200))
        while col_id in self.virtual_db.list_collection_names():
            col_id = str(getrandbits(200))
        user = query.state["user"]
        self.virtual_db.create_collection(col_id)  # create new collection
        self.server_db.users_info_col.update_one(
            {"_id": user["name"]}, {"$addToSet": {"db_ids": col_id}}
        )
        query.add_response({"db_id": col_id})

    def delete_db(self, query):
        db_id = query["db_id"]
        if not self.permission_check(query):
            return
        self.virtual_db.drop_collection(db_id)
        query.add_response("db {} has deleted".format(db_id))

    def create_key(self, query):
        db_id = query["db_id"]
        key_name = query["key"]
        start_value = query["value"]

        if not self.permission_check(query):
            return
        self.virtual_db[db_id].insert_one({"_id": key_name, "value": start_value})
        query.add_response("ok key was created")

    def get_key(self, query):
        db_id = query["db_id"]
        key_name = query["key"]

        if not self.permission_check(query):
            return
        key = self.virtual_db[db_id].find_one({"_id": key_name})
        if key:
            value = key["value"]
        else:
            query.add_error("key doesnt found", code=config.arg_not_found)
            return
        query.add_response({"value": value})

    def pop_from_array(self, query):
        """db.users.aggregate([
           {
             $project:
              {
                 name: 1,
                 first: { $arrayElemAt: [ "$favorites", 0 ] },
                 last: { $arrayElemAt: [ "$favorites", -1 ] }
              }
           }
        ])"""
        db_id = query["db_id"]
        key_name = query["key"]
        if not self.permission_check(query):
            return
        self.virtual_db[db_id].aggregate()

    def update_key(self, query):
        db_id = query["db_id"]
        key_name = query["key"]
        updated_value = query["value"]
        action = query["action"]
        if not action:
            action = "$set"

        if not self.permission_check(query):
            return
        res = self.virtual_db[db_id].update_one(
            {"_id": key_name}, {action: {"value": updated_value}}
        )
        if res.raw_result:
            print(dir(res))
            query.add_response(res.raw_result)
        else:
            query.add_response("key updated")

    def delete_key(self, query):
        db_id = query["db_id"]
        key_name = query["key"]

        if not self.permission_check(query):
            return
        self.virtual_db[db_id].delete_one({"_id": key_name})
        query.add_response("key deleted")

    def permission_check(self, query):
        db_id = query["db_id"]
        user_name = query.state["user"]["name"]
        user_info = self.server_db.users_info_col.find_one({"_id": user_name})

        if db_id not in user_info["db_ids"]:
            query.add_error(
                "you don't have a permission to do this", code=config.action_not_allow
            )
            return False
        return True
