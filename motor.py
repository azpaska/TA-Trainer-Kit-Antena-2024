import serial
import time

# Set up serial connection
ser = serial.Serial('/dev/ttyACM0', 115200)  # Change '/dev/ttyUSB0' to the appropriate port

# Wait for serial connection to be established
time.sleep(2)

# Function to send G-code commands
def send_command(command):
    # Ensure command ends with newline character
    command += '\n'
    # Send command
    ser.write(command.encode())
    # Wait for response
    while True:
        response = ser.readline().decode().strip()
        if response == 'ok':
            break
        elif response.startswith('error'):
            print("Error:", response)
            break


# Example G-code commands
send_command('G21')  # Set units to millimeters
send_command('G90')  # Set to absolute positioning mode

'''# Initialize X position
x_position = 0.0
returning = x_position / 2

# Move X by 0.1mm 36 times with a delay of 1 second between each move
for _ in range(36):
    x_position += 0.045  # Increment X position by 0.1
    send_command(f'G1 Y{x_position} F0.01')  # Move to new X position at a feed rate of 1 mm/min
    time.sleep(1)  # Add a delay of 1 second
send_command(f'G1 Y-{returning} F0.01')
'''
#send_command(f'G1 Y1.6 F0.1')
#Close serial connection
#ser.close()
