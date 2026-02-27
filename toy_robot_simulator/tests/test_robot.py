from classes.Simulator import PointRobot
import pytest

@pytest.fixture
def robot_data():
    robot = PointRobot(robot_name="Toy Robot")
    return robot

@pytest.mark.robot
def test_robot_move(robot_data):
    robot_data.orientation = "NORTH"
    robot_data.plan_move(displace_x=0, displace_y=1)
    robot_data.accept_move()
    assert (robot_data.x == 0) and (robot_data.y == 1)
