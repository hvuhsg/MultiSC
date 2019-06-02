import shutil, errno

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


def main():
    from sys import argv
    if len(argv) != 2:
        print("get one argument <server|client>")
    if argv[1] not in ("server", "client"):
        print("get one argument <server|client>")
    
    if argv[1] == "server":
        copyanything("MultiSC/MultiServer/__config__", "./__config__")
    elif argv[1] == "client":
        copyanything("MultiSC/MultiClient/__client_config__", "./__client_config__")

if __name__ == '__main__':
    main()
