import pytest
from main import execute_commands, read_input_file
from robot import Direction


@pytest.mark.parametrize("input_str,expected_commands", [
	("PLACE 1,2,EAST\nMOVE\nMOVE\nREPORT", [("PLACE", [1, 2, Direction.EAST]), ("MOVE", []), ("MOVE", []), ("REPORT", [])]),
	("PLACE 4,4,EAST\nMOVE\nLEFT\nRIGHT\nREPORT", [("PLACE", [4, 4, Direction.EAST]), ("MOVE", []), ("LEFT", []), ("RIGHT", []), ("REPORT", [])]),
])
def test_read_input_valid(mocker, input_str, expected_commands):
	mocker.patch("builtins.open", mocker.mock_open(read_data=input_str))
	resp = read_input_file('mock/input/file')
	print(resp)
	assert resp == expected_commands


@pytest.mark.parametrize("input_str,expected_commands", [
	("PLACE 1,2,EAST\nRIGHT\nPLACE 1,2,SOUTHEAST\nREPORT", [("PLACE", [1, 2, Direction.EAST]), ("RIGHT", []), ("REPORT", [])]),
	("PLACE 1,EAST\nRIGHT\nPLACE 2,1,SOUTH\nREPORT", [("RIGHT", []), ("PLACE", [2, 1, Direction.SOUTH]), ("REPORT", [])]),
])
def test_read_input_invalid_params(mocker, input_str, expected_commands):
	mocker.patch("builtins.open", mocker.mock_open(read_data=input_str))
	resp = read_input_file('mock/input/file')
	print(resp)
	assert resp == expected_commands


@pytest.mark.parametrize("input_str,expected_commands", [
	("PLACE 1,2,EAST\nUNRECOGNIZED\nMOVE\nLEFT\nREPORT", [("PLACE", [1, 2, Direction.EAST]), ("MOVE", []), ("LEFT", []), ("REPORT", [])]),
	("PLACE 1,2,EAST\nMOVE\nLEFT\nJUMP\nREPORT\nCRAWL", [("PLACE", [1, 2, Direction.EAST]), ("MOVE", []), ("LEFT", []), ("REPORT", [])]),
])
def test_read_input_unknown_command(mocker, input_str, expected_commands):
	mocker.patch("builtins.open", mocker.mock_open(read_data=input_str))
	resp = read_input_file('mock/input/file')
	print(resp)
	assert resp == expected_commands


def test_execute_places(capsys):
	commands = [
		("PLACE", [0, 0, Direction.NORTH]), ("REPORT", []),
		("PLACE", [0, 4, Direction.EAST]), ("REPORT", []),
		("PLACE", [4, 4, Direction.SOUTH]), ("REPORT", []),
		("PLACE", [4, 0, Direction.WEST]), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	assert all_outputs == [
		"0,0,NORTH",
		"0,4,EAST",
		"4,4,SOUTH",
		"4,0,WEST"
	]


def test_execute_horizontal_move(capsys):
	commands = [
		("PLACE", [0, 2, Direction.EAST]), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	# last move should be ignored since the robot is already at the edge
	assert all_outputs == [
		"0,2,EAST",
		"1,2,EAST",
		"2,2,EAST",
		"3,2,EAST",
		"4,2,EAST",
		"4,2,EAST",
	]


def test_execute_vertical_move(capsys):
	commands = [
		("PLACE", [2, 4, Direction.SOUTH]), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
		("MOVE", []), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	# last move should be ignored since the robot is already at the edge
	assert all_outputs == [
		"2,4,SOUTH",
		"2,3,SOUTH",
		"2,2,SOUTH",
		"2,1,SOUTH",
		"2,0,SOUTH",
		"2,0,SOUTH",
	]


def test_execute_square_move(capsys):
	commands = [
		("PLACE", [0, 0, Direction.EAST]), ("REPORT", []),
		("MOVE", []), ("MOVE", []), ("LEFT", []), ("REPORT", []),
		("MOVE", []), ("MOVE", []), ("LEFT", []), ("REPORT", []),
		("MOVE", []), ("MOVE", []), ("LEFT", []), ("REPORT", []),
		("MOVE", []), ("MOVE", []), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	assert all_outputs == [
		"0,0,EAST",
		"2,0,NORTH",
		"2,2,WEST",
		"0,2,SOUTH",
		"0,0,SOUTH",
	]


def test_execute_uturn_move(capsys):
	commands = [
		("PLACE", [1, 2, Direction.EAST]), ("REPORT", []),
		("MOVE", []), ("MOVE", []), ("REPORT", []),
		("RIGHT", []), ("RIGHT", []),("REPORT", []),
		("MOVE", []), ("MOVE", []), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	assert all_outputs == [
		"1,2,EAST",
		"3,2,EAST",
		"3,2,WEST",
		"1,2,WEST",
	]


def test_execute_place_twice(capsys):
	commands = [
		("PLACE", [0, 4, Direction.EAST]), ("REPORT", []),
		("PLACE", [4, 0, Direction.NORTH]), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	assert all_outputs == [
		"0,4,EAST",
		"4,0,NORTH",
	]


def test_execute_ignore_commands(capsys):
	commands = [
		("MOVE", []), ("REPORT", []),
		("LEFT", []), ("REPORT", []),
		("RIGHT", []), ("REPORT", []),
	]
	execute_commands(commands)

	captured = capsys.readouterr()
	all_outputs = captured.out.rstrip().split('\n')

	# output should be empty since the robot was not placed
	assert all_outputs == ['']
