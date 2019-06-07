from socket import socket, AF_INET, SOCK_DGRAM
from __client_config__ import dns_config


class DNSClient(object):
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.dns_address = (dns_config.ip, dns_config.port)

    def get_server_ip(self):
        msg = b"get server address"
        self.sock.sendto(msg, self.dns_address)
        server_address = self.sock.recvfrom(1024)[0].decode()
        server_address = (
            server_address.split(":")[0],
            int(server_address.split(":")[1]),
        )
        return server_address


def test():
    client = DNSClient()
    print(client.get_server_ip())


if __name__ == "__main__":
    test()
