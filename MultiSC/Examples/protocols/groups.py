from MultiSC.MultiServer.protocols.protocols_groups.group import Group

from .user_protocol import UserProtocol


#  base group of protocols
base_group = Group("base_group", 0)  # level 0 for logs
base_group.add_protocol("UserProtocol", UserProtocol())

#  protocols that allowed after login
after_login = Group("after_login", 1)  # level 1 for logs
after_login.contain_group(base_group)  # give access to base group on after login group
# Example of adding protocol: after_login.add_protocol(<protocol_name>, <ProtocolObject>)


all_groups = {"base_group": base_group, "after_login": after_login}
