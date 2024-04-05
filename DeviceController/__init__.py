import os
import socket
from dotenv import load_dotenv
from server_client import ServerClient
from remote_client import RemoteClient

load_dotenv(override=True)
NAME = os.getenv('NAME')
HOSTNAME = os.getenv('HOSTNAME')
PORT = int(os.getenv('PORT'))

remote_client = RemoteClient()
server_client = ServerClient("server-client", NAME, HOSTNAME, PORT, remote_client)
try:
	server_client.initialise()
except socket.timeout as e:
	print("Something went wrong while initialising MQTT connection.")
	print("Double check the hostname and port number.")

# remote_client.connect_to_remote()
# while True:
# 	command = remote_client.discover_command()
# 	time.sleep(5)
# 	remote_client.send_command(command)
