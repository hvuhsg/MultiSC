class Group:
    def __init__(self, group_name, group_level, protocols=None):
        if protocols is None:
            protocols = {}

        self.name = group_name
        self.level = group_level
        self.protocols = protocols
        self.group_contains = set()

    def __contains__(self, protocol):
        flag = protocol in self.protocols
        if not flag:
            for group in self.group_contains:
                if protocol in group:
                    flag = True
                    break
        return flag

    def __getitem__(self, protocol_name):
        if protocol_name in self.protocols:
            return self.protocols[protocol_name]
        for group in self.group_contains:
            protocol = group[protocol_name]
            if protocol:
                return protocol
        return None

    def contain_group(self, group):
        self.group_contains.add(group)

    def add_protocol(self, name, protocol):
        self.protocols[name] = protocol
