from .monitor_classs.BlockPentest import BlockPentest
from global_objects.global_object import GlobalObject
import __config__.system_config as sys_config

if sys_config.quick_setup_mod:
    from quick_setup import MonitorManager

__all__ = ["MonitorFactory"]


class MonitorFactory(GlobalObject):
    def __init__(self):
        self.monitors = [BlockPentest]
        if sys_config.quick_setup_mod:
            self.quick_setup_monitors = MonitorManager.monitors
        self.name = "MonitorFactory"
        super().__init__(self.name)

    def get_monitors(self):
        monitors_obj = []
        for monitor_class in self.monitors:
            monitors_obj.append(monitor_class())
        if sys_config.quick_setup_mod:
            monitors_obj += list(self.quick_setup_monitors.values())
        return monitors_obj


#  just for init object
obj = MonitorFactory()
