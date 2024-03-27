import pytest
from robot import Robot, Direction, RobotOutOfBoundsError, RobotUnplacedError

@pytest.fixture
def robot():
	'''Returns a Robot unplaced on a 5x5 table'''
	return Robot(5, 5)


def test_new_robot(robot):
	assert robot.xpos == -1
	assert robot.ypos == -1
	assert robot.direction == Direction.UNDEFINED


@pytest.mark.parametrize("x,y,dir", [
	(0, 0, Direction.NORTH),
	(0, 4, Direction.SOUTH),
	(4, 0, Direction.EAST),
	(4, 4, Direction.WEST),
	(2, 2, Direction.WEST),
])
def test_place_valid(robot, x, y, dir):
	robot.place(x, y, dir)

	assert robot.xpos == x
	assert robot.ypos == y
	assert robot.direction == dir


@pytest.mark.parametrize("x,y,dir", [
	(-1, -1, Direction.NORTH),
	(-1, 5, Direction.SOUTH),
	(5, -1, Direction.EAST),
	(5, 5, Direction.WEST),
	(0, -1, Direction.NORTH),
	(0, 5, Direction.SOUTH),
	(5, 0, Direction.EAST),
	(-1, 4, Direction.WEST),
])
def test_place_invalid(robot, x, y, dir):
	with pytest.raises(RobotOutOfBoundsError):
		robot.place(x, y, dir)

		assert robot.xpos == -1
		assert robot.ypos == -1
		assert robot.direction == Direction.UNDEFINED


@pytest.mark.parametrize("initial_x,initial_y,expected_x,expected_y,dir", [
	(0, 0, 0, 1, Direction.NORTH),
	(0, 0, 1, 0, Direction.EAST),
	(4, 4, 4, 3, Direction.SOUTH),
	(4, 4, 3, 4, Direction.WEST),
])
def test_move_valid(robot, initial_x, initial_y, expected_x, expected_y, dir):
	robot.place(initial_x, initial_y, dir)
	robot.move()

	assert robot.xpos == expected_x
	assert robot.ypos == expected_y
	assert robot.direction == dir


@pytest.mark.parametrize("initial_x,initial_y,dir", [
	(4, 4, Direction.NORTH),
	(4, 4, Direction.EAST),
	(0, 0, Direction.SOUTH),
	(0, 0, Direction.WEST),
])
def test_move_invalid(robot, caplog, initial_x, initial_y, dir):
	robot.place(initial_x, initial_y, dir)
	with pytest.raises(RobotOutOfBoundsError):
		robot.move()

		assert robot.xpos == initial_x
		assert robot.ypos == initial_y
		assert robot.direction == dir


def test_move_before_place(robot):
	with pytest.raises(RobotUnplacedError):
		robot.move()

		assert robot.xpos == -1
		assert robot.ypos == -1
		assert robot.direction == Direction.UNDEFINED


@pytest.mark.parametrize("initial_dir,expected_dir", [
	(Direction.NORTH, Direction.WEST),
	(Direction.EAST, Direction.NORTH),
	(Direction.SOUTH, Direction.EAST),
	(Direction.WEST, Direction.SOUTH),
])
def test_left(robot, initial_dir, expected_dir):
	robot.place(0,0,initial_dir)
	robot.turn_left()

	assert robot.direction == expected_dir


def test_left_before_place(robot):
	with pytest.raises(RobotUnplacedError):
		robot.turn_left()

		assert robot.xpos == -1
		assert robot.ypos == -1
		assert robot.direction == Direction.UNDEFINED


@pytest.mark.parametrize("initial_dir,expected_dir", [
	(Direction.NORTH, Direction.EAST),
	(Direction.EAST, Direction.SOUTH),
	(Direction.SOUTH, Direction.WEST),
	(Direction.WEST, Direction.NORTH),
])
def test_right(robot, initial_dir, expected_dir):
	robot.place(0,0,initial_dir)
	robot.turn_right()

	assert robot.direction == expected_dir


def test_right_before_place(robot):
	with pytest.raises(RobotUnplacedError):
		robot.turn_right()

		assert robot.xpos == -1
		assert robot.ypos == -1
		assert robot.direction == Direction.UNDEFINED


@pytest.mark.parametrize("initial_x,initial_y,expected_x,expected_y,dir", [
	(0, 0, 0, 1, Direction.NORTH),
	(0, 0, 1, 0, Direction.EAST),
	(4, 4, 4, 3, Direction.SOUTH),
	(4, 4, 3, 4, Direction.WEST),
])
def test_report(robot, initial_x, initial_y, expected_x, expected_y, dir, capsys):
	robot.place(initial_x, initial_y, dir)
	robot.move()
	robot.report()

	assert capsys.readouterr().out == f"{expected_x},{expected_y},{dir.name}\n"


def test_report_before_place(robot):
	with pytest.raises(RobotUnplacedError):
		robot.report()

		assert robot.xpos == -1
		assert robot.ypos == -1
		assert robot.direction == Direction.UNDEFINED
