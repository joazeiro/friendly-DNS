import paramiko
from constants import Constants
from flask import Flask,jsonify

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try: 
    client.connect(Constants.HOSTNAME, Constants.PORT, Constants.USERNAME, Constants.PASSWORD)
    #test_command = "ls /home"
    #stdin, stdout, stderr = client.exec_command(test_command)


finally:
    client.close()