from MultiSC.MultiServer.quick_setup.manager import (
    ProtocolsManager,
    MonitorManager,
    Runner,
)

# Simple monitor that print every request
@MonitorManager.add("client_info_printer")
def monitor(self, query):
    print(query)


# Simple protocol that return your name
@ProtocolsManager.add("printer", "name")
def func(query):
    return query["name"]


Server = Runner()
Server.run()
