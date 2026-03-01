from abc import ABC, abstractmethod


class AbstractRobot(ABC):
    """Interface for a generic mobile robot.
    Creates an abstract robot with basic attributes to express current and planned X/Y coordinates, orientation,
    and a reference name.
    This interface defines abstract methods for driving and steering the robot. However, the implementation of these
    abstract methods must be provided by the concrete classes.

    :param robot_name: Reference name to be assigned to instance.
    """

    permissible_orientations = {}
    """: dict[Any, Any]: Stores each possible orientation descriptor as a key value pair with its corresponding
    quantitative angle value (e.g. in degrees)."""
    robot_name = ''
    """: str: Reference name of robot."""
    x = 0
    """: int: The robot's current x position."""
    y = 0
    """: int: The robot's current y position."""
    planned_x = 0
    """: int: The robot's planned x position generated from the plan_move() method."""
    planned_y = 0
    """: int: The robot's planned y position generated from the plan_move() method."""
    orientation = ''
    """: str: The robot's current orientation. This should be a member of permissible_orientations."""

    def __init__(self, robot_name: str = 'Robot') -> None:
        """Object initialisation. Assigns default values to attributes."""
        self.robot_name = robot_name
        self.x = 0
        self.y = 0
        self.planned_x = 0
        self.planned_y = 0
        self.orientation = ""
        self.permissible_orientations = {}

    @abstractmethod
    def plan_move(self):
        """Abstract method for planning a robot move. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def accept_move(self):
        """Abstract method for accepting (and executing) a planned move.
        Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def turn_left(self):
        """Abstract method for steering left. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def turn_right(self):
        """Abstract method for steering right. Implementation to be provided by concrete class."""
        pass  # pragma no cover


class AbstractWorld(ABC):
    """Interface for a generic world. Used to create concrete classes to describe simulator environments.
    The interface provides basic attributes to describe the world's X/Y dimensions, origin, and reference name.
    The world stores information about the robot to be used with its environment and keeps track of whether the
    robot is placed in the world. Implementations for all abstract methods must be provided by the concrete subclass.

    :param robot: Robot object to be used with the world.
    :param world_name: Reference name to be assigned to instance.
    """
    robot = None
    """: AbstractRobot: A robot object that implements the AbstractRobot interface."""
    world_name = 'World'
    """: str: Reference name for the world."""
    size_x = 0
    """: int: The x dimension of the world."""
    size_y = 0
    """: int: The y dimension of the world."""
    origin_x = 0
    """: int: The x coordinate of the world origin."""
    origin_y = 0
    """: int: The y coordinate of the world origin."""
    robot_in_world = False
    """: bool: Flag to indicate the robot is placed in the world when True, otherwise False."""

    def __init__(self, robot: AbstractRobot, world_name: str = 'World') -> None:
        """Object initialisation. Assigns default values to attributes (robot object must be supplied) on creation of
        Object instance.
        """
        self.robot = robot
        self.world_name = world_name
        self.size_x = 0
        self.size_y = 0
        self.origin_x = 0
        self.origin_y = 0
        self.robot_in_world = False

    @abstractmethod
    def place_robot(self, x: int, y: int, f: str):
        """Abstract method for placing a robot into the world. Implementation to be provided by concrete class.

        :param x: X position to place robot.
        :param y: Y position to place robot.
        :param f: Orientation descriptor for placement of robot."""
        pass  # pragma no cover

    @abstractmethod
    def remove_robot(self):
        """Abstract method for removing a robot from the world. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def move_robot(self):
        """Abstract method for moving the robot in the world. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def turn_robot_left(self):
        """Abstract method for steering a robot left in the world. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def turn_robot_right(self):
        """Implementation for steering a robot right in the world. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def report_robot_location(self):
        """Abstract method for reporting the robot's location in the world. Implementation to be provided by concrete
        class."""
        pass  # pragma no cover


class AbstractRequester(ABC):
    """Interface for a generic requester. Used to create concrete classes that provide the implementation for user
    interactions with the simulator. The requester takes requests from the user and sends the request to a simulator
    of type AbstractWorld to interact with its robot.
    It provides abstract methods for receiving a request, verifying integrity of the request, and then sending the
    request for onwards processing by the simulator. The implementation of these methods are provided by the concrete
    subclass.

    :param simulator: The simulator that the requester will send commands to.
    """
    input_counter = 0
    """: int: A running counter for the number of user input requests supplied to the requester."""
    action_counter = 0
    """: int: A running counter for the number of actions accepted by the requester."""
    accepted_commands = []
    """: list[Any]: Stores a list of all recognised commands that the requester will process."""
    quit = False
    """: bool: Flag to indicate if a request to terminate interactions with the simulator has been received."""
    received_request = ''
    """: str: Stores the received request from the user as a string command."""
    command_sent = False
    """: bool: Flag to indicate if the latest received (valid) command has been sent to the simulator."""
    place_request_f = ''
    """: str: Stores the requested robot orientation for a received PLACE command."""
    place_request_y = 0
    """: int: Stores the requested y robot position for a received PLACE command."""
    place_request_x = 0
    """: int: Stores the requested x robot position for a received PLACE command."""
    requested_command = ''
    """: str: Stores the latest validated requested command received from the user."""
    world = None
    """: AbstractWorld: A world object representing the simulator, which implements the AbstractWorld interface."""

    def __init__(self, simulator: AbstractWorld):
        """Object initialisation. Assigns default values to attributes (simulator object must be supplied) on creation
        of Object instance."""
        self.world = simulator
        self.received_request = ""
        self.requested_command = ""
        self.place_request_x = 0
        self.place_request_y = 0
        self.place_request_f = ""
        self.command_sent = False
        self.quit = False
        self.accepted_commands = []
        self.action_counter = 0
        self.input_counter = 0

    @abstractmethod
    def check_request(self) -> bool:
        """
        Abstract method for checking the validity of a request. Implementation to be provided by concrete class.

        :returns: True if request is valid, otherwise False.
        """
        pass  # pragma no cover

    @abstractmethod
    def send_request(self):
        """Abstract method for sending a validated request to the simulator. Implementation to be provided by concrete
        class."""
        pass  # pragma no cover

    @abstractmethod
    def get_request(self):
        """Abstract method for getting a request from the user. Implementation to be provided by concrete class."""
        pass  # pragma no cover

    @abstractmethod
    def run(self):
        """Abstract method for running the Requester. Implementation to be provided by concrete class."""
        pass  # pragma no cover
