from abc import ABC, abstractmethod
from typing import Any


class AbstractRobot(ABC):
    """Abstract class for a mobile robot.
    Creates an abstract robot with unassigned X/Y coordinates, orientation, and a name.
    This class defines abstract methods that must be re-defined (overridden) for any
    concrete robot subclass. These include:
    - plan_move
    - accept_move
    - turn_left
    - turn_right.
    """
    permissible_orientations: dict[Any, Any]

    robot_name: str
    x: int
    y: int
    planned_x: int
    planned_y: int
    orientation: str

    def __init__(self, robot_name: str = 'Robot') -> None:
        """
        Object initialisation
        :type robot_name: str
        """
        self.robot_name = robot_name  # robot name as a string
        self.x = 0  # robot x coordinate as an int
        self.y = 0  # robot y coordinate as an int
        self.planned_x = 0  # robot target x coordinate from planned move as int
        self.planned_y = 0  # robot target y coordinate from planned move as int
        self.orientation = ""  # robot orientation as string
        self.permissible_orientations = {}  # permissible robot orientations

    @abstractmethod
    def plan_move(self):
        """Provide implementation for planning a move action."""
        pass

    @abstractmethod
    def accept_move(self):
        """Provide implementation for accepting a planned move."""
        pass

    @abstractmethod
    def turn_left(self):
        """Provide implementation for turning the robot left."""
        pass

    @abstractmethod
    def turn_right(self):
        """Provide implementation for turning the robot right."""
        pass


class AbstractWorld(ABC):
    """Abstract class for a world in which a robot operates in.
    Creates an abstract world with unassigned X/Y dimensions, zero origin, and a name.
    This class defines abstract methods that must be re-defined (overridden) for
    any concrete world subclass. These include:
    - place_robot
    - remove_robot
    - move_robot
    - report_robot_location.
    """
    robot: AbstractRobot
    world_name: str
    size_x: int
    size_y: int
    origin_x: int
    origin_y: int
    robot_in_world: bool

    def __init__(self, robot: AbstractRobot, world_name: str = 'World') -> None:
        """
        Object initialisation
        :type world_name: str
        :type robot: AbstractRobot
        """
        self.robot = robot  # robot object that will interact with the world
        self.world_name = world_name  # name of the world
        self.size_x = 0  # x dimension of the world as an int
        self.size_y = 0  # y dimension of the world as an int
        self.origin_x = 0  # x coordinate of the origin as an int
        self.origin_y = 0  # y coordinate of the origin as an int
        self.robot_in_world = False  # flag to indicate if robot is placed in world as boolean

    @abstractmethod
    def place_robot(self, x: int, y: int, f: str):
        """Provide implementation for placing a robot in the world.
        :type x: int
        :type y: int
        :type f: str
        """
        pass

    @abstractmethod
    def remove_robot(self):
        """Provide implementation for removing robot from the world."""
        pass

    @abstractmethod
    def move_robot(self):
        """Provide implementation for moving a robot in the world."""
        pass

    @abstractmethod
    def turn_robot_left(self):
        """Provide implementation for turning the robot left."""
        pass

    @abstractmethod
    def turn_robot_right(self):
        """Provide implementation for turning the robot right."""
        pass

    @abstractmethod
    def report_robot_location(self):
        """Provide implementation for reporting the robot location in the world."""
        pass


class AbstractRequester(ABC):
    acceptable_commands: list[Any]
    quit: bool
    received_request: str
    command_sent: bool
    place_request_f: str
    place_request_y: int
    place_request_x: int
    requested_command: str
    world: AbstractWorld

    def __init__(self, simulator: AbstractWorld):
        """
        Object initialisation
        :type simulator: AbstractWorld
        """
        self.world = simulator
        self.received_request = ""
        self.requested_command = ""
        self.place_request_x = 0
        self.place_request_y = 0
        self.place_request_f = ""
        self.command_sent = False
        self.quit = False
        self.acceptable_commands = []  # list of accepted commands for application

    @abstractmethod
    def check_request(self) -> bool:
        """Provide implementation for checking received string request"""
        pass

    @abstractmethod
    def send_request(self):
        """Provide implementation for sending request to world."""
        pass

    @abstractmethod
    def get_request(self):
        """Provide implementation for getting an input request."""
        pass

    @abstractmethod
    def run(self):
        """Provide implementation for running requester application until terminated"""
