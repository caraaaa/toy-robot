import logging
import re
from robot import Direction

logger = logging.getLogger(__name__)

class InvalidParameters(Exception):
	def __init__(self, command, params):
		self.command = command
		self.params = params
		self.message = f"Invalid parameters for {command} command. Format must be: {params}."
		super().__init__(self.message)

class UnknownCommand(Exception):
	def __init__(self, command):
		self.command = command
		self.message = f"Unknown command {command}."
		super().__init__(self.message)

class Command:
	def parse(input_str):
		command = input_str.upper().split(" ")
		parameters = []

		if command[0] == "PLACE":
			param_pattern = r"^(-{0,1}[0-9]+),(-{0,1}[0-9]+),(NORTH|EAST|SOUTH|WEST)$"
			params = re.match(param_pattern, command[1])

			if not params:
				raise InvalidParameters(command[0], "<x_pos>,<y_pos>,<direction>")

			parameters.append(int(params.group(1)))
			parameters.append(int(params.group(2)))
			parameters.append(Direction[params.group(3)])

		elif command[0] not in ["MOVE", "LEFT", "RIGHT", "REPORT"]:
			raise UnknownCommand(command[0])
					
		return command[0], parameters
