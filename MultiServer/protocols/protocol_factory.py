from global_objects.global_object import GlobalObject
import __config__.system_config as sys_config

if sys_config.quick_setup_mod:
    from quick_setup import ProtocolsManager


class Factory(GlobalObject):
    def __init__(self):
        self.groups = None
        if sys_config.quick_setup_mod:
            self.quick_setup_protocols = ProtocolsManager.protocols
        self.global_object_name = "ProtocolsFactory"
        super().__init__(self.global_object_name)

    def __setup__(self):
        from .protocols_groups.groups import all_groups

        self.groups = all_groups

    def __finish__(self):
        pass

    def get_protocols(self, group_name):
        if sys_config.quick_setup_mod:
            return self.quick_setup_protocols
        return self.groups[group_name]
