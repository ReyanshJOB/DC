import socket
import time

def client_program():
    time.sleep(1)  # Wait for server to start

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "127.0.0.1"   # Same as server
    port = 5000

    # Connect to server
    client_socket.connect((host, port))

    # Send message to server
    message = input("Client: Enter message -> ")
    client_socket.send(message.encode())

    # Receive response from server
    response = client_socket.recv(1024).decode()
    print("Client: Received ->", response)

    # Close connection
    client_socket.close()

if __name__ == "__main__":
    client_program()