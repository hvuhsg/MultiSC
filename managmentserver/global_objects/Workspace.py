from global_objects import GLOBAL_OBJECTS
from global_objects.global_object import GlobalObject, GlobalObjectOptions
from DB.TempDB import TempDB

from threading import Thread, current_thread
from setup import start_event


class WorkspaceManager(GlobalObject):
    def __init__(self):
        self.global_objects = GLOBAL_OBJECTS
        self.active = False
        self.db = TempDB()
        self._connections = []  # number of active threads
        self.option_object = WorkspaceOptions(self)

        super().__init__()

    def __setup__(self):
        self.active = True  # default
        t = Thread(target=self.run)
        t.setDaemon(True)
        t.setName("WorkspaceManager")
        t.start()

    def __finish__(self):
        self.active = False

    def run(self):
        start_event.wait()
        while True:
            command = self.read_command()
            res, run_ok = self.run_command(command, is_master_shell=True)
            if run_ok:
                print(res)
            else:
                print(res)  # print error

    def read_command(self):
        command = input(">>> ")
        return command

    def run_command(self, command, is_master_shell=False):
        self._connections.append(current_thread())
        if not self.is_allow(is_master_shell):
            return "Workspace isn't active now.", False

        return self._run_command(command)

    def _run_command(self, command):
        if not self.db.is_init():
            self.init_db()
        db = self.db

        try:
            try:
                return str(eval(command)), True
            except SyntaxError:
                exec(command)  # return None
                return "Ok done.", True
        except Exception as ex:
            res = "Error: {}, {}".format(type(ex), ex)
            return res, False

    def init_db(self):
        for name, obj in self.global_objects.items():
            if hasattr(obj, "option_object"):
                obj = obj.option_object
            self.db[name] = obj

    def is_allow(self, is_shell_master):
        return self.active or is_shell_master

    def show(self, lis=None):
        if lis is None:
            lis = self.global_objects
        output = ""
        output += "{}{}{}\n".format("--" * 10, "LIST", "--" * 10)
        for obj in sorted(lis):
            output += "{}{}".format(obj, "\n")
        output += "{}{}{}\n".format("--" * 10, "LIST", "--" * 10)
        return output

    def set(self, global_object_name):
        if global_object_name in self.global_objects:
            if hasattr(self.global_objects[global_object_name], "option_object"):
                self.db["obj"] = self.global_objects[global_object_name].option_object
                return "Ok self.db['obj'] is now your object"
            return "{} not have option object".format(global_object_name)
        return "{} is not in the global objects list".format(global_object_name)

    def options(self):
        if "obj" not in self.db:
            return "set object first with set function."

        options_list = self.db["obj"].options()
        return options_list

    def connection_count(self):
        count = 0
        for connection in self._connections:
            if connection.is_alive():
                count += 1
        return count

    def status(self):
        res = ""
        for name, objectt in self.global_objects.items():
            if hasattr(objectt, "option_object"):
                option_object = getattr(objectt, "option_object")
                if hasattr(option_object, "status"):
                    res += (
                        option_object.status()
                        + "\n------------------------------------\n"
                    )
        return res


class WorkspaceOptions(GlobalObjectOptions):
    def __init__(self, workspace):
        self.workspace = workspace
        self.name = "[workspace]\n"
        super().__init__()

    def lock(self):
        self.workspace.active = False

    def unlock(self):
        self.workspace.active = True

    def status(self):
        return self.name + """shell active: {}\nactive connections count: {}""".format(
            self.workspace.active, self.workspace.connection_count()
        )
