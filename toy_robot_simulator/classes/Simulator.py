import math
from classes.AbstractClasses import AbstractRobot, AbstractWorld


class PointRobot(AbstractRobot):
    """Concrete robot class for a theoretical point robot with no geometry.
    The point robot is able to turn on the spot and move according to the direction
    of its orientation.

    Its orientation is defined by four compass directions: North, East, South, West.
    These are converted to degrees with the clockwise direction as positive, starting
    from 0 degrees when facing North. North is assumed to correspond to the world's
    Y direction.

    :param robot_name: Reference name to assign to this instance when initialised.
    """
    permissible_orientations = {'NORTH': 0, 'EAST': 90, 'SOUTH': 180, 'WEST': 270}
    """: dict[str, int]: The four possible orientation descriptors and their corresponding angle values in degrees."""

    def __init__(self, robot_name: str = 'Robot') -> None:
        """
        Object Initialisation. Assign default values to attributes (robot_name must be provided).
        """
        super().__init__(robot_name)
        # dict is used for look-up when resolving turning commands
        self.permissible_orientations = {'NORTH': 0, 'EAST': 90, 'SOUTH': 180, 'WEST': 270}

    def plan_move(self, displace_x: int = 0, displace_y: int = 1) -> None:
        """
        Applies 2D rotation to input X and Y displacement inputs based on robot's current orientation and
        sums these to the robot's current X and Y positions. The resulting X and Y values are stored in the planned_x
        and planned_y attributes. The robot's current X and Y positions can be updated to these values by calling
        the accept_move() method.

        :param displace_x: number of units to move along X direction (before rotation)
        :param displace_y: number of units to move along Y direction (before rotation)
        """
        # get current heading and convert angle to radians in right-hand thumb notation
        angle = -1 * self.permissible_orientations[self.orientation] * math.pi / 180
        # calculate resultant X and Y positions using 2D rotation matrix relationships
        self.planned_x = self.x + round(displace_x*math.cos(angle) - displace_y*math.sin(angle))
        self.planned_y = self.y + round(displace_x*math.sin(angle) + displace_y*math.cos(angle))

    def accept_move(self) -> None:
        """Updates the robot's X and Y attributes with the values stored in planned_x and planned_y attributes, which
        are obtained from calling the plan_move() method."""
        self.x = self.planned_x
        self.y = self.planned_y

    def turn_left(self) -> None:
        """
        Steers the robot 90 degrees left and updates current orientation. This is calculated by looking up the angle
        value for the corresponding orientation descriptor from the permissible_orientations dictionary, applying a -90
        degrees rotation, and wrapping the result to ensure it is within the range of [0, 360). The resulting
        orientation is determined by mapping the angle value back to the orientation descriptor in
        permissible_orientations. Note that the positive direction for rotation is taken as clockwise based on the
        representation used in permissible_orientations.
        """
        heading = self._wrap_deg(self.permissible_orientations[self.orientation] - 90)
        self.orientation = list(self.permissible_orientations.keys())[list(self.permissible_orientations.values()).index(heading)]

    def turn_right(self) -> None:
        """
        Steers the robot 90 degrees right and updates current orientation. This is calculated by looking up the angle
        value for the corresponding orientation descriptor from the permissible_orientations dictionary, applying a +90
        degrees rotation, and wrapping the result to ensure it is within the range of [0, 360). The resulting
        orientation is determined by mapping the angle value back to the orientation descriptor in
        permissible_orientations. Note that the positive direction for rotation is taken as clockwise based on the
        representation used in permissible_orientations.
        """
        heading = self._wrap_deg(self.permissible_orientations[self.orientation] + 90)
        self.orientation = list(self.permissible_orientations.keys())[list(self.permissible_orientations.values()).index(heading)]

    @staticmethod
    def _wrap_deg(val: int) -> int:
        """
        Internal method for wrapping an input value between [0, 360)
        :param val: the value to be wrapped
        :returns: the resulting value after applying wrapping operation
        """
        return val % 360


class TableSimulation(AbstractWorld):
    """
    Concrete class for a Table Simulation. It provides proxy methods for commanding
    a robot in the world such that table-imposed constraints are applied to prevent robot moves
    that would lead to it falling from the table. The class prints messages to StdOut to report the status of the
    robot/success of an action when a command is performed and when requested using the REPORT command.

    :param robot: The robot to load into the Table Simulation.
    :param world_name: Reference name to be assigned to the Table Simulation.
    :param dim_x: The x dimension for the created instance of the Table Simulation.
    :param dim_y: The y dimension for the created instance of the Table Simulation.
    """

    def __init__(self, robot: PointRobot, world_name: str = 'Table', dim_x: int = 5, dim_y: int = 5) -> None:
        """
        Object initialisation. Assigns default values to attributes (robot must be specified).
        """
        super().__init__(robot, world_name)
        self.size_x = dim_x
        self.size_y = dim_y
        print(f"[INFO] {self.world_name} created with default dimensions",
              f"[{self.size_x} x {self.size_y}] and origin ({self.origin_x}, {self.origin_y}).")

    def place_robot(self, x: int = 0, y: int = 0, f: str = 'NORTH') -> bool:
        """
        Checks if the requested place location for the robot is within the dimensions of the
        table. If valid, updates the pose of the robot and sets the robot_in_world flag to indicate the robot has been
        placed on the table.

        :param x: Target X position to place the robot.
        :param y: Target Y position to place the robot.
        :param f: Requested orientation to place the robot.
        :returns: True if the PLACE request is valid (within table boundaries), otherwise False.
        """
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
        """Removes the robot by resetting robot location attributes to Default values and sets the robot_in_world
        flag to denote robot is no longer on table."""
        self.robot.x = 0
        self.robot.y = 0
        self.robot.orientation = ""
        self.robot_in_world = False
        print(f"[INFO] {self.robot.robot_name} has been removed from {self.world_name}.")

    def move_robot(self) -> bool:
        """
        Checks if the robot is on the table, and whether a move at its current location
        would lead to it falling from the table. If the planned move is safe, it accepts the move and updates
        the robot position attributes.

        :returns: True if the move command is valid and does not lead to the robot falling from the table, otherwise False.
        """
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
            print("[INFO] Move successful.")
            return True  # command succeeded
        else:
            # robot has not been placed in the world, cannot execute planned move
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}. Unable to move!')
            return False  # command rejected

    def turn_robot_left(self) -> bool:
        """
        Checks if the robot is on the table. If it is, call the robot's turn_left() method.

        :returns: True if the robot is on the table and a turn_left command has been carried out, otherwise False.
        """
        if self.robot_in_world:
            self.robot.turn_left()
            print("[INFO] Turn left successful.")
            return True  # command succeeded
        else:
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}. Unable to turn left!')
            return False  # command rejected

    def turn_robot_right(self) -> bool:
        """
        Checks if the robot is on the table. If it is, call the robot's turn_right() method.

        :returns: True if the robot is on the table and a turn_right command has been carried out, otherwise False.
        """
        if self.robot_in_world:
            self.robot.turn_right()
            print("[INFO] Turn right successful.")
            return True  # command succeeded
        else:
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}. Unable to turn right!')
            return False  # command rejected

    def report_robot_location(self) -> bool:
        """
        Check if the robot is on the table. If it is, report the robot's current pose.

        :returns: True if the robot is on the table and a report has been provided, otherwise False.
        """
        if self.robot_in_world:
            print(f"[INFO] {self.robot.robot_name}'s current pose in {self.world_name} is (X: {self.robot.x},",
                  f"Y: {self.robot.y}, F: {self.robot.orientation}).")
            return True  # command succeeded
        else:
            print(f'[WARNING] {self.robot.robot_name} has not been placed in {self.world_name}.',
                  'Unable to report robot pose!')
            return False  # command rejected
