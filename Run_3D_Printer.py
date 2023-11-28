import subprocess
import serial
import time

def slice_stl_to_gcode():
    #Convert the stl file into gcode using slic3r
    slic3r_path = ''
    stl_file = 'CombinedSTL\combined_letters.stl'
    output_gcode = 'CombinedSTL\output.gcode'
    
    command = [slic3r_path, '-g', stl_file, '--layer-height 0.2', '--output', output_gcode]
    
    try:
        subprocess.run(command, check=True)
        print('Slicing completed successfully')
    except subprocess.CalledProcessError as e:
        print(f'Error {e}')

def send_to_3D_printer():
    port = '' #Change this to Ender 3 Pro's port
    baudrate = 115200
    
    # Open serial connection to the printer
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        print("Connected to", ser.name)
    except serial.SerialException as e:
        print("Failed to connect:", e)
        exit()
    
    # Read the G-code file
    gcode_file = 'CombinedSTL\output.gcode'
    with open(gcode_file, 'r') as file:
        gcode_commands = file.readlines()
    
    # Send G-code commands to the printer
    for command in gcode_commands:
        ser.write(command.strip().encode())
        time.sleep(0.1) #0.1 is delay
    
    #close connection    
    ser.close()
   
def main():
    #call slice_stl_to_gcode for slicing
    slice_stl_to_gcode()
    
    #read gcode and send to printer
    send_to_3D_printer()
    