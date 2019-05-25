import traceback

from .temp_db import TempDB
from .MongoDB import GlobalMongoDbClient
from .VirtualDB import VirtualDBClient
from ..protocols.protocol_factory import Factory
from ..security.serializer import serializer, de_serializer
from .global_object import GLOBAL_OBJECTS
from ..__config__ import db_config as config

__all__ = [
    "TEMP_DB",
    "ManagementServerDB",
    "protocols_factory",
    "SERI",
    "DE_SERI",
    "setup_all",
    "finish_all",
]

#  TempDB global db
TEMP_DB_OBJ = TempDB()
TEMP_DB = TEMP_DB_OBJ.db

#  MongoDB global client
MongoClient = GlobalMongoDbClient(config.db_name)
ManagementServerDB = MongoClient.mongo

# MongoDB virtual db client
VirtualDBObj = VirtualDBClient()
VirtualDB = VirtualDBObj.mongo

#  global protocols factory
protocols_factory = Factory()

#  serializer and de_serializer
SERI = serializer()
DE_SERI = de_serializer()


def setup_all():
    for g_object in GLOBAL_OBJECTS.values():
        try:
            g_object.__setup__()
            print("setup:", g_object)
        except Exception as ex:
            traceback.print_exc()
            print("setup except on {}:".format(g_object), ex)


def finish_all():
    for g_object in GLOBAL_OBJECTS.values():
        try:
            g_object.__finish__()
            print("finish:", g_object)
        except Exception as ex:
            print("finish except:", ex)
