"""
documentation for server class

father class is ThreadingTCPServer
this class implemented tcp server that active with threads thread
for each connection

input:
    server address (Example: ('0.0.0.0', 81))

attributes:
    logger : Logger object from logging module allow to write log file

    address : server address got config file
        and the server activate on this address

    black_list : set of ips that contains wiche ip is allow to connect
"""

import logging
import threading
from socketserver import ThreadingTCPServer

from ..__config__ import server_config as config
from ..__config__ import system_config as sys_config
from ..global_objects.global_object import GlobalObject, GlobalObjectOptions
from ..global_objects import ManagementServerDB
from .RequestHandler import RequestHandler


class Server(ThreadingTCPServer, GlobalObject):

    request_queue_size = config.QUEUE_SIZE

    def __init__(self, address=None):
        if address is None:
            address = (config.IP, config.PORT)

        self.logger = logging.getLogger("Server {}".format(address))
        self.address = address

        self.get_new_connections = config.get_new_connections
        self.check_black_list = config.check_black_list
        self.white_list = set()
        self.black_list = set()

        self.option_object = ServerOptions(self)
        self.DBapi = ManagementServerDB

        self.connections_count = 0

        super(Server, self).__init__(
            self.address, RequestHandler, bind_and_activate=True
        )
        GlobalObject.__init__(self)

    def server_activate(self):
        self.logger.info("setup")
        super().server_activate()

    def verify_request(self, request, client_address) -> bool:
        if not self.get_new_connections:
            return False

        if self.check_black_list:
            if client_address[0] in self.black_list:
                self.logger.info(
                    "{} is on the black list and try to connect".format(client_address)
                )
                return False
            return True
        if client_address[0] not in self.white_list:
            self.logger.info(
                "{} is not on the white list and try to connect".format(client_address)
            )
            return False
        return True

    def shutdown(self):
        self.logger.info("shutdown")
        self.DBapi.close_server(self.address)
        super().shutdown()

    def __setup__(self):
        t = threading.Thread(target=self.serve_forever)
        t.setDaemon(True)  # don't hang on exit
        t.setName("Server thread")
        t.start()
        self.DBapi.open_server(self.address)

    def __finish__(self):
        self.shutdown()

    def get_request(self):
        self.connections_count += 1
        try:
            self.DBapi.new_client(self.address)
        except Exception as ce:
            if sys_config.debug:
                raise ce
        return super().get_request()

    def close_request(self, request):
        self.connections_count -= 1
        try:
            self.DBapi.close_client(self.address)
        except Exception as ce:
            if sys_config.debug:
                raise ce
        super().close_request(request)


class ServerOptions(GlobalObjectOptions):
    def __init__(self, server):
        self.server = server
        self.name = "[server]\n"
        super().__init__()

    def get_black_list(self):
        return self.server.black_list

    def get_white_list(self):
        return self.server.white_list

    def remove_black(self, ip):
        self.server.black_list.remove(ip)

    def add_black(self, ip):
        self.server.black_list.add(ip)

    def add_white(self, ip):
        self.server.white_list.add(ip)

    def remove_white(self, ip):
        self.server.white_list.remove(ip)

    def close_server(self):
        self.server.get_new_connections = False

    def open_server(self):
        self.server.get_new_connections = True

    def check_white_list(self):
        self.server.check_black_list = False

    def check_black_list(self):
        self.server.check_black_list = True

    def status(self):
        return (
            self.name
            + """server open: {}\nconnection count: {}\nwhite list: {}\nblack list: {}""".format(
                self.server.get_new_connections,
                self.server.connections_count,
                self.get_white_list(),
                self.get_black_list(),
            )
        )
