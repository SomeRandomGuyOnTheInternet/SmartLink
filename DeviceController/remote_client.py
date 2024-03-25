from actions import Actions
from command import Command
from remote_exception import RemoteException
from broadlink.exceptions import ReadError, StorageError
import broadlink
import time

class RemoteClient:
	TIMEOUT = 30

	action: Actions
	remote: broadlink.Device

	# Main functions
	def __init__(self):
		self.action = Actions.DISCONNECT
		self.remote = None

	def configure_broadlink(self, ssid, password, security_mode):
		print("Setting up Broadlink...")
		broadlink.setup(ssid, password, int(security_mode))
		print("Set up complete!")

	def connect_to_remote(self):
		print("Discovering remotes...")
		remotes = []
		remotes = broadlink.discover(timeout = 5)
		if remotes:
			self.remote = remotes[0]
			print("Found a remote!")
			self.remote.auth()
			return self.remote
		else:
			print("Could not find a remote.")
			raise RemoteException("NoRemoteFound")		

	
	def discover_command(self):
		if self.remote != None:
			print("Checking for signal...")
			start = time.time()
			self.remote.enter_learning()
			while (time.time() - start < self.TIMEOUT) or (self.action is Actions.START_LEARNING):
				try:   
					packet = self.remote.check_data()
					print("Found signal!")
					print(packet.hex())
					command_str = ''.join(format(x, '02x') for x in bytearray(packet))
					return command_str
				except (ReadError, StorageError):
					continue
			else:
				print("Signal timed out.")
				raise RemoteException("NoSignalFound")

	def send_command(self, command: str):
		try:
			print("Trying to send command...")
			print(command)
			self.remote.send_data(bytearray.fromhex(''.join(command)))
			print("Command sent successfully!")
		except Exception as ex:
			print(ex)
			print("Something went wrong while sending command.")
			raise RemoteException("CannotSendCommand")