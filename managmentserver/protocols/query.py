import __config__.protocol_code_config as config
from Exceptions.QueryKeyError import QueryKeyError


class Query:
    def __init__(self, request=None, response=None, state=None):
        if request is None:
            request = {}
        if response is None:
            response = {}

        self.state = state
        self.request = request
        self.response = {"Response": response}
        if "protocol" in self.request:
            self.protocol = self.request["protocol"]
        else:
            self.protocol = None

        self.error = {}
        self.settings = {}
        self.other = {}

    def __getitem__(self, key):
        try:
            return self.request[key]
        except KeyError:
            raise QueryKeyError(key)

    def get_response(self, get_all=False):
        res = {}
        res.update(self.response)
        res.update(self.error)
        if get_all:
            res.update({"Request": self.request})
            res.update({"Settings": self.settings})
            res.update({"Other": self.other})
        return res

    def add_response(self, response):
        if isinstance(response, dict):
            self.response["Response"].update(response)
            if "code" not in self.response["Response"]:
                self.response["Response"]["code"] = config.ok
        else:
            self.response["Response"].update({"message": response})
            self.response["Response"]["code"] = config.ok

    def add_error(self, error, code=None):
        error_dict = dict()
        error_dict["message"] = error
        if code:
            error_dict["code"] = code
        self.error["Error"] = error_dict

    def change_settings(self, setting_name, new_value):
        self.settings[setting_name] = new_value

    def flush_state_protocols(self):
        self.state.flush()

    def flush(self):
        self.settings = {}
        self.request = {}
        self.response = {}
        self.error = {}
        self.other = {}

    def __contains__(self, item):
        return item in self.other or item in self.request or item in self.response

    def __str__(self):
        obj_str = self.__dict__
        return str(obj_str)
