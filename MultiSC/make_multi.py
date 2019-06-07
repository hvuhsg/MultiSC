import shutil


def copyanything(src, dst):
    shutil.copytree(src, dst)


def main():
    from os import path
    from sys import argv

    dir_path = path.dirname(__file__)

    if len(argv) < 2 or argv[1] not in ("server", "client"):
        print("get one argument <server|client>")

    try:
        if argv[1] == "server":
            copyanything(path.join(dir_path, "MultiServer/__config__"), "./__config__")
            if len(argv) > 2 and argv[2] in ("--quick", "-q"):
                shutil.copyfile(
                    path.join(dir_path, "Examples/simple_quick_server.py"),
                    "./simple_quick_server.py",
                )
            else:
                copyanything(path.join(dir_path, "Examples/protocols"), "./protocols")
                shutil.copyfile(
                    path.join(dir_path, "Examples/simple_server.py"),
                    "./simple_server.py",
                )
        elif argv[1] == "client":
            copyanything(
                path.join(dir_path, "MultiClient/__client_config__"),
                "./__client_config__",
            )
            shutil.copyfile(
                path.join(dir_path, "Examples/simple_client.py"), "./simple_client.py"
            )
    except Exception as ex:
        print("files already exist...", ex)
    else:
        print("create project successfuly")


if __name__ == "__main__":
    main()
