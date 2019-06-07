from MultiSC.MultiClient.EasyClient import EasyClient


def main():
    address = "127.0.0.1", 84
    user = EasyClient(address)
    user.connect()

    # Send your name and get it back
    print(user.castom_request("printer", "name", name="mosh"))


main()
input("Enter to exit")
