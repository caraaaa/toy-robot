import logging
from enum import Enum

logger = logging.getLogger(__name__)

class Direction(Enum):
	UNDEFINED = -1
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

class RobotOutOfBoundsError(Exception):
	def __init__(self, xpos, ypos):
		self.xpos = xpos
		self.ypos = ypos
		self.message = f"Trying to place robot beyond the table bounds ({xpos},{ypos})."
		super().__init__(self.message)

class RobotUnplacedError(Exception):
	def __init__(self):
		self.message = f"Trying to place move robot that is not placed on the table."
		super().__init__(self.message)

class Robot:
	def __init__(self, table_width, table_height):
		logger.info(f"Creating robot to move around a {table_width}x{table_height} table.")

		self.xpos = -1
		self.ypos = -1
		self.direction = Direction.UNDEFINED
		
		self.table_width = table_width
		self.table_height = table_height

	def place(self, xpos, ypos, dir):
		logger.info(f"Placing robot on {xpos},{ypos}, facing {dir.name}")

		# if place coordinate is beyond table bounds, raise an error
		if (xpos < 0 or
	  		xpos >= self.table_width or
			ypos < 0 or
			ypos >= self.table_height):
			raise RobotOutOfBoundsError(xpos, ypos)

		self.xpos = xpos
		self.ypos = ypos
		self.direction = dir

	def move(self):
		logger.info(f"Moving robot 1 unit to {self.direction.name}.")

		# if the robot is not yet on the table
		# or the resulting coordinate is beyond table bounds, raise an error
		if self.direction == Direction.UNDEFINED:
			raise RobotUnplacedError
		elif self.direction == Direction.NORTH:
			if self.ypos >= self.table_height - 1:
				raise RobotOutOfBoundsError(self.xpos, self.ypos + 1)
			self.ypos += 1
		elif self.direction == Direction.EAST:
			if self.xpos >= self.table_width - 1:
				raise RobotOutOfBoundsError(self.xpos + 1, self.ypos)
			self.xpos += 1
		elif self.direction == Direction.SOUTH:
			if self.ypos <= 0:
				raise RobotOutOfBoundsError(self.xpos, self.ypos - 1)
			self.ypos -= 1
		elif self.direction == Direction.WEST:
			if self.xpos <= 0:
				raise RobotOutOfBoundsError(self.xpos - 1, self.ypos)
			self.xpos -= 1

	def turn_left(self):
		logger.info(f"Rotating robot 90 degress to the left.")

		# if the robot is not yet on the table, raise an error
		if self.direction == Direction.UNDEFINED:
			raise RobotUnplacedError

		new_dir = (self.direction.value - 1) % 4
		self.direction = Direction(new_dir)

	def turn_right(self):
		logger.info(f"Rotating robot 90 degress to the right.")

		# if the robot is not yet on the table, raise an error
		if self.direction == Direction.UNDEFINED:
			raise RobotUnplacedError

		new_dir = (self.direction.value + 1) % 4
		self.direction = Direction(new_dir)

	def report(self):
		# if the robot is not yet on the table, raise an error
		if self.direction == Direction.UNDEFINED:
			raise RobotUnplacedError

		print(self)

	def __str__(self):
		return f"{self.xpos},{self.ypos},{self.direction.name}"
