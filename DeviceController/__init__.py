import os
import time
import broadlink
from dotenv import load_dotenv
from server_client import ServerClient
from remote_client import RemoteClient

load_dotenv()
NETWORK_SSID = os.getenv('NETWORK_SSID')
NETWORK_PASSWORD = os.getenv('NETWORK_PASSWORD')
NETWORK_SECURITY = os.getenv('NETWORK_SECURITY')

server_client = ServerClient()
remote_client = RemoteClient()
remote: broadlink.Device

server_client.initialise_connection
remote_client.configure_broadlink(NETWORK_SSID, NETWORK_PASSWORD, NETWORK_SECURITY)
remote_client.connect_to_remote()

while True:
	command = remote_client.discover_command()
	time.sleep(5)
	remote_client.send_command(command)
