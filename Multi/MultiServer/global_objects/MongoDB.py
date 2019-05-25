from .global_object import GlobalObject, GlobalObjectOptions
from ..DB.MongoDbAPI import MongoDB
from ..__config__ import db_config as config


class GlobalMongoDbClient(GlobalObject):
    def __init__(self, db_name=None):
        if not db_name:
            db_name = config.db_name
        self.mongo = MongoDB(db_name)
        self.connect = False
        self.option_object = GlobalMongoDbClientOptions(self)
        super().__init__()

    def __setup__(self):
        self.mongo.connect()
        self.connect = True
        super().__setup__()

    def __finish__(self):
        self.mongo.close_connection()
        self.connect = False
        super().__finish__()


class GlobalMongoDbClientOptions(GlobalObjectOptions):
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.name = "[mongo client]\n"
        super().__init__()

    def status(self):
        return self.name + """connect: {}""".format(self.mongo_client.connect)
