import sys
import os
from xml.dom.minidom import parse
import paramiko
#from scp import SCPClient
import sys
from datetime import time
import subprocess

 Define a function to create an SSH client
def create_ssh_client(ip, username, password):
    print(f"Open ssh connection to remote {ip}")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    return client

# Define a function to copy a file to a remote destination
# def copy_file_to_remote(ssh_client, local_path, remote_path):
#     remote_file_path = os.path.join(remote_directory, os.path.basename(local_path))
#     print(f"copying {local_path} to remote {remote_file_path}")

#     with SCPClient(ssh_client.get_transport()) as scp:
#         scp.put(local_path, remote_file_path)

def create_directory_if_not_exists(ssh_client, directory):
    stdin, stdout, stderr = ssh_client.exec_command(f'mkdir -p {directory}')
    exit_status = stdout.channel.recv_exit_status()  # Blocking call
    if exit_status == 0:
        print(f"Directory '{directory}' created or already exists.")
    else:
        print(f"Failed to create directory '{directory}'. Error: {stderr.read().decode()}")



    ip_addresses = list()

        for interface in interface_list:
            if interface.getElementsByTagName("usage")[0].firstChild.nodeValue == "management":
                ip_address = interface.getElementsByTagName("ip-address")[0].firstChild.nodeValue
                ip_addresses.append(ip_address)

                ping_command = "ping -c 1 -w 1 " + ip_address + " > /dev/null"
                print(f" {ping_command}" , end = " ")
                ping_result = os.system(ping_command)

                if (ping_result != 0):
                    print(f" - failed to connect to machine  {ip_address}")
                    DpeIP_BadStatusList.append(ip_address)
                    continue
                else:
                    print(f" - successful")

    


def CreateFile(ipp_index):

    file_name = f"ConfigureKafka_on_IPP-{ipp_index}.sh"
    file_path = os.path.join(local_directory, file_name)

    print(f"Creating {file_path}")

    # Create and close the file
    with open(file_path, 'w+') as file:
        file.write("#!/bin/sh\n")
        file.write(f"{CLI} << EOF \n")
        file.write(f"configure\n")

        for command in commands:
            replaced_text = command.replace('xx', str(ipp_index))
            #print(f"replaced_text = {replaced_text}")
            file.write(f"{replaced_text}\n")

        file.write(f"commit\n")
        file.write(f"exit\n")
        file.write(f"EOF\n")
        file.close()
        # Get the current permissions using the stat module
        current_permissions = os.stat(file_path).st_mode
        # Add execute permissions for user, group, and others
        os.chmod(file_path, current_permissions | 0o111)
        print(f"will return {file_path}")
        return file_path



def CommitFile(file_path):
    p = subprocess.Popen(['/bin/bash', file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    print(f" output : {output}\n error: {err} \n result code = {rc}")

    print(f"Successfully comitted to confd {file_path} ")


def main():
    # Check if the command line argument is provided
    # if len(sys.argv) != 3:
    #     print("Incorrect usage: python script.py <number_of_files> <dpe_password>")

    # if len(sys.argv) = 2:
    #     print("Incorrect usage: python script.py <dpe_password>")
    #     sys.exit(1)

    passw = ""
    if len(sys.argv) == 2:
        # Try to convert the command line argument to an integer
        try:
            #n = int(sys.argv[1])
            #passw = str(sys.argv[2])
            passw = str(sys.argv[1])
        except ValueError as e :
            print(f"The argument must be appropriate type: {e}")
            sys.exit(1)

           
            
            # try:
            #     print(f"Trying to copy {file_path} to addres  {address}")
            #     # Create an SSH client for the current IP
            #     ssh_client = create_ssh_client(address, "root", passw)
            #     create_directory_if_not_exists(ssh_client,remote_directory)
            #     # Copy the file to the remote destination
            #     copy_file_to_remote(ssh_client, file_path, remote_directory)
            #     # Close the SSH client
            #     ssh_client.close()

            #     print(f"File copied to {address} successfully.")
            # except Exception as e:
            #     print(f"Failed to copy file to {address}. Error: {e}")


if __name__ == "__main__":
    main()
