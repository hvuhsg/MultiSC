from ..global_objects.global_object import GlobalObject
from __config__ import system_config as sys_config
from importlib import import_module

if sys_config.quick_setup_mod:
    from ..quick_setup import ProtocolsManager


class Factory(GlobalObject):
    def __init__(self):
        self.groups = None
        if sys_config.quick_setup_mod:
            self.quick_setup_protocols = ProtocolsManager.protocols
        self.global_object_name = "ProtocolsFactory"
        super().__init__(self.global_object_name)

    def __setup__(self):
        try:
            groups_module = import_module(sys_config.groups_module_path)
            self.groups = groups_module.all_groups
        except ImportError as ex:
            print("cant load protocols groups module", ex)
            self.groups = {}

    def __finish__(self):
        pass

    def get_protocols(self, group_name):
        if sys_config.quick_setup_mod:
            return self.quick_setup_protocols
        return self.groups[group_name]
