import serial
import time

class MotorController:
    def __init__(self, serial_device='/dev/ttyACM0', serial_baudrate=115200):
        self.serial_device = serial_device
        self.serial_baudrate = serial_baudrate
        self.connection = None

    def connect(self):
        self.connection = serial.Serial()
        self.connection.port = self.serial_device
        self.connection.baudrate = self.serial_baudrate
        self.connection.timeout = 1
        self.connection.dtr = 0  # don't reset controller when connecting
        try:
            self.connection.open()
        except Exception as e:
            print("Failed to connect to motor controller on {:s}\nCheck the port settings\n".format(self.connection.port), e)
            raise e
        connect_msg = ""
        connect_tries = 10
        while connect_msg.strip() == "" and connect_tries > 0:
            connect_msg = self.connection.readline().decode('ascii')
            connect_tries -= 1 
        print("Connect response: ", connect_msg)
        self.connection.write(("G1 F500\n").encode())  # Set feedrate to 500 units/s max
        response = self.connection.readline().decode('ascii')
        print("Set feedrate response: ", response)
        if connect_msg.find("Grbl 1.1f") < 0 or connect_tries == 0 or response[:2] != "ok":
            self.connection.close()
            self.connection = None
            return False
        else:
            self.connection.reset_input_buffer()
            self.connection.reset_output_buffer()
            return True

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def is_connected(self):
        return self.connection is not None and self.connection.is_open

    def send_command(self, command):
        if not self.connection:
            raise Exception("Not connected to motor controller")
        # Ensure command ends with newline character
        command += '\n'
        # Send command
        self.connection.write(command.encode())
        # Wait for response
        while True:
            response = self.connection.readline().decode().strip()
            if response == 'ok':
                break
            elif response.startswith('error'):
                print("Error:", response)
                break
