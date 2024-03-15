import os
from dotenv import load_dotenv
from .states import States as states
from .server_client import ServerClient
from .remote_client import RemoteClient


server = ServerClient()
remote = RemoteClient()
device: RemoteClient.broadlink.Device

server.initialise_connection
remote.connect_to_device