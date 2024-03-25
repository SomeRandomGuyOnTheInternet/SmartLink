from enum import Enum

class Actions(Enum):
	CONNECT = "smartlink/connect",
	START_LEARNING = "smartlink/start_learning",
	SEND_PACKET = "smartlink/send_packet"

	@classmethod
	def has_value(cls, value):
		values = set(item.value for item in cls)
		return value in values