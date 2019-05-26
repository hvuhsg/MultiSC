import re
from time import time

from ..protocol import Protocol

from ...__config__ import protocol_code_config as config
from ...__config__ import users_config as user_config
from ...global_objects import ManagementServerDB


class UserProtocol(Protocol):
    def __init__(self):
        self.name = "UserProtocol"
        self.function = {
            "login": self.login,
            "register": self.register,
            "admin_login": self.admin_login,
            "get_user_info": self.get_user_info,
            "logout": self.logout,
        }
        self.db = ManagementServerDB
        super().__init__(self.name, self.function)

    def login(self, query):
        name = query["name"]
        password = query["password"]
        user = self.db.get_user(name, password)

        if user and query.state.group_name == "base_group":
            query.add_response({"message": "ok your connected.", "code": config.ok})
            query.state["user"] = user
            query.state.set_group_name("after_user_login_group")
        elif query.state.group_name != "base_group":
            query.add_response({"message": "your alrady connected.", "code": config.ok})
        else:
            query.add_response(
                {
                    "message": "username or password wrong",
                    "code": config.argument_invalid,
                }
            )

    def register(self, query):
        name = query["name"]
        password = query["password"]
        email = query["email"]
        register_ip = query.other["client_address"][0]
        if not name or len(name) < 4:
            query.add_response(
                {
                    "message": "name must have minimum of 4 letters",
                    "code": config.argument_invalid,
                }
            )
            return

        if not (12 >= len(password) >= 6):
            query.add_response(
                {
                    "message": "password must have length between 6 - 12",
                    "code": config.argument_invalid,
                }
            )

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            query.add_response(
                {
                    "message": "email address is not valid",
                    "code": config.argument_invalid,
                }
            )

        users_with_same_name = self.db.search("users", {"name": name})
        if not users_with_same_name:
            user_info = {
                "name": name,
                "password": password,
                "register_ip": register_ip,
                "register_time": time(),
                "is_admin": False,
                "email_address": email,
            }
            user_info.update(user_config.new_user_values)
            self.db.create_user(user_info)
            query.add_response({"message": "register successful", "code": config.ok})
        else:
            query.add_response(
                {"message": "username already exist", "code": config.argument_invalid}
            )

    def admin_login(self, query):
        name = query["name"]
        password = query["password"]

        admins = self.db.get_admin(name, password)
        if admins:
            query.add_response(
                {"message": "ok your connected as admin.", "code": config.ok}
            )
            query.state["user"] = admins[0]
            query.state.set_group_name("admin_options")
            query.change_settings("timeout", 1000)
        else:
            query.add_response(
                {
                    "message": "username or password wrong",
                    "code": config.argument_invalid,
                }
            )

    def logout(self, query):
        if query.state.group_name == "base_group":
            query.add_response(
                {
                    "message": "your need to login before you logout",
                    "code": config.action_not_allow,
                }
            )
        else:
            query.state.set_group_name("base_group")
            query.add_response({"message": "logout success"})

    def get_user_info(self, query):
        if "user" not in query.state:
            query.add_error("you need to login first.", code=config.action_not_allow)
            return
        user_name = query.state["user"]["name"]
        user_info = self.db.get_user_info(user_name)
        query.add_response({"user_info": dict(user_info)})
