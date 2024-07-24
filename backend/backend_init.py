import paramiko
from constants import Constants

'''def init_backend():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try: 
        client.connect(Constants.HOSTNAME, Constants.PORT, Constants.USERNAME, Constants.PASSWORD)
        #test_command = "ls /home"
        #stdin, stdout, stderr = client.exec_command(test_command)


    finally:
        client.close()'''

class BackendClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = Constants.HOSTNAME
        self.port = Constants.PORT
        self.username = Constants.USERNAME
        self.password = Constants.PASSWORD
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.hostname, self.port, self.username, self.password)
        except Exception as e:
            print(f"Failed to connect: {e}")

    def close(self):
        self.client.close()

# Initialize the BackendClient with your constants
backend_client = BackendClient()


