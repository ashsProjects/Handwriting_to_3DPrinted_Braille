import sys
import serial
import time

def send_to_3D_printer(file_path):
    port = 'COM3' #Change this to Ender 3 Pro's port
    baudrate = 115200
    
    # Open serial connection to the printer
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        print("Connected to", ser.name)
        time.sleep(2)
    except serial.SerialException as e:
        print("Failed to connect:", e)
        exit()
    
    # Read the G-code file
    with open(file_path, 'r') as file:
        gcode_commands = file.readlines()
    
    # Send G-code commands to the printer
    for command in gcode_commands:
        ser.write(str.encode(command))
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py <file_path>')
        sys.exit(1)

    g_code_file_path = sys.argv[1]
    
    send_to_3D_printer(g_code_file_path)

