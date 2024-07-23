import paramiko
import sqlite3

hostname = "192.168.100.115"
port = 22
username = "ricardo"
password = "@itudobem123"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try: 
    client.connect(hostname, port, username, password)
    test_command = "ls /home"
    stdin, stdout, stderr = client.exec_command(test_command)

    print('Output')
    for line in stdout:
        print(line.strip())

finally:
    client.close()