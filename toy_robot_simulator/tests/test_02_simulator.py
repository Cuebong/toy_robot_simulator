import pytest
from classes.Simulator import PointRobot, TableSimulation


def robot_at_default_xy(simulator_data):
    return (simulator_data.robot.x == 0) & (simulator_data.robot.y == 0)


def robot_at_default_orientation(simulator_data):
    return simulator_data.robot.orientation == ""


@pytest.fixture
def simulator_data():
    toy_robot = PointRobot(robot_name='Toy Robot')
    table_simulator = TableSimulation(robot=toy_robot, world_name='Table Simulator')
    return table_simulator


@pytest.mark.simulator
def test_simulator_init(simulator_data):
    """
    Test instance initialisation to confirm expected default values are assigned to attributes. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    if not (simulator_data.world_name == 'Table Simulator'):
        errors.append("[FAILURE] Error in simulator name assignment.")  # pragma no cover
    if not (simulator_data.size_x == 5):
        errors.append("[FAILURE] Error in initialising Table Simulator x dimensions.")  # pragma no cover
    if not (simulator_data.size_y == 5):
        errors.append("[FAILURE] Error in initialising Table Simulator y dimensions.")  # pragma no cover
    if not (simulator_data.origin_x == 0):
        errors.append("[FAILURE] Error in initialising Table Simulator x coordinate.")  # pragma no cover
    if not (simulator_data.origin_y == 0):
        errors.append("[FAILURE] Error in initialising Table Simulator y coordinate.")  # pragma no cover
    if not (isinstance(simulator_data.robot, PointRobot)):
        errors.append("[FAILURE] Error in assigning PointRobot object.")  # pragma no cover
    if simulator_data.robot_in_world:
        errors.append("[FAILURE] Error in setting initial robot state in world.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_simulator_init_with_args(capsys):
    """
    Test instance initialisation with specified arguments. Checks that the feedback message to Standard Output
    reflects the specified arguments.
    """
    toy_robot = PointRobot(robot_name='Toy Robot')
    TableSimulation(robot=toy_robot, world_name='Table Simulator', dim_x=7, dim_y=8)
    captured = capsys.readouterr()
    assert (captured.out == "[INFO] Table Simulator created with default dimensions [7 x 8] and origin (0, 0).\n")


@pytest.mark.simulator
def test_place_robot(simulator_data):
    """
    Test the place_robot method with a combination of valid place command arguments. Tests include valid boundary values.
    Individual failures are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    x_test_data = list(range(6))
    y_test_data = list(range(6))
    orientation_test_data = ['NORTH', 'EAST', 'SOUTH', 'WEST', 'NORTH', 'EAST']
    for i in range(0, len(x_test_data)):
        x = x_test_data[i]
        y = y_test_data[i]
        f = orientation_test_data[i]
        ret_code = simulator_data.place_robot(x=x, y=y, f=f)
        robot_correct_pose = ((simulator_data.robot.x == x) & (simulator_data.robot.y == y) &
                              (simulator_data.robot.orientation == f))
        if not (ret_code & simulator_data.robot_in_world & robot_correct_pose):
            errors.append(f"[FAILURE] Error placing robot at {x}, {y}, {f}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_place_robot_reject(simulator_data):
    """
    Test the place_robot method with a combination of invalid place command arguments that would lead to the robot
    falling from the table. Arguments have been selected to test boundary conditions. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    x_test_data = [-1, 6, 1, 1, -2, 7]
    y_test_data = [1, 1, -1, 6, -2, 7]
    for i in range(0, len(x_test_data)):
        x = x_test_data[i]
        y = y_test_data[i]
        ret_code = simulator_data.place_robot(x=x, y=y, f='NORTH')
        if ret_code or simulator_data.robot_in_world or not robot_at_default_xy(simulator_data):
            errors.append(f"[FAILURE] Failed to reject place command X={x}, Y={y}, F='NORTH'.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_remove(simulator_data):
    """
    Test the remove method to verify that the robot is removed from the table and position attributes are reset
    to default.
    """
    simulator_data.place_robot(x=3, y=3, f='WEST')
    simulator_data.remove_robot()
    assert (robot_at_default_xy(simulator_data) and robot_at_default_orientation(simulator_data)
            and not simulator_data.robot_in_world)


@pytest.mark.simulator
def test_move(simulator_data):
    """
    Test a series of valid move commands at different initial positions assigned using the place method. The combination
    of valid move commands cover all four possible orientations. Individual failures are captured in an error list
    that is checked and reported using assert statement.
    """
    place_inputs_x = [1, 2, 4, 5]
    place_inputs_y = [4, 3, 1, 0]
    place_inputs_f = ['EAST', 'NORTH', 'SOUTH', 'WEST']
    expected_result_x = [2, 2, 4, 4]
    expected_result_y = [4, 4, 0, 0]
    errors = []
    for i in range(0, len(place_inputs_x)):
        x = place_inputs_x[i]
        y = place_inputs_y[i]
        f = place_inputs_f[i]
        simulator_data.place_robot(x=x, y=y, f=f)
        ret_code = simulator_data.move_robot()
        robot_at_expected_xy = ((simulator_data.robot.x == expected_result_x[i]) &
                                (simulator_data.robot.y == expected_result_y[i]))
        if not (ret_code and robot_at_expected_xy):
            errors.append(f"[FAILURE] Failed to move robot at {x}, {y}, {f}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_move_reject_no_robot(simulator_data):
    """
    Test the move method to ensure it rejects a command if requested without the robot being placed on the table.
    """
    ret_code = simulator_data.move_robot()
    assert not ret_code and robot_at_default_xy(simulator_data) and robot_at_default_orientation(simulator_data)


@pytest.mark.simulator
def test_move_reject_out_of_bounds(simulator_data):
    """
    Test the move method to verify that invalid move requests that would lead to the robot falling from the table
    are rejected. This is tested for all possible 'corner' scenarios of the table. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    place_inputs_x = [0, 0, 0, 0, 5, 5, 5, 5]
    place_inputs_y = [0, 0, 5, 5, 0, 0, 5, 5]
    place_inputs_f = ['SOUTH', 'WEST', 'NORTH', 'WEST', 'SOUTH', 'EAST', 'NORTH', 'EAST']
    errors = []
    for i in range(0, len(place_inputs_x)):
        x = place_inputs_x[i]
        y = place_inputs_y[i]
        f = place_inputs_f[i]
        simulator_data.place_robot(x=x, y=y, f=f)
        ret_code = simulator_data.move_robot()
        robot_at_original_xy = ((simulator_data.robot.x == place_inputs_x[i]) &
                                (simulator_data.robot.y == place_inputs_y[i]))
        if ret_code or not robot_at_original_xy:
            errors.append(f"[FAILURE] Failed to reject robot move at {x}, {y}, {f}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_left_turn(simulator_data):
    """
    Test the turn_robot_left method for all four possible orientations. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    orientations = {'NORTH': 'WEST', 'EAST': 'NORTH', 'SOUTH': 'EAST', 'WEST': 'SOUTH'}
    for i in range(0, len(orientations.keys())):
        f = list(orientations.keys())[i]
        simulator_data.place_robot(x=0, y=0, f=f)
        simulator_data.turn_robot_left()
        if not (simulator_data.robot.orientation == orientations[f]):
            errors.append(f"[FAILURE] Failed to turn robot left at orientation {f}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_left_turn_reject(simulator_data):
    """
    Test the turn_robot_left method to ensure it rejects any commands if the robot has not been placed on the table.
    """
    ret_code = simulator_data.turn_robot_left()
    assert not ret_code and robot_at_default_xy(simulator_data) and robot_at_default_orientation(simulator_data)


@pytest.mark.simulator
def test_right_turn(simulator_data):
    """
    Test the turn_robot_right method for all four possible orientations. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    orientations = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}
    for i in range(0, len(orientations.keys())):
        f = list(orientations.keys())[i]
        simulator_data.place_robot(x=0, y=0, f=f)
        simulator_data.turn_robot_right()
        if not (simulator_data.robot.orientation == orientations[f]):
            errors.append(f"[FAILURE] Failed to turn robot right at orientation {f}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_right_turn_reject(simulator_data):
    """
    Test the turn_robot_right method to ensure it rejects any commands if the robot has not been placed on the table.
    """
    ret_code = simulator_data.turn_robot_right()
    assert not ret_code and robot_at_default_xy(simulator_data) and robot_at_default_orientation(simulator_data)


@pytest.mark.simulator
def test_report(simulator_data, capsys):
    """
    Test the report_robot_location method to verify that it reports correct information to Standard Output. Covers
    all four possible orientations. Individual failures are captured in an error list that is checked and reported
    using assert statement.
    """
    place_inputs_x = [1, 2, 4, 5]
    place_inputs_y = [4, 3, 1, 0]
    place_inputs_f = ['EAST', 'NORTH', 'SOUTH', 'WEST']
    errors = []
    for i in range(0, len(place_inputs_x)):
        x = place_inputs_x[i]
        y = place_inputs_y[i]
        f = place_inputs_f[i]
        simulator_data.place_robot(x=x, y=y, f=f)
        captured = capsys.readouterr()
        ret_code = simulator_data.report_robot_location()
        captured = capsys.readouterr()
        expected_msg = f"[INFO] Toy Robot's current pose in Table Simulator is (X: {x}, Y: {y}, F: {f}).\n"
        if not ret_code or captured.out != expected_msg:
            errors.append(f"[FAILURE] Failed to report robot location at {x}, {y}, {f}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.simulator
def test_report_reject(simulator_data, capsys):
    """
    Test the report_robot_location method to ensure it rejects any commands if the robot has not been placed on the
    table.
    """
    ret_code = simulator_data.report_robot_location()
    captured = capsys.readouterr()
    expected_msg = '[WARNING] Toy Robot has not been placed in Table Simulator. Unable to report robot pose!\n'
    assert not ret_code and (captured.out == expected_msg)
