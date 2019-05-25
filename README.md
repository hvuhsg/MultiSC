# MultiServer 

<p align="center">
<a href=""><img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg" alt="awesome"></a>
<a href="https://badge.fury.io/py/mit"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT"></a>
<a href="https://badge.fury.io/py/pypi"><img src="https://badge.fury.io/py/pypi.svg" alt="PyPI version"></a>
<a href=""><img src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" alt="coverage"></a>
<a href=""><img src="https://img.shields.io/badge/code%20quality-A-brightgreen.svg" alt="quality"></a>
</p>

### Server for your app needs.

#### **Quick setup example (server)**
```
from MultiServer.quick_setup.manager import ProtocolsManager, MonitorManager, Runner


@MonitorManager.add("client_info_printer")
def monitor(self, query, **kwargs):
    print(query.other)

@ProtocolsManager.add("math", "sum")
def func2(query):
    return query["a"] + query["b"]


Server = Runner()
Server.run()
```

#### **client example**
```
from MultiClient.EasyClient import EasyClient

def main():
    address = "127.0.0.1", 84
    user = EasyClient(address)
    user.connect()

    print(user.castom_request("math", "sum", a=5, b=9)) # -> {'message': 14, 'code': 200}
main()
```
