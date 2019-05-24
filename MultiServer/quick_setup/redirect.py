# redirect python managementserver path
def root_dir_update():
    import sys
    import os

    base_dir = "\\".join(__file__.split("\\")[:-2])
    sys.path.append(base_dir)
    os.chdir(base_dir)
    return base_dir


base_dir = root_dir_update()


import __config__.system_config as config

config.root_path = base_dir
config.switch_to_root_path = True


def start_quick_setup_mod():
    config.quick_setup_mod = True
