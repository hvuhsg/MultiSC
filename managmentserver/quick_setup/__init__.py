from .redirect import start_quick_setup_mod


from .decorator import ProtocolsDecorator
from .decorator import MonitorsDecorator

__all__ = ["ProtocolsManager", "MonitorManager"]


start_quick_setup_mod()
ProtocolsManager = ProtocolsDecorator()
MonitorManager = MonitorsDecorator()
