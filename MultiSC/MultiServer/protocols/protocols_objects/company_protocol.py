from time import time
from ..protocol import Protocol
from __config__ import protocol_code_config as config
from __config__ import companys_config
from ...global_objects import ManagementServerDB


class CompanyProtocol(Protocol):
    def __init__(self):
        self.name = "CompanyProtocol"
        self.functions = {
            "login": self.login,
            "register": self.register,
            "get_company_info": self.get_company_info,
        }
        self.db = ManagementServerDB
        super().__init__(self.name, self.functions)

    def login(self, query):
        name = query["name"]
        password = query["password"]

        company = self.db.get_company(name, password)

        if company:
            query.add_response({"message": "ok your connected.", "code": config.ok})
            query.state["company"] = company
            query.state.set_group_name("after_company_login")  # permission group
        else:
            query.add_response(
                {
                    "message": "company name or password wrong",
                    "code": config.argument_invalid,
                }
            )

    def register(self, query):
        name = query["name"]
        password = query["password"]
        register_ip = query.other["client_address"][0]
        users_with_same_name = self.db.search("users", {"name": name})

        if users_with_same_name:
            query.add_response(
                {"message": "username already exist", "code": config.argument_invalid}
            )
            return

        company_info = {
            "name": name,
            "password": password,
            "register_ip": register_ip,
            "register_time": time(),
        }
        company_info.update(companys_config.new_company_values)
        self.db.create_company(company_info)
        query.add_response({"message": "register successful", "code": config.ok})

    def get_company_info(self, query):
        if "company" not in query.state:
            query.add_error("you need to login first.", code=config.action_not_allow)
            return
        company_name = query.state["company"]["name"]
        user_info = self.db.get_company_info(company_name)
        query.add_response({"company_info": dict(user_info)})
