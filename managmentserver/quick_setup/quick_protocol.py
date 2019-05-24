class QuickProtocol:
    def __init__(self):
        self.functions = dict()

    def handle(self, query):
        function_name = query["function"]
        if function_name not in self.functions:
            query.add_error("function {} not found".format(function_name), code=404)
            return
        func = self.functions[function_name]
        func(query)

    def __setitem__(self, func_name, func_obj):
        self.functions[func_name] = func_obj

    def __getitem__(self, func_name):
        return self.functions[func_name]

    def __delitem__(self, func_name):
        del self.functions[func_name]
