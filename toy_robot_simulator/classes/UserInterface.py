from classes.AbstractClasses import AbstractRequester, AbstractWorld
from enum import Enum


class InputErrorCodes(Enum):
    """
    An Enumerator class to define error codes associated with parsing of user input strings. Checks are carried
    out by the check_request() method within the Requester class, which returns the corresponding error code.
    Only when the error code return is OKAY does the command get sent to the simulator.
    """
    OKAY = 0  # doc: Input has been validated and can be used.
    PLACE_NARGS_TOO_LOW = 1  # doc: Not enough arguments supplied for PLACE command.
    PLACE_NARGS_TOO_HIGH = 2  # doc: Too many arguments supplied for PLACE command.
    PLACE_XY_NOT_INT = 3  # doc: X and/or Y argument supplied for PLACE command is not an Integer.
    PLACE_F_UNKNOWN = 4  # doc: F argument supplied for PLACE command is not a recognised orientation.
    COMMAND_ARGS_NOT_VALID = 5  # doc: Unexpected arguments have been supplied for given command.
    COMMAND_UNKNOWN = 6  # doc: Requested command is not recognised.


class Requester(AbstractRequester):
    """
    Concrete class implementation of the AbstractRequester interface. This implementation uses the Standard Input
    as the interface for users to input string commands to the simulator.

    This Requester exposes the following commands to the user: PLACE, MOVE, LEFT, RIGHT, REPORT, and QUIT. The
    interaction with the user begins when the run() method is called, which cycles through a continuous loop that
    requests an input from the user via Standard Input, validates the input, then sends the command to the loaded
    simulator. This loops continues until a valid QUIT command is received.

    The Requester returns error messages back to the user via the Standard Output whenever an invalid request is
    received. On these instances, no commands are sent to the simulator.

    :param simulator: The target simulator that the Requester sends received commands to.
    """

    accepted_commands = ["PLACE", "MOVE", "LEFT", "RIGHT", "REPORT", "QUIT"]
    """: list[str]: The list of accepted commands that this Requester will process."""

    def __init__(self, simulator: AbstractWorld):
        """
        Object initialisation. Assigns default values to attributes (the simulator must be specified).
        """
        super().__init__(simulator)
        self.accepted_commands = ["PLACE", "MOVE", "LEFT", "RIGHT", "REPORT", "QUIT"]

    def check_request(self) -> InputErrorCodes:
        """
        Checks a received string request stored in its received_request attribute and returns an error code if the
        supplied string does not meet accepted formats for a given command. If valid, the command is assigned to
        the requested_command attribute and the command_sent attribute is updated to notify the send_request() method
        that the current request has not been sent to the simulator.

        :returns: The associated error code for the received string request.
        """
        inputs = self.received_request.split(" ")
        if inputs[0].upper() == "PLACE":
            if len(inputs) < 4:
                return InputErrorCodes.PLACE_NARGS_TOO_LOW
            elif len(inputs) > 4:
                return InputErrorCodes.PLACE_NARGS_TOO_HIGH
            else:
                try:
                    self.place_request_x = int(inputs[1])
                    self.place_request_y = int(inputs[2])
                    if inputs[3].upper() in self.world.robot.permissible_orientations:
                        self.place_request_f = inputs[3].upper()
                    else:
                        return InputErrorCodes.PLACE_F_UNKNOWN
                except ValueError:
                    return InputErrorCodes.PLACE_XY_NOT_INT
                self.requested_command = "PLACE"
        else:
            if len(inputs) != 1:
                return InputErrorCodes.COMMAND_ARGS_NOT_VALID
            elif inputs[0].upper() in self.accepted_commands:
                self.requested_command = inputs[0].upper()
            else:
                return InputErrorCodes.COMMAND_UNKNOWN
        self.command_sent = False
        return InputErrorCodes.OKAY

    def send_request(self):
        """
        Sends a validated request command to the simulator and increments the action counter. Sets the quit flag
        if a QUIT command has been received.
        """
        if not self.command_sent:
            match self.requested_command:
                case "PLACE":
                    self.world.place_robot(self.place_request_x, self.place_request_y, self.place_request_f)
                case "MOVE":
                    self.world.move_robot()
                case "LEFT":
                    self.world.turn_robot_left()
                case "RIGHT":
                    self.world.turn_robot_right()
                case "REPORT":
                    self.world.report_robot_location()
                case "QUIT":
                    self.quit = True
            self.action_counter += 1
            self.command_sent = True

    def get_request(self):
        """
        Gets a string request from the user via Standard Input. A message is displayed when user input is requested
        to provide instructions on how the string request should be formatted.
        """
        self.received_request = input("\n-------------------------------------------------------\n" +
                                      "\nPlease enter one of the following commands:" +
                                      "\n\t- PLACE [X: int] [Y: int] [F: {NORTH, EAST, SOUTH, WEST}]" +
                                      "\n\t- MOVE" +
                                      "\n\t- LEFT" +
                                      "\n\t- RIGHT" +
                                      "\n\t- REPORT" +
                                      "\n\t- QUIT" +
                                      "\n\nEnter Command: ")  # pragma no cover

    def run(self):
        """
        Runs the Requester's main business logic to initiate and maintain interaction with the user and simulator.
        Terminates when the quit flag is set by the send_request() method.

        Error messages are displayed to the user via Standard Output if received requests are invalid.
        """
        print(f"[INFO] {self.world.world_name} has been set up and ready to receive commands.")
        self.quit = False

        while not self.quit:
            self.get_request()
            self.input_counter += 1
            ret_code = self.check_request()
            match ret_code:
                case InputErrorCodes.OKAY:
                    self.send_request()
                case InputErrorCodes.PLACE_NARGS_TOO_LOW:
                    print("[ERROR] Too few arguments have been supplied for PLACE command. Please try again.")
                case InputErrorCodes.PLACE_NARGS_TOO_HIGH:
                    print("[ERROR] Too many arguments have been supplied for PLACE command. Please try again.")
                case InputErrorCodes.PLACE_XY_NOT_INT:
                    print("[ERROR] X and/or Y arguments for PLACE command must be integer values. Please try again.")
                case InputErrorCodes.PLACE_F_UNKNOWN:
                    print("[ERROR] Supplied F argument for PLACE command is not recognised. Please try again.")
                case InputErrorCodes.COMMAND_ARGS_NOT_VALID:
                    print("[ERROR] Unexpected arguments for requested command. Please try again without arguments.")
                case InputErrorCodes.COMMAND_UNKNOWN:
                    print("[ERROR] Command not valid. Please try again.")
        print("[INFO] QUIT command received. Application is terminating...")
