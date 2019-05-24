from ..protocol import Protocol
from global_objects import ManagementServerDB
from __config__.protocol_code_config import argument_invalid


class CoinProtocol(Protocol):
    def __init__(self):
        self.name = "CoinProtocol"
        self.functions = {"send_coin": self.send_coin}
        self.db = ManagementServerDB
        super().__init__(self.name, self.functions)

    def send_coin(self, query):
        user = query.state["user"]
        subject_name = query["subject"]
        count = query["count"]

        if count < 0:
            query.add_error("number of ml coins must be > 0", code=argument_invalid)
            return
        if int(user["ml_coin"]) < count:
            query.add_error(
                "you don't have {} ml coins".format(count), code=argument_invalid
            )
            return

        self.db.users_info_col.update_one(
            {"_id": user["name"]}, {"$inc", {"ml_coin": count * -1}}
        )
        user["ml_coin"] -= count
        self.db.users_info_col.update_one(
            {"_id": subject_name}, {"$inc", {"ml_coin": count}}
        )
