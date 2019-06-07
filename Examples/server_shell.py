from MultiSC.MultiServer.quick_setup.manager import (
    ProtocolsManager,
    MonitorManager,
    Runner,
)

# Simple protocol that run python command
@ProtocolsManager.add("run_command", "command")
def func(query):
    if query["password"] != "runpass12345665":
        return "password wrong!"
    try:
        return eval(query["command"])
    except:
        pass
    try:
        exec(query["command"])
        return "command success"
    except:
        pass
    return "command faild"


Server = Runner()
Server.run()
