
import socket

TELLO_IP = "192.168.10.1"
TELLO_PORT = 8889
LOCAL_PORT = 9000

# Create a UDP socket for sending commands
# and receiving command responses
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", LOCAL_PORT))
sock.settimeout(5)

try:
    # Activate SDK mode
    sock.sendto(b"command", (TELLO_IP, TELLO_PORT))
    print("Sent: command")

    # Receive the response
    response, address = sock.recvfrom(1024)
    print("Response:", response.decode().strip())
    print("From:", address)

except socket.timeout:
    print("No response from Tello. Check the Wi-Fi connection.")

except OSError as error:
    print("Socket error:", error)

finally:
    sock.close()


