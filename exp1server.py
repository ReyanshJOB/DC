import socket

def server_program():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "127.0.0.1"   # Localhost
    port = 5000

    # Bind socket to address
    server_socket.bind((host, port))

    # Start listening
    server_socket.listen(1)
    print("Server: Waiting for connection...")

    # Accept connection
    conn, addr = server_socket.accept()
    print("Server: Connected to", addr)

    # Receive message from client
    message = conn.recv(1024).decode()
    print("Server: Received ->", message)

    # Send response to client
    response = input("Server: Enter response -> ")
    conn.send(response.encode())

    # Close connection
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    server_program()