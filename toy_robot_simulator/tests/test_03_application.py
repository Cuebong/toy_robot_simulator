from classes.UserInterface import Requester, InputErrorCodes
from classes.Simulator import TableSimulation, PointRobot
import pytest


def monkey_patch_get_request(self):
    """
    Overrides the Requester.get_request() method to enable testing of sequences in the run() method without
    requiring user input via Standard Input. Specifies a test sequence to iterate through.
    """
    sequence = ["PLACE 1 1 4 NORTH",  # REJECTED TOO MANY ARGUMENTS
                "place f 5 WEST",  # REJECTED X IS NOT INTEGER
                "PLACE 1 SOUTH",  # REJECTED TOO FEW ARGUMENTS
                "PLACE 3 2 RANDOM",  # REJECTED UNKNOWN F ARGUMENT
                "PLACE 2 4 EAST",  # 2 4 EAST
                "MOVE",  # 3 4 EAST
                "invalid_input",  # REJECTED UNKNOWN COMMAND
                "LEFT",  # 3 4 NORTH
                "Move",  # 3 5 NORTH
                "MOVE",  # REJECTED OUT OF BOUND
                "LeFt",  # 3 5 WEST
                "MOVE",  # 2 5 WEST
                "MOVE unknown_arg",  # REJECTED UNKNOWN ARGUMENT
                "LEFT",  # 2 5 SOUTH
                "MOVE",  # 2 4 SOUTH
                "move",  # 2 3 SOUTH
                "RIghT",  # 2 3 WEST
                "REPORT",  # REPORT 2 3 WEST
                "QUIT"]  # TERMINATE RUN

    self.received_request = sequence[self.input_counter]


@pytest.fixture
def app_data():
    """
    Set up an instance of Requester called application that points to a table simulator and robot object.
    """
    toy_robot = PointRobot(robot_name='Toy Robot')
    table_simulator = TableSimulation(robot=toy_robot, world_name='Table Simulator')
    application = Requester(simulator=table_simulator)
    func_type = type(application.get_request)
    application.get_request = func_type(monkey_patch_get_request, application)  # monkey patch the get_request() method
    return application


@pytest.mark.application
def test_app_init(app_data):
    """
    Test the initialised instance to verify default values have been set to attributes. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    errors = []
    if not isinstance(app_data.world, TableSimulation):
        errors.append("[FAILURE] Error in assigning TableSimulation object in application.")  # pragma no cover
    if not (app_data.received_request == ""):
        errors.append("[FAILURE] Error in initialising received request attribute.")  # pragma no cover
    if not (app_data.requested_command == ""):
        errors.append("[FAILURE] Error in initialising requested command attribute.")  # pragma no cover
    if not (app_data.place_request_x == 0):
        errors.append("[FAILURE] Error in initialising place request x attribute.")  # pragma no cover
    if not (app_data.place_request_y == 0):
        errors.append("[FAILURE] Error in initialising place request y attribute.")  # pragma no cover
    if not (app_data.place_request_f == ""):
        errors.append("[FAILURE] Error in initialising place request f attribute.")  # pragma no cover
    if app_data.command_sent:
        errors.append("[FAILURE] Error in initialising command sent attribute.")  # pragma no cover
    if app_data.quit:
        errors.append("[FAILURE] Error in initialising quit attribute.")  # pragma no cover
    if not (app_data.accepted_commands == ["PLACE", "MOVE", "LEFT", "RIGHT", "REPORT", "QUIT"]):
        errors.append("[FAILURE] Error in initialising accepted commands attribute.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_valid(app_data):
    """
    Test the check_request method to ensure it correctly identifies all valid requests. Individual failures
    are captured in an error list that is checked and reported using assert statement.
    """
    test_strings = ["PLACE 2 4 EAST",
                    "place 1 3 north",
                    "place 0 5 South",
                    "PlaCe 2 4 WeSt",
                    "MOVE",
                    "move",
                    "moVe",
                    "LEFT",
                    "leFt",
                    "RIGHT",
                    "righT"]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.OKAY) or app_data.command_sent:
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_place_nargs_low(app_data):
    """
    Test the check_request method to ensure it correctly identifies errors involving too few arguments being
    supplied for the PLACE command. Individual failures are captured in an error list that is checked and reported
    using assert statement.
    """
    test_strings = ["PLACE 2 EAST",
                    "PLACE 1 3",
                    "PLACE",
                    "PlACE 2"]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.PLACE_NARGS_TOO_LOW):
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_place_nargs_high(app_data):
    """
    Test the check_request method to ensure it correctly identifies errors involving too many arguments being
    supplied for the PLACE command. Individual failures are captured in an error list that is checked and reported
    using assert statement.
    """
    test_strings = ["PLACE 2 2 4 EAST",
                    "PLACE 1 3 WEST 1",
                    "PLACE 4 1 NORTH 0 8",
                    "PlACE 2 3 NORTH SOUTH"]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.PLACE_NARGS_TOO_HIGH):
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_place_xy_not_int(app_data):
    """
    Test the check_request method to ensure it correctly identifies errors involving noninteger values being
    supplied for the PLACE command. Individual failures are captured in an error list that is checked and reported
    using assert statement.
    """
    test_strings = ["PLACE 2 s EAST",
                    "PLACE 1 3.5 NORTH",
                    "PLACE fsf 5 SOUTH",
                    "PlACE 2 _1 WEST"]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.PLACE_XY_NOT_INT):
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_place_f_unknown(app_data):
    """
    Test the check_request method to ensure it correctly identifies errors involving unrecognised F arguments being
    supplied for the PLACE command. Individual failures are captured in an error list that is checked and reported
    using assert statement.
    """
    test_strings = ["PLACE 2 2 EASST",
                    "PLACE 1 3 NOR",
                    "PLACE 0 0 hjhs",
                    "PlACE 2 1 westt"]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.PLACE_F_UNKNOWN):
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_command_args_not_valid(app_data):
    """
    Test the check_request method to ensure it correctly identifies errors involving unrecognised arguments being
    supplied for non-PLACE command. Individual failures are captured in an error list that is checked and reported
    using assert statement.
    """
    test_strings = ["MOVE 2 2 EAST",
                    "MOVE 1 1",
                    "LEFT jhfg",
                    "LEFT 5 1 WEST",
                    "RIGHT 1",
                    "QUIT gfnshfsu",
                    "QUIT 1 5 SOUTH",
                    "jshfushfu 55 1 SOUTH",
                    " ",
                    ]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.COMMAND_ARGS_NOT_VALID):
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_check_request_command_unknown(app_data):
    """
    Test the check_request method to ensure it correctly identifies errors involving unrecognised commands being sent.
    Individual failures are captured in an error list that is checked and reported using assert statement.
    """
    test_strings = ["",
                    "Pace",
                    "MOVEIT",
                    "fggh",
                    "1",
                    "_$%£&"]
    errors = []
    for string in test_strings:
        app_data.received_request = string
        if not (app_data.check_request() == InputErrorCodes.COMMAND_UNKNOWN):
            errors.append(f"[FAILURE] Failed to correctly process received string request {string}.")  # pragma no cover
    assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.application
def test_app_send_request_place(app_data):
    """
    Test the send_request method with a valid PLACE command to verify that the robot executes the requested command.
    """
    app_data.requested_command = "PLACE"
    app_data.place_request_x = 4
    app_data.place_request_y = 0
    app_data.place_request_f = 'SOUTH'
    app_data.command_sent = False
    app_data.send_request()
    assert (app_data.world.robot_in_world and app_data.world.robot.x == 4 and app_data.world.robot.y == 0
            and app_data.world.robot.orientation == 'SOUTH')


@pytest.mark.application
def test_app_send_request_move(app_data):
    """
    Test the send_request method with a valid MOVE command to verify that the robot executes the requested command.
    """
    app_data.world.place_robot(x=0, y=0, f='NORTH')
    app_data.requested_command = "MOVE"
    app_data.command_sent = False
    app_data.send_request()
    assert (app_data.world.robot.x == 0 and app_data.world.robot.y == 1 and app_data.world.robot.orientation == 'NORTH')


@pytest.mark.application
def test_app_send_request_left(app_data):
    """
    Test the send_request method with a valid LEFT command to verify that the robot executes the requested command.
    """
    app_data.world.place_robot(x=0, y=0, f='NORTH')
    app_data.requested_command = "LEFT"
    app_data.command_sent = False
    app_data.send_request()
    assert (app_data.world.robot.x == 0 and app_data.world.robot.y == 0 and app_data.world.robot.orientation == 'WEST')


@pytest.mark.application
def test_app_send_request_right(app_data):
    """
    Test the send_request method with a valid RIGHT command to verify that the robot executes the requested command.
    """
    app_data.world.place_robot(x=0, y=0, f='NORTH')
    app_data.requested_command = "RIGHT"
    app_data.command_sent = False
    app_data.send_request()
    assert (app_data.world.robot.x == 0 and app_data.world.robot.y == 0 and app_data.world.robot.orientation == 'EAST')


@pytest.mark.application
def test_app_send_request_report(app_data, capsys):
    """
    Test the send_request method with a valid REPORT command to verify that the simulator reports the position of the
    robot to Standard Output.
    """
    app_data.world.place_robot(x=3, y=4, f='WEST')
    app_data.requested_command = "REPORT"
    app_data.command_sent = False
    captured = capsys.readouterr()
    app_data.send_request()
    captured = capsys.readouterr()
    expected_msg = "[INFO] Toy Robot's current pose in Table Simulator is (X: 3, Y: 4, F: WEST).\n"
    assert captured.out == expected_msg


@pytest.mark.application
def test_app_send_request_quit(app_data, capsys):
    """
    Test the send_request method with a valid QUIT command to verify that the quit attribute is correctly set.
    """
    app_data.requested_command = "QUIT"
    app_data.command_sent = False
    app_data.send_request()
    assert app_data.quit


@pytest.mark.application
def test_app_send_request_resend(app_data, capsys):
    """
    Test the send_request method with a MOVE request while the command sent flag is set to confirm it does not
    re-send the MOVE command.
    """
    app_data.world.place_robot(x=0, y=0, f='NORTH')
    app_data.requested_command = "MOVE"
    app_data.command_sent = True
    app_data.send_request()
    assert (app_data.world.robot.x == 0 and app_data.world.robot.y == 0 and app_data.world.robot.orientation == 'NORTH')


@pytest.mark.application
def test_app_run(app_data, capsys):
    """
    Test the run method using the pre-defined test sequence specified in the monkey_patch_get_request() override
    method. Capsys is disabled to allow output messages from the application to display on the test console. The test
    checks that the final position and orientation of the robot matches the expected result, which will reflect both
    correct acceptance of valid commands and correct rejection of invalid commands.
    """
    with capsys.disabled():
        print("\n ------------------------------------------------ "
              "\n[TEST INFO] Application test run output messages:"
              "\n ------------------------------------------------ ")
        app_data.run()
    assert (app_data.world.robot.x == 2 and app_data.world.robot.y == 3 and app_data.world.robot.orientation == 'WEST')
