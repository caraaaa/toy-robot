# Toy Robot Coding Challenge

### Overview
This application is a simulation of a toy robot moving on a square table top, of dimensions 5 units x 5 units with no obstructions. The robot is free to roam around the surface of the table, but must be prevented from falling to destruction. **Any movement that would result in the robot falling from the table must be prevented, however further valid movement commands must still be allowed.**

#### Commands
* `PLACE <xpos>,<ypos>,<direction>` - Put the toy robot on the table in position X,Y and facing NORTH, SOUTH, EAST or WEST.
* `MOVE` - Move the toy robot one unit forward in the direction it is currently facing.
* `LEFT` - Rotate the robot 90 degrees in the specified direction without changing its position.
* `RIGHT` - Put the toy robot on the table in position X,Y and facing NORTH, SOUTH, EAST or WEST.
* `REPORT` - Announce the X,Y and F of the robot in the following format: `<xpos>,<ypos>,<direction>`

For the purpose of this exercise, commands are **not case-sensitive**.

### Requirements

This app requires the following:
* python 3.10 (tested under Python 3.10.12)

To run the tests, the following requirements must also be installed:
* pytest 8.1.1
* pytest-mock 3.14.0

To install:
```
pip install -r requirements.txt
```


### How to run

#### App
Usage:
```
usage: main.py [-h] input_file

This script takes an input file that contains commands for a toy robot, and executes the commands,
ignoring invalid ones.

positional arguments:
  input_file  File containing lines of commands. Empty lines and invalid commands are ignored.

options:
  -h, --help  show this help message and exit
```

Sample input file:
```
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
```

Example:
```
$ python3 main.py test_input.txt
3,3,NORTH
3,4,NORTH
3,4,NORTH
```

#### Tests
To run tests, simply run `pytest`.

Example:
```
$ pytest
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.1.1, pluggy-1.4.0
rootdir: /home/cara/codes/toy-robot
plugins: mock-3.14.0
collected 72 items

command_test.py .....................                                    [ 29%]
main_test.py .............                                               [ 47%]
robot_test.py ......................................                     [100%]

============================== 72 passed in 0.89s ==============================
```

### Future considerations and improvements
* Support for table variable table dimension (may be part of the input file)
