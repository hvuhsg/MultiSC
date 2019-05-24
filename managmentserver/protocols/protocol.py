from __config__.protocol_code_config import arg_not_found


class Protocol:
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions

    def handle(self, query):
        function_name = query["function"]
        if function_name not in self.functions:
            query.add_error(
                "function {} not found".format(function_name), code=arg_not_found
            )
            return
        func = self.functions[function_name]
        func(query)

    def get_name(self):
        return self.name
