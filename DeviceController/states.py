from enum import Enum

class States(Enum):
	DISCONNECTED = "disconnected",
	DISCOVER_BROADLINK = "discover_broadlink",
	CONNECTED = "connected",
	START_LEARNING = "start_learning",
	STOP_LEARNING = "stop_learning",
	SEND_PACKET = "send_packet"

	@classmethod
	def has_value(cls, value):
		values = set(item.value for item in cls)
		return value in values