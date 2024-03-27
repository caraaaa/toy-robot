import pytest
from robot import Direction
from command import Command, UnknownCommand, InvalidParameters


@pytest.mark.parametrize("raw_command,expected_command,expected_parameters", [
	("PLACE -1,-1,NORTH", "PLACE", [-1, -1, Direction.NORTH]),
	("PLACE 1,-1,EAST", "PLACE", [1, -1, Direction.EAST]),
	("PLACE -1,1,WEST", "PLACE", [-1, 1, Direction.WEST]),
	("PLACE 1,1,SOUTH", "PLACE", [1, 1, Direction.SOUTH]),
	("MOVE", "MOVE", []),
	("LEFT", "LEFT", []),
	("RIGHT", "RIGHT", []),
	("REPORT", "REPORT", []),
])
def test_parse_valid(raw_command, expected_command, expected_parameters):
	command, parameters = Command.parse(raw_command)

	assert command == expected_command
	assert parameters == expected_parameters

@pytest.mark.parametrize("raw_command,expected_command,expected_parameters", [
	("place -1,-1,NORTH", "PLACE", [-1, -1, Direction.NORTH]),
	("mOvE", "MOVE", []),
	("Left", "LEFT", []),
	("right", "RIGHT", []),
	("REPORT", "REPORT", []),
])
def test_parse_different_case(raw_command, expected_command, expected_parameters):
	command, parameters = Command.parse(raw_command)

	assert command == expected_command
	assert parameters == expected_parameters

@pytest.mark.parametrize("raw_command", [
	("UNPLACE -1,-1,NORTH"),
	("TURN"),
	("JUMP"),
])
def test_parse_unknown_command(raw_command):
	with pytest.raises(UnknownCommand):
		Command.parse(raw_command)


@pytest.mark.parametrize("raw_command", [
	("PLACE -1,-1"),
	("PLACE -5,WEST"),
	("PLACE NORTH"),
	("PLACE 1,1,SOUTHEAST"),
	("PLACE 1,one,EAST"),
])
def test_parse_invalid_place_parameters(raw_command):
	with pytest.raises(InvalidParameters):
		Command.parse(raw_command)
