import socket
import time


class DjiTello:
    def __init__(self, video=False, log=None, verbose=False):
        self.TELLO_IP = "192.168.10.1"
        self.TELLO_PORT = 8889
        self.TELLO_VIDEO_PORT = 11111
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", 9000))
        self.sock.settimeout(10.0)
        self.log = log

       
    def send_command(self, command):
        """Send command and wait for its response"""
        try:
            destination = (self.TELLO_IP, self.TELLO_PORT)
            print(f"Sending {command!r} to {destination}")

            self.sock.sendto(command.encode("utf-8"), destination)

            data, server = self.sock.recvfrom(1024)
            response = data.decode("utf-8").strip()
            return response

        except socket.timeout:
            print(f"Timeout: {command}")
            return None

        except OSError as e:
            print(f"Socket error: {e}")
            return None

    def setup(self):
        return self.send_command("command")

    def takeoff(self):
        return self.send_command("takeoff")

    def land(self):
        return self.send_command("land")

    def move_up(self, cm):
        cm = int(cm)
        if not 20 <= cm <= 500:
            raise ValueError("Movement distance must be 20–500 cm")
        return self.send_command(f"up {cm}")

    def move_down(self, cm):
        cm = int(cm)
        if not 20 <= cm <= 500:
            raise ValueError("Movement distance must be 20–500 cm")
        return self.send_command(f"down {cm}")

    def move_forward(self, cm):
        cm = int(cm)
        if not 20 <= cm <= 500:
            raise ValueError("Movement distance must be 20–500 cm")
        return self.send_command(f"forward {cm}")

    def move_back(self, cm):
        cm = int(cm)
        if not 20 <= cm <= 500:
            raise ValueError("Movement distance must be 20–500 cm")
        return self.send_command(f"back {cm}")

    def move_left(self, cm):
        cm = int(cm)
        if not 20 <= cm <= 500:
            raise ValueError("Movement distance must be 20–500 cm")
        return self.send_command(f"left {cm}")

    def move_right(self, cm):
        cm = int(cm)
        if not 20 <= cm <= 500:
            raise ValueError("Movement distance must be 20–500 cm")
        return self.send_command(f"right {cm}")

    def rotate_clockwise(self, degrees):
        degrees = int(degrees)
        if not 1 <= degrees <= 360:
            raise ValueError("Rotation must be 1–360 degrees")
        return self.send_command(f"cw {degrees}")

    def rotate_counter_clockwise(self, degrees):
        degrees = int(degrees)
        if not 1 <= degrees <= 360:
            raise ValueError("Rotation must be 1–360 degrees")
        return self.send_command(f"ccw {degrees}")

    def send_rc(self, left_right, forward_back, up_down, yaw):
        """Send continuous RC control; do not wait for a reply."""
        values = [int(v) for v in
                  (left_right, forward_back, up_down, yaw)]

        if any(v < -100 or v > 100 for v in values):
            raise ValueError("RC values must be between -100 and 100")

        command = f"rc {values[0]} {values[1]} {values[2]} {values[3]}"
        try:
            self.sock.sendto(
                command.encode("utf-8"),
                (self.TELLO_IP, self.TELLO_PORT)
            )
        except OSError as e:
            print(f"Socket error: {e}")

    def get_battery(self):
        return self.send_command("battery?")

        try:
            self.sock.sendto(
                command.encode("utf-8"),
                (self.TELLO_IP, self.TELLO_PORT)
            )
        except OSError as e:
            print(f"Socket error: {e}")

    def close(self):
        self.sock.close()


if __name__ == "__main__":

    drone = DjiTello()

    try:
        print("Connecting to Tello EDU...")
        response = drone.setup()

        if response == "ok":
            print("Connected to Tello EDU")
            print("Battery:", drone.get_battery(), "%")
            print(drone.takeoff())
            print(drone.move_up(30))
            print(drone.move_forward(100))
            print(drone.rotate_clockwise(180))
            print(drone.move_forward(50))
            print(drone.land())
        else:
            print("Tello didn't confirm command mode.")

    finally:
        drone.close()