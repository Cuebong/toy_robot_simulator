import math
from classes.AbstractClasses import AbstractRobot, AbstractWorld


class PointRobot(AbstractRobot):
    """Concrete robot class for a theoretical point robot with no geometry.
    The point robot is able to turn on the spot and advances by one unit according to
    its orientation when requested to move.

    Its orientation is confined to four compass directions: North, East, South, West.
    These are translated to degrees with the clockwise direction as positive, starting
    from 0 degrees when facing North. North is assumed to correspond to the world's
    Y direction.
    """

    def __init__(self, robot_name: str = 'Robot') -> None:
        super().__init__(robot_name)
        # declare permissible headings as a dict for look-up when resolving turning commands
        self.permissible_headings = {'NORTH': 0, 'EAST': 90, 'SOUTH': 180, 'WEST': 270}
        # declare attributes used to temporarily store resulting X/Y from a planned move
        self.planned_x = None
        self.planned_y = None

    def plan_move(self, displace_x: int = 0, displace_y: int = 1) -> None:
        """Applies rotation to desired X and Y translation based on heading and assigns
        to temporary storage attributes."""
        # get current heading and convert angle to radians in right-hand thumb notation
        angle = -1 * self.permissible_headings[self.orientation]*math.pi/180
        # calculate resultant X and Y positions using 2D rotation matrix relationships
        self.planned_x = self.x + int(displace_x*math.cos(angle) - displace_y*math.sin(angle))
        self.planned_y = self.y + int(displace_x*math.sin(angle) + displace_y*math.cos(angle))

    def accept_move(self) -> None:
        """Updates robot X and Y pose using planned move resultant location."""
        if (self.planned_x is not None) & (self.planned_y is not None):
            self.x = self.planned_x
            self.y = self.planned_y

    def turn_left(self) -> None:
        """Turns robot 90 degrees left and updates current orientation, ensuring it is
        within the range of [0, 360)."""
        # Rotation is negative in counter-clockwise direction
        heading = self._wrap_deg(self.permissible_headings[self.orientation] - 90)
        # look-up dictionary and search for corresponding heading angle to update orientation
        self.orientation = list(self.permissible_headings.keys())[list(self.permissible_headings.values()).index(heading)]

    def turn_right(self) -> None:
        """Turns robot 90 degrees right and updates current orientation, ensuring it is
        within the range of [0, 360)."""
        # Rotation is positive in clockwise direction
        heading = self._wrap_deg(self.permissible_headings[self.orientation] + 90)
        # look-up dictionary and search for corresponding heading angle to update orientation
        self.orientation = list(self.permissible_headings.keys())[list(self.permissible_headings.values()).index(heading)]

    # Internal method to wrap values between [0, 360) degrees
    @staticmethod
    def _wrap_deg(val: int) -> int:
        return val % 360


class TableSimulation(AbstractWorld):
    """
    Concrete class object for defining a Table Simulation. It provides proxy methods for commanding
    a robot in the world such that table-imposed constraints are applied to prevent robot moves
    that would lead to it falling from the table.
    """

    def __init__(self, robot: PointRobot, world_name: str = 'Table') -> None:
        super().__init__(robot, world_name)
        self.size_x = 5
        self.size_y = 5
        print(f"[INFO] {self.world_name} created with default dimensions",
              f" [{self.size_x} x {self.size_y}] and origin ({self.origin_x}, {self.origin_y}).")

    def place_robot(self, x: int = 0, y: int = 0, f: str = 'NORTH') -> bool:
        """Checks if the requested place location for the robot is within the dimensions of the
        table. Updates the pose of the robot if it is within dimensions and return True,
        otherwise rejects command and returns False."""
        try:
            assert (x >= self.origin_x) & (x <= self.size_x + self.origin_x)
            assert (y >= self.origin_y) & (y <= self.size_y + self.origin_y)
        except AssertionError:
            print(f"[WARNING] Requested location is out of the bounds of {self.world_name}.",
                  f"Unable to place {self.robot.robot_name} at X: {x}, Y: {y}!")
            return False
        self.robot.x = x
        self.robot.y = y
        self.robot.orientation = f
        self.robot_in_world = True
        print(f"[INFO] {self.robot.robot_name} has been placed in {self.world_name} at (X: {x}, Y: {y}, F: {f}).")
        return True  # command succeeded

    def remove_robot(self) -> None:
        """Resets robot location attributes to None and sets flag to denote robot is no longer on table."""
        self.robot.x = None
        self.robot.y = None
        self.robot.orientation = None
        self.robot_in_world = False
        print(f"[INFO] {self.robot.robot_name} has been removed from {self.world_name}.")

    def move_robot(self) -> bool:
        """Checks if the robot is on the table, and whether a move at its current location
        would lead to it falling from the table. If the planned move is safe, accept the move and return
        True, otherwise return False."""
        if self.robot_in_world:
            self.robot.plan_move()
            # test if planned move would cause robot to fall off the table boundaries
            try:
                assert (self.robot.planned_x >= self.origin_x) & (self.robot.planned_x <= self.size_x + self.origin_x)
                assert (self.robot.planned_y >= self.origin_y) & (self.robot.planned_y <= self.size_y + self.origin_y)
            except AssertionError:
                print(f"[WARNING] Requested move will cause robot to fall out of bounds of {self.world_name}.",
                      f"Unable to move {self.robot.robot_name}!")
                return False
            # move command is safe, accept it
            self.robot.accept_move()
            return True  # command succeeded
        else:
            # robot has not been placed in the world, cannot execute planned move
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}. Unable to move!')
            return False  # command rejected

    def turn_robot_left(self) -> bool:
        """Check if the robot is on the table. If so, carry out the left turn command and return True, otherwise
        return False."""
        if self.robot_in_world:
            self.robot.turn_left()
            return True  # command succeeded
        else:
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}. Unable to turn left!')
            return False  # command rejected

    def turn_robot_right(self) -> bool:
        """Check if the robot is on the table. If so, carry out the right turn command and return True, otherwise
        return False."""
        if self.robot_in_world:
            self.robot.turn_right()
            return True  # command succeeded
        else:
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}. Unable to turn right!')
            return False  # command rejected

    def report_robot_location(self) -> bool:
        """Check if the robot is on the table. If so, report its current pose and return True, otherwise
        return False."""
        if self.robot_in_world:
            print(f"[INFO] {self.robot.robot_name}'s current pose in {self.world_name} is (X: {self.robot.x}, ",
                  f"Y: {self.robot.y}, F: {self.robot.orientation}).")
            return True  # command succeeded
        else:
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}.',
                  ' Unable to report robot pose!')
            return False  # command rejected
