import subprocess
import paramiko

def slice_stl_to_gcode():
    #Convert the stl file into gcode using slic3r
    slic3r_path = r'C:/Users/TEMP/Documents/Slic3r/Slic3r-console.exe'
    stl_file = r'C:/Users/TEMP/Documents/Visual_Studio_Code/Handwriting_to_3DPrinted_Braille/CombinedSTL/combined_letters.stl'
    command = [slic3r_path, stl_file]
    
    try:
        subprocess.run(command, check=True, shell=True)
        print('Slicing completed successfully')
    except subprocess.CalledProcessError as e:
        print(f'Error {e}')

def send_to_pi():
    pi_ip = '192.168.12.187'
    pi_username = 'dstreeb'
    pi_password = '1428'
    
    local_path = r'CombinedSTL/combined_letters.gcode'
    remote_path = r'/home/pi/gCode/letters.gcode'
    
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
        _, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')
        print(f'Raspberry Pi command output: {output}')
        print(f'Raspberry Pi errors: {errors}')
        
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
    