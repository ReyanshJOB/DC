import socket
import pickle
import time

def client_program():
    time.sleep(1)

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("127.0.0.1", 6000))

    while True:
        print("\n--- RPC Client Menu ---")
        print("1. Add")
        print("2. Multiply")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "3":
            print("Exiting client...")
            break

        if choice not in ["1", "2"]:
            print("Invalid choice!")
            continue

        try:
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
        except ValueError:
            print("Please enter valid numbers!")
            continue

        if choice == "1":
            request = ("add", (a, b))
        else:
            request = ("multiply", (a, b))

        # Send request
        c.send(pickle.dumps(request))

        # Receive result
        result = pickle.loads(c.recv(1024))
        print("Result =", result)

    c.close()


if __name__ == "__main__":
    client_program()