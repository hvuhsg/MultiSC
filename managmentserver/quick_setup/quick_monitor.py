import logging


class QuickMonitor:
    def __init__(self, monitor_function, name):
        self.monitor_function = monitor_function
        self.logger = logging.getLogger(name)
        self.monitor_actions = {
            "CloseConnection": CloseConnectionAction(),
            "BlockClient": BlockClientAction(),
        }
        self.db = dict()
        self.handle = monitor_function  # main function

    def run_on(self, query):
        self.monitor_function(self, query)

    def is_active(self):
        return True


class MonitorAction:
    def start_action(self, query):
        self.run(query)

    def run(self, query):
        raise NotImplementedError  # abstract class


class CloseConnectionAction(MonitorAction):
    def run(self, query):
        from Exceptions.CloseConnection import CloseConnection

        raise CloseConnection


class BlockClientAction(MonitorAction):
    def run(self, query):
        query.change_settings(setting_name="block socket", new_value=True)
