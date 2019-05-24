from global_objects import TEMP_DB as temp_db


class Monitor:
    def __init__(self, name, logger):
        self.logger = logger
        self.name = name

        self.db = temp_db

    def is_active(self):
        return True

    def run_on(self, query):
        if self.is_active():
            try:
                self.setup(query)
                self.handle(query)
                self.finish(query)
            except SkipException as skip:
                self.logger.info("skip {} monitor: {}".format(self.name, skip))

    def setup(self, query):
        pass

    def handle(self, query):
        pass

    def finish(self, query):
        pass

    def log_error(self, error, name=None):
        if name is None:
            name = self.name
        error_msg = "{} {}: {}".format(name, type(error), error)
        self.logger.info(error_msg)


class SkipException(Exception):
    def __init__(self, msg):
        self.msg = msg
