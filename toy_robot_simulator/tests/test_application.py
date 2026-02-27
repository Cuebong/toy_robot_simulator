from classes.UserInterface import Requester, InputErrorCodes
from classes.Simulator import TableSimulation, PointRobot
import pytest


@pytest.fixture
def simulator_data():
    toy_robot = PointRobot(robot_name='Toy Robot')
    table_simulator = TableSimulation(robot=toy_robot, world_name='Table Simulator')
    application = Requester(simulator=table_simulator)
    return application


@pytest.mark.application
def test_app_check_request(simulator_data):
    simulator_data.received_request = "PLACE 2 F EAST"
    assert simulator_data.check_request() == InputErrorCodes.PLACE_XY_NOT_INT
