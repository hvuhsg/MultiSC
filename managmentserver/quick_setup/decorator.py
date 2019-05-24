from .quick_protocol import QuickProtocol
from .quick_monitor import QuickMonitor


class ProtocolsDecorator:
    def __init__(self):
        self.protocols = dict()

    def add(self, protocol_name, function_name):
        return lambda func: self._function_saver(func, protocol_name, function_name)

    def _function_saver(self, func, protocol_name, function_name):
        if protocol_name not in self.protocols:
            self.protocols[protocol_name] = QuickProtocol()
        self.protocols[protocol_name][function_name] = lambda query: query.add_response(
            str(func(query))
        )
        return func  # return the original function


class MonitorsDecorator:
    def __init__(self):
        self.monitors = dict()

    def add(self, monitor_name):
        return lambda func: self._function_saver(func, monitor_name)

    def _function_saver(self, func, monitor_name):
        self.monitors[monitor_name] = QuickMonitor(
            lambda cls, query: func(cls, query), monitor_name
        )
        return func  # return the original function
