from typing import List
from command import Command

class Device:
	id: str
	name: str
	description: str
	commands: List[Command]

	def __init__(self, id: str, name: str, description: str, commands: List[Command]):
		self.id = id
		self.name = name
		self.description = description
		self.commands = commands

	