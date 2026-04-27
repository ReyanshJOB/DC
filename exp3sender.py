import socket
import struct

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

def send():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set TTL (time-to-live)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print("Sender ready...\n")

    while True:
        msg = input("Enter message: ")
        sock.sendto(msg.encode(), (MULTICAST_GROUP, PORT))

if __name__ == "__main__":
    send()