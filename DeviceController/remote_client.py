from states import States
from broadlink.exceptions import ReadError, StorageError
import broadlink
import time

class RemoteClient:
	TIMEOUT = 30

	state: States
	remote: broadlink.Device


	# Main functions
	def __init__(self):
		self.state = States.DISCONNECTED
		self.remote = None

	def configure_broadlink(self, ssid, password, security_mode):
		print("Setting up Broadlink...")
		broadlink.setup(ssid, password, int(security_mode))
		print("Set up complete!")

	def connect_to_remote(self):
		print("Discovering remotes...")
		remotes = []
		while (not remotes) or (self.state is States.DISCOVER_BROADLINK):
			remotes = broadlink.discover(timeout = 5)
		self.remote = remotes[0]
		print("Found a remote!")
		self.remote.auth()
	
	def discover_command(self):
		print("Checking for signal...")
		start = time.time()
		self.remote.enter_learning()
		while (time.time() - start < self.TIMEOUT) or (self.state is States.START_LEARNING):
			try:   
				packet = self.remote.check_data()
				print("Found signal!")
				print(packet.hex())
				return ''.join(format(x, '02x') for x in bytearray(packet))
			except (ReadError, StorageError):
				continue
			else:
				break
		else:
			print("Signal timed out.")

	def send_command(self, command):
		try:
			print("Trying to send command...")
			print(command)
			self.remote.send_data(bytearray.fromhex(''.join(command)))
			print("Command sent successfully!")
		except Exception as ex:
			print(ex)
			print("Something went wrong.")