from classes.AbstractClasses import AbstractRequester, AbstractWorld
from enum import Enum


class InputErrorCodes(Enum):
    """
    Enumerator class to define user input error codes
    0 - input is OKAY
    1 - not enough arguments supplied for PLACE command
    2 - too many arguments supplied for PLACE command
    3 - X and/or Y argument supplied for PLACE command is not an Integer
    4 - F argument supplied for PLACE command is not a recognised string
    5 - Supply of arguments not valid for given command
    6 - Requested command is not recognised
    """
    OKAY = 0
    PLACE_NARGS_TOO_LOW = 1
    PLACE_NARGS_TOO_HIGH = 2
    PLACE_XY_NOT_INT = 3
    PLACE_F_UNKNOWN = 4
    COMMAND_ARGS_NOT_VALID = 5
    COMMAND_UNKNOWN = 6


class Requester(AbstractRequester):

    accepted_commands: list[str]

    def __init__(self, simulator: AbstractWorld):
        """
        Object initialisation
        :type simulator: AbstractWorld
        """
        super().__init__(simulator)
        self.accepted_commands = ["PLACE", "MOVE", "LEFT", "RIGHT", "REPORT", "QUIT"]

    def check_request(self) -> InputErrorCodes:
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
