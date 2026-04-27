import socket
import pickle

class RPCServer:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


def server_program():
    server = RPCServer()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 6000))
    s.listen(1)

    print("RPC Server: Waiting for client...")

    conn, addr = s.accept()
    print("RPC Server: Client connected from", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        function_name, args = pickle.loads(data)
        print(f"RPC Server: Request -> {function_name}{args}")

        result = getattr(server, function_name)(*args)
        conn.send(pickle.dumps(result))

    conn.close()
    s.close()


if __name__ == "__main__":
    server_program()