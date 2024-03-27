import argparse
import logging
from command import Command, InvalidParameters, UnknownCommand
from os import path
from robot import Robot, RobotOutOfBoundsError, RobotUnplacedError

logging.basicConfig(format='%(asctime)s|%(module)s|%(levelname)s|%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def read_input_file(filename):
	commands = []
	with open(filename, 'r') as input_file:
		lines = input_file.read().rstrip().splitlines()

		# read commands, discard unknown and invalid commands
		for line in lines:
			try:
				commands.append(Command.parse(line))
			except UnknownCommand as err:
				logger.warning(f"Ignored unknown command '{line}'.")
			except InvalidParameters as err:
				logger.warning(f"Ignored command '{line}' because of invalid parameters.")

	return commands

def execute_commands(commands):
	robot = Robot(5,5)
	for command, parameters in commands:
		try:
			if command == "PLACE":
				robot.place(*parameters)
			elif command == "MOVE":
				robot.move()
			elif command == "LEFT":
				robot.turn_left()
			elif command == "RIGHT":
				robot.turn_right()
			elif command == "REPORT":
				robot.report()

		# ignore commands if they result to errors
		except RobotUnplacedError as err:
			logger.warning(f"Ignored {command} command because robot is not placed on the table yet.")
		except RobotOutOfBoundsError as err:
			logger.warning(f"Ignored {command} command because resulting position is out of the table bounds ({err.xpos},{err.ypos}).")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="This script takes an input file that contains commands for a toy robot, and executes the commands, ignoring invalid ones.")
	parser.add_argument("input_file", help="File containing lines of commands. Empty lines and invalid commands are ignored.")
	args = parser.parse_args()

	# check if input file exists
	if not path.exists(args.input_file):
		print(f"Input file {args.input_file} does not exist!")
		exit()

	commands = read_input_file(args.input_file)
	execute_commands(commands)
