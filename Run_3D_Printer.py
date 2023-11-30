import subprocess
import serial
import time
import paramiko

def slice_stl_to_gcode():
    #Convert the stl file into gcode using slic3r
    slic3r_path = '"C:\\Users\\Ayush Adhikari\\Documents\\Slic3r\\Slic3r-console.exe"'
    stl_file = 'C:\\Users\\Ayush Adhikari\\Documents\\Handwriting_to_3DPrinted_Braille\\CombinedSTL\\combined_letters.stl'
    command = [slic3r_path, stl_file, '--layer-height 0.2']
    
    try:
        subprocess.run(command, check=True)
        print('Slicing completed successfully')
    except subprocess.CalledProcessError as e:
        print(f'Error {e}')

def send_to_pi():
    pi_ip = ''
    pi_username = ''
    pi_password = ''
    
    local_path = 'CombinedSTL\combined_letters.gcode'
    remote_path = ''
    
    #ssh setup
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        #connect to the Raspberry Pi
        ssh_client.connect(pi_ip, username=pi_username, password=pi_password)

        #create an SFTP client session
        sftp = ssh_client.open_sftp()
        #upload the file to the Raspberry Pi
        sftp.put(local_path, remote_path)
        print(f"File '{local_path}' sent to '{pi_ip}:{remote_path}'")
        #close the SFTP session
        sftp.close()
        
        #execute command on Pi
        command = f'python Send_to_Printer.py {remote_path}'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        print(f'Raspberry Pi command output: {output}')
        
    except paramiko.AuthenticationException as auth_exception:
        print(f"Authentication failed: {auth_exception}")
    except paramiko.SSHException as ssh_exception:
        print(f"SSH connection failed: {ssh_exception}")
    finally:
        #close the SSH connection
        ssh_client.close()
    
   
def main():
    #call slice_stl_to_gcode for slicing
    slice_stl_to_gcode()
    
    #send gcode file to Raspberry Pi and execute a command
    send_to_pi()
    