from abc import ABC, abstractmethod


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

    def __init__(self, robot_name: str = 'Robot') -> None:
        self.robot_name = robot_name  # robot name as a string
        self.x = None  # robot x coordinate as an int
        self.y = None  # robot y coordinate as an int
        self.planned_x = None  # robot target x coordinate from planned move as int
        self.planned_y = None  # robot target y coordinate from planned move as int
        self.orientation = None  # robot orientation as string

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

    def __init__(self, robot: AbstractRobot, world_name: str = 'World') -> None:
        self.robot = robot  # robot object that will interact with the world
        self.world_name = world_name  # name of the world
        self.size_x = None  # x dimension of the world as an int
        self.size_y = None  # y dimension of the world as an int
        self.origin_x = 0  # x coordinate of the origin as an int
        self.origin_y = 0  # y coordinate of the origin as an int
        self.robot_in_world = False  # flag to indicate if robot is placed in world as boolean

    @abstractmethod
    def place_robot(self):
        """Provide implementation for placing a robot in the world."""
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
