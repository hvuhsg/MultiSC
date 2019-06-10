import shutil
import argparse


def copyanything(src, dst):
    shutil.copytree(src, dst)


def main():
    from os import path
    from sys import argv

    dir_path = path.dirname(__file__)

    parser = argparse.ArgumentParser(description='Create new Multi project <server|client>.')
    parser.add_argument("ProjectType",
            choices=["server", "client"],
            help="Project type to create.")
    parser.add_argument("-q", "--quick", const=True, action="store_const")
    args = parser.parse_args()

    try:
        if args.ProjectType == "server":
            copyanything(path.join(dir_path, "MultiServer/__config__"), "./__config__")
            if args.quick:
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
        elif args.ProjectType == "client":
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
