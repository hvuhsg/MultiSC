from MultiSC.MultiClient.EasyClient import EasyClient


def main():
    address = "195.154.243.51", 84
    user = EasyClient(address)
    user.connect()

    while True:
        command = input(">>> ")
        if command == "exit":
            break
        print(
            user.castom_request(
                "run_command", "command", command=command, password="runpass12345665"
            )
        )


main()
input("Enter to exit")
