import os
import time
import broadlink
from device import Device
from command import Command
from db_context import DBContext
from dotenv import load_dotenv
from server_client import ServerClient
from remote_client import RemoteClient

load_dotenv(override=True)
NETWORK_SSID = os.getenv('NETWORK_SSID')
NETWORK_PASSWORD = os.getenv('NETWORK_PASSWORD')
NETWORK_SECURITY = int(os.getenv('NETWORK_SECURITY'))
HOSTNAME = os.getenv('HOSTNAME')
PORT = int(os.getenv('PORT'))

print(NETWORK_SSID)

remote_client = RemoteClient()
server_client = ServerClient("123asd", HOSTNAME, PORT, remote_client)

remote_client.configure_broadlink(NETWORK_SSID, NETWORK_PASSWORD, NETWORK_SECURITY)
remote_client.connect_to_remote()

while True:
	command = remote_client.discover_command()
	time.sleep(5)
	remote_client.send_command(command)