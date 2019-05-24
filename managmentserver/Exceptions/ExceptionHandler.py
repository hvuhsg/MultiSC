import logging
import __config__.protocol_code_config as config
import __config__.system_config as sys_config
from .MainException import MainException
from Exceptions.TestException import TestException
from pymongo.errors import PyMongoError
from Handlers.catch_events_handler import CatchEventsHandler


class ExceptionHandler:
    def __init__(self, function, level, query=None):
        self.logger = logging.getLogger("ExceptionHandler")
        self.logger.addHandler(CatchEventsHandler())
        self.function = function
        self.query = query
        self.level = level
        self.debug = sys_config.debug

    def run(self):
        error = None
        error_code = None
        try:
            self.function()

        except PyMongoError as DBerror:
            error = "{}: {}".format("Database error", DBerror)
            error_code = config.db_error
            self.logger.error(error)

        except TestException as TE:
            error = "{}: {}".format("TestException", TE)
            error_code = config.server_error
            self.logger.info(error)

        except MainException as ME:
            if ME.level < self.level:
                raise ME
            else:
                error = "{}: {}".format(type(ME), ME)
                error_code = ME.error_code
                self.logger.info(error)

        except Exception as ex:
            error = "{}: {}".format(
                "ServerError", "something is wrong!. but we don't know what"
            )
            error_code = config.server_error
            if self.debug:
                self.logger.debug(ex)
                raise ex
            else:
                self.logger.exception(ex)

        if self.query and error:
            self.query.add_error(error, code=error_code)
