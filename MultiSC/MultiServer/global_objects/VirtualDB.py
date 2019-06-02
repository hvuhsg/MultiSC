from .global_object import GlobalObject
from ..DB.MongoDbAPI import MongoDB
from __config__ import db_config as config


class VirtualDBClient(GlobalObject):
    def __init__(self, db_name=None):
        if not db_name:
            db_name = config.virtual_db_name
        self.mongo = MongoDB(
            db_name, config.virtual_db_default_name, config.virtual_db_default_password
        )
        super().__init__()

    def __setup__(self):
        self.mongo.connect()
        super().__setup__()

    def __finish__(self):
        self.mongo.close_connection()
        super().__finish__()
