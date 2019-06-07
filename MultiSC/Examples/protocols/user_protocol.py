from MultiSC.MultiServer.protocols.protocol import Protocol

from __config__ import protocol_code_config as config
from __config__ import users_config as user_config


class UserProtocol(Protocol):
    def __init__(self):
        self.name = "UserProtocol"
        self.function = {
            "login": self.login,
            "register": self.register,
            "get_user_info": self.get_user_info,
            "logout": self.logout,
        }
        # self.db = some_db_module
        super().__init__(self.name, self.function)

    def login(self, query):
        # template of login function
        name = query["name"]
        password = query["password"]
        # validate username and password

        # save user info on the server
        # before that you need to get the info from the db
        query.state["user"] = user_info

        # if everysing good upgrade user premmision
        query.state.set_group_name("after_login")

    def register(self, query):
        # template of register function
        name = query["name"]
        password = query["password"]
        email = query["email"]
        # validate username, password and email

        # if have some problem send response like this
        query.add_response(
            {"message": "your email is invalid", "code": config.argument_invalid}
        )
        # if everysing good, send this response
        query.add_response({"message": "register successfuly", "code": config.ok})

    def logout(self, query):
        # logout function example
        if query.state.group_name == "base_group":
            query.add_response(
                {
                    "message": "your need to login before you logout",
                    "code": config.action_not_allow,
                }
            )
        else:
            del query.state["user"]
            query.state.set_group_name("base_group")
            query.add_response({"message": "logout success"})

    def get_user_info(self, query):
        # get user info function example
        if "user" not in query.state:
            query.add_error("you need to login first.", code=config.action_not_allow)
            return
        user_info = query.state["user"]
        query.add_response({"user_info": dict(user_info)})
