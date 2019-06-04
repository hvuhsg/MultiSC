import shutil, errno

def copyanything(src, dst):    
    shutil.copytree(src, dst)



def main():
    from os import path
    from sys import argv
    
    dir_path = path.dirname(__file__)
    
    if len(argv) != 2:
        print("get one argument <server|client>")
    if argv[1] not in ("server", "client"):
        print("get one argument <server|client>")
    
    if argv[1] == "server":
        copyanything(path.join(dir_path, "MultiServer/__config__") , "./__config__")
    elif argv[1] == "client":
        copyanything(path.join(dir_path, "MultiClient/__client_config__"), "./__client_config__")

if __name__ == '__main__':
    main()
