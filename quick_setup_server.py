from Multi.MultiServer.quick_setup.manager import ProtocolsManager, MonitorManager, Runner


@MonitorManager.add("client_info_printer")
def monitor(self, query, **kwargs):
    logger = None
    if "logger" in kwargs:
        logger = kwargs['logger']
    if logger:
        logger.info(query.other)
    else:
        print(query.other)
    #self.monitor_actions["CloseConnection"].start_action()


@ProtocolsManager.add("printer", "name")
def func(query):
    return query["name"]


@ProtocolsManager.add("math", "sum")
def func2(query):
    return query["a"] + query["b"]


Server = Runner()
Server.run()
