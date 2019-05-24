"""
documentation for connectionHandler class

father class is BaseRequestHandler
this class implemented connection handler options like setup, handle, finish

input:
    request as connection : socket
    client_address : the client ip and port
    server : server object that active this connection handler

attributes:
    logger : Logger object from logging module allow to write log file

    connection : socket

    client_address : ip, port

    server : server object

    settings : dict for all the connection settings like (timeout, recv count)

    security_handler : SecurityHandler object.
        allow to secure connection by exchange keys, encrypt and decrypt

    protocol_handler : ProtocolHandler object. allow to communicate
        with protocols objects
"""

import logging
from socket import timeout
from socketserver import BaseRequestHandler
from threading import current_thread

import __config__.request_handler_config as config
from Exceptions.CloseConnection import CloseConnection
from protocols.ProtocolHandler import ProtocolManager
from security.SecurityHandler import SecurityHandler
from global_objects import SERI, DE_SERI
from Handlers.catch_events_handler import CatchEventsHandler

__all__ = ["RequestHandler"]


class RequestHandler(BaseRequestHandler):
    def __init__(self, connection, client_address, server):
        self.logger = logging.getLogger("RequestHandler")
        self.logger.addHandler(CatchEventsHandler())
        current_thread().setName(str(client_address))

        self.connection = connection
        self.client_address = client_address
        self.server = server
        self.settings = {
            "timeout": config.TIMEOUT_DEFAULT,
            "recv": config.MAX_RECV_IN_ONE_TIME,
        }
        self.proxy_data = None
        self.update_to_proxy_data = False
        self.security_handler = SecurityHandler(self)
        self.protocol_handler = ProtocolManager(self.client_address)

        super().__init__(connection, client_address, server)

    def setup(self):
        self.connection.settimeout(self.settings["timeout"])
        self.logger.info("setup handler")
        try:
            if config.SECURITY:
                self.security_handler.secure_connection()
        except ConnectionError as ex:
            self.logger.debug("secure connection exception, {}".format(ex))

    def handle(self):
        try:
            self.handle_loop()
        except ConnectionError as ex:
            self.logger.error("connection error: {} {}".format(type(ex), ex))
        except timeout:
            self.logger.info("timed out error")
        except CloseConnection as err:
            self.logger.info("socket closed, {}".format(str(err)))
        except Exception as ex:
            self.logger.exception(ex)

    def handle_loop(self):
        while True:
            data = self.recv(self.settings["recv"])
            if not data:  # if connection is closed
                break
            self.update_client_address()
            result = self.protocol_handler.run(
                data
            )  # result is Query object from protocols package
            self.send(result.get_response())
            self.update_settings(result.settings)  # update socket settings

    def recv(self, num):
        self.proxy_data = None
        recv_data = self.connection.recv(num)
        if not recv_data:  # if connection if closed
            return recv_data
        client_data, proxy_data = self.split_recv_data(recv_data)
        if proxy_data:
            proxy_data = DE_SERI(proxy_data)
        if self.security_handler.is_secure:
            client_data = self.security_handler.decrypt(client_data)
            client_data = DE_SERI(client_data)
            self.proxy_data = proxy_data
            self.logger.info(
                "proxy_data: {} client sent: {}".format(proxy_data, client_data)
            )
            return client_data
        if not config.SECURITY:
            client_data = DE_SERI(client_data)
            self.logger.info(
                "proxy_data: {} client sent: {}".format(proxy_data, client_data)
            )
        return client_data

    def send(self, message):
        if self.security_handler.is_secure:
            self.logger.info("server sent: {}".format(message))
            message = SERI(message)
            message = self.security_handler.encrypt(message)
        elif not config.SECURITY:
            message = SERI(message)
        self.connection.send(message)

    def finish(self):
        self.logger.info("finish")

    def update_settings(self, result_settings):
        self.settings.update(result_settings)
        self.connection.settimeout(self.settings["timeout"])
        if "block socket" in result_settings:
            if result_settings["block socket"]:
                self.server.black_list.add(self.client_address[0])
                raise CloseConnection("socket blocked.")

    def split_recv_data(self, data):
        proxy_data = ""
        if config.DATA_SPLITER in data:
            data, proxy_data = data.split(config.DATA_SPLITER)
        return data, proxy_data

    def update_client_address(self):
        if not self.proxy_data:
            return
        if self.update_to_proxy_data:
            return

        if "client_address" not in self.proxy_data:
            return

        self.protocol_handler.update_client_adderss(self.proxy_data["client_address"])
        self.update_to_proxy_data = True
