from .states import States as states
import broadlink as broadlink
import time

class RemoteClient:
	# Magic numbers
	TICK = 32.84
	TIMEOUT = 30
	IR_TOKEN = 0x26

	state: states
	device: broadlink.Device


	# Main functions
	def configure_broadlink(ssid, password, security_mode):
		print("Setting up Broadlink...")

		broadlink.setup(ssid, password, security_mode)

	def connect_to_device(self):
		print("Discovering devices...")
		devices = []
		while not devices:
			devices = broadlink.discover(timeout=5)
		self.device = devices[0]
		print("Found a device!")
		self.device.auth()
	
	def discover_signal(self):
		start = time.time()
		self.device.enter_learning()
		while time.time() - start < self.TIMEOUT:
			try:   
				packet = self.device.check_data()
				print(packet.hex())
				self.send_signal(self.device, packet)
				# return packet
			except (broadlink.exceptions.ReadError, broadlink.exceptions.StorageError):
				continue
			else:
				break
		else:
			print("No data received...")
			exit(1)

	def send_signal(self, packet):
		self.device.send_data(packet)
		self.discover_signal(self.device)


	# Helper functions
	def auto_int(self, x):
		return int(x, 0)

	def to_microseconds(self, bytes):
		result = []
		#  print bytes[0] # 0x26 = 38for IR
		index = 4
		while index < len(bytes):
			chunk = bytes[index]
			index += 1
			if chunk == 0:
				chunk = bytes[index]
				chunk = 256 * chunk + bytes[index + 1]
				index += 2
			result.append(int(round(chunk * self.TICK)))
			if chunk == 0x0d05:
				break
		return result

	def durations_to_broadlink(self, durations):
		result = bytearray()
		result.append(self.IR_TOKEN)
		result.append(0)
		result.append(len(durations) % 256)
		result.append(len(durations) / 256)
		for dur in durations:
			num = int(round(dur / self.TICK))
			if num > 255:
				result.append(0)
				result.append(num / 256)
			result.append(num % 256)
		return result
	
	def format_durations(self, data):
		result = ''
		for i in range(0, len(data)):
			if len(result) > 0:
				result += ' '
			result += ('+' if i % 2 == 0 else '-') + str(data[i])
		return result


	def parse_durations(self, str):
		result = []
		for s in str.split():
			result.append(abs(int(s)))
		return result