class Action:
	id: str
	device_id: str
	name: str
	description: str
	command: str
	states: list[str]
	current_state: int

	def __init__(self, id, device_id, name, description, command, states, current_state):
		self.id = id
		self.device_id = device_id
		self.name = name
		self.description = description
		self.command = command
		self.states = states
		self.current_state = current_state