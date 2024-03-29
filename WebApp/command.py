class Command:
	id: str
	device_id: str
	name: str
	description: str
	command: str

	def __init__(self, id, device_id, name, description, command):
		self.id = id
		self.device_id = device_id
		self.name = name
		self.description = description
		self.command = command