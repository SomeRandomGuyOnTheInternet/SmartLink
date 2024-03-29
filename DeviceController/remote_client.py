import time
import broadlink
from broadlink.exceptions import ReadError, StorageError
from remote_exception import RemoteException

class RemoteClient:
	TIMEOUT = 30
	
	remote: broadlink.Device

	# Main functions
	def __init__(self):
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
			raise RemoteException("NoRemoteFound", "No remotes were found")		

	
	def discover_command(self):
		if self.remote != None:
			print("Checking for signal...")
			start = time.time()
			self.remote.enter_learning()
			while (time.time() - start < self.TIMEOUT):
				try:   
					packet = self.remote.check_data()
					print("Found signal!")
					print(packet.hex())
					command_str = ''.join(format(x, '02x') for x in bytearray(packet))
					return command_str
				except broadlink.exceptions.NetworkTimeoutError:
					print("Network timed out.")
					raise RemoteException("NoSignalFound", "Could not find any signal")
				except (ReadError, StorageError):
					continue
			else:
				print("Signal timed out.")
				raise RemoteException("NoSignalFound", "Could not find any signal")

	def send_command(self, command: str):
		try:
			print("Trying to send command...")
			print(command)
			self.remote.send_data(bytearray.fromhex(''.join(command)))
			print("Command sent successfully!")
		except Exception as ex:
			print(ex)
			print("Something went wrong while sending command.")
			raise RemoteException("CannotSendCommand", "Could not send command")
