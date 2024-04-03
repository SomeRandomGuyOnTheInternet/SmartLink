from action import Action

class Device:
	id: str
	name: str
	description: str
	commands: list[Action]

	def __init__(self, id: str, name: str, description: str, actions: list[Action]):
		self.id = id
		self.name = name
		self.description = description
		self.actions = actions

	