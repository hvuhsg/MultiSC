from time import time
from threading import current_thread

from .state import State
from .query import Query

from __config__ import protocol_code_config as config
from ..global_objects import protocols_factory, GLOBAL_OBJECTS
from ..Exceptions.ExceptionHandler import ExceptionHandler


class ProtocolManager:
    def __init__(self, client_address):
        self.state = State()
        self.MonitorFactory = GLOBAL_OBJECTS["MonitorFactory"]
        self.ProtocolFactory = protocols_factory

        self.query = None
        self.exception_level = 1
        self.exception_handler = None
        self.client_address = client_address

    def run(self, dict_request):
        self._setup(dict_request)
        self._handle()
        return self._finish()

    def _setup(self, dict_request):
        if self.query is None:
            self.query = Query()
        else:
            self.query.flush()
        has_problem = self._check_format(dict_request)
        if has_problem:
            #  TODO raise exception
            return

        self.query = Query(request=dict_request, state=self.state)
        self._add_extra_arguments()

    def _handle(self):
        protocol = self.get_protocol()

        if protocol is None:
            self.query.add_error("protocol not found", code=config.arg_not_found)
            return

        self._run_protocol_handler(protocol)

    def _finish(self):
        for monitor in self.MonitorFactory.get_monitors():
            monitor.run_on(self.query)
        self.state = self.query.state
        return self.query

    def _run_protocol_handler(self, protocol):
        func = lambda: protocol.handle(self.query)
        self.exception_handler = ExceptionHandler(
            func, self.exception_level, self.query
        )
        self.exception_handler.run()

    def _check_format(self, dict_request) -> bool:
        if not isinstance(dict_request, dict):
            self.query.add_error(
                "your request must be in json format", code=config.format_error
            )
            return True
        return False

    def get_protocol(self):
        group_name = self.state.group_name
        protocols = self.ProtocolFactory.get_protocols(group_name)
        if self.query.protocol in protocols:
            protocol = protocols[self.query.protocol]
        else:
            protocol = None
        return protocol

    def update_client_adderss(self, address):
        self.client_address = address
        current_thread().setName(str(address))

    def _add_extra_arguments(self):
        self.query.other["client_address"] = self.client_address
        self.query.other["time"] = time()
