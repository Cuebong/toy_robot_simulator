from classes.Simulator import PointRobot
import pytest


@pytest.fixture
def robot_data():
    robot = PointRobot(robot_name="Toy Robot")
    return robot


@pytest.mark.robot
def test_robot_init(robot_data):
    """
    Test initialisation values of Toy Robot attributes. Uses an error list to capture results of multiple test
    conditions and reports a failed assertion test if any conditions do not return True.
    """
    errors = []
    if not (robot_data.robot_name == 'Toy Robot'):
        errors.append("[FAILURE] Error in robot name assignment.")  # pragma no cover
    if not (robot_data.x == 0):
        errors.append("[FAILURE] Error in robot position X initialisation.")  # pragma no cover
    if not (robot_data.y == 0):
        errors.append("[FAILURE] Error in robot position Y initialisation.")  # pragma no cover
    if not (robot_data.planned_x == 0):
        errors.append("[FAILURE] Error in planned robot position X initialisation.")  # pragma no cover
    if not (robot_data.planned_y == 0):
        errors.append("[FAILURE] Error in planned robot position Y initialisation.")  # pragma no cover
    if not (robot_data.orientation == ""):
        errors.append("[FAILURE] Error in robot orientation initialisation.")  # pragma no cover
    for orientation in ["NORTH", "EAST", "SOUTH", "WEST"]:
        if not (orientation in robot_data.permissible_orientations):
            errors.append(f"[FAILURE] Error in robot permissible orientations initialisation: {orientation} not found.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.robot
def test_robot_plan_move(robot_data):
    """
    Test plan_move method at default XY position (0, 0) for all four possible orientations. Uses the default
    displacement values for X and Y so that the robot moves one unit in the direction it is facing. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    orientations = ["NORTH", "EAST", "SOUTH", "WEST"]
    expected_results_x = [0, 1, 0, -1]
    expected_results_y = [1, 0, -1, 0]
    for i in range(0, len(orientations)):
        robot_data.orientation = orientations[i]
        robot_data.plan_move()
        if not ((robot_data.planned_x == expected_results_x[i])
                and (robot_data.planned_y == expected_results_y[i])):
            errors.append(f"[FAILURE] Error in planned move for orientation {orientations[i]}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.robot
def test_robot_plan_move_with_custom_displacement(robot_data):
    """
        Test plan_move method at default XY position (0, 0) for all four possible orientations. Uses non-default
        displacement values X = 1 and Y = 2. Individual failures are captured in an error list that is checked and
        reported using assert statement.
        """
    errors = []
    orientations = ["NORTH", "EAST", "SOUTH", "WEST"]
    displace_x = 1
    displace_y = 2
    expected_results_x = [1, 2, -1, -2]
    expected_results_y = [2, -1, -2, 1]
    for i in range(0, len(orientations)):
        robot_data.orientation = orientations[i]
        robot_data.plan_move(displace_x, displace_y)
        if not ((robot_data.planned_x == expected_results_x[i]) and
                (robot_data.planned_y == expected_results_y[i])):
            errors.append(f"[FAILURE] Error in planned move for orientation {orientations[i]}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.robot
def test_robot_accept_move(robot_data):
    """
    Test the accept_move method after a plan_move method call to check that the robot's current position is
    updated accordingly.
    """
    robot_data.orientation = "NORTH"
    robot_data.plan_move(displace_x=0, displace_y=1)
    robot_data.accept_move()
    assert (robot_data.x == 0) and (robot_data.y == 1)


@pytest.mark.robot
def test_robot_left(robot_data):
    """
    Test turn_left method for all four possible orientations to check that the resulting orientation matches
    expected results. Individual failures are captured in an error list that is checked and reported using assert
    statement.
    """
    errors = []
    orientations = ["NORTH", "EAST", "SOUTH", "WEST"]
    expected_results = {"NORTH": "WEST", "EAST": "NORTH", "SOUTH": "EAST", "WEST": "SOUTH"}
    for i in range(0, len(orientations)):
        robot_data.orientation = orientations[i]
        robot_data.turn_left()
        if not (robot_data.orientation == expected_results[orientations[i]]):
            errors.append(f"[FAILURE] Error in turning left from orientation {orientations[i]}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.robot
def test_robot_right(robot_data):
    """
    Test turn_right method for all four possible orientations to check that the resulting orientation matches
    expected results. Individual failures are captured in an error list that is checked and reported using assert
    statement.
    """
    errors = []
    orientations = ["NORTH", "EAST", "SOUTH", "WEST"]
    expected_results = {"NORTH": "EAST", "EAST": "SOUTH", "SOUTH": "WEST", "WEST": "NORTH"}
    for i in range(0, len(orientations)):
        robot_data.orientation = orientations[i]
        robot_data.turn_right()
        if not (robot_data.orientation == expected_results[orientations[i]]):
            errors.append(f"[FAILURE] Error in turning right from orientation {orientations[i]}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))
