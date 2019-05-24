GLOBAL_OBJECTS = {}


class GlobalObject:
    def __init__(self, name=None):
        if name is None:
            name = type(self).__name__
        GLOBAL_OBJECTS[name] = self

    def __setup__(self):
        pass

    def __finish__(self):
        pass


class GlobalObjectOptions:
    def __init__(self):
        pass

    def options(self):
        options = []
        for method in self.__dir__():
            if not str(method).startswith("_"):
                options.append(method)
        return options
