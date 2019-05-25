import logging
from ..DB.TempDB import TempDB


class State(TempDB):
    def __init__(self, group_name=None):
        self.logger = logging.getLogger("State")

        if group_name is None:
            self.group_name = "base_group"  # group of protocols that allowed
        else:
            self.group_name = group_name

        super().__init__()

    def set_group_name(self, group_name):
        self.group_name = group_name
