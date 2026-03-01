from classes.Simulator import PointRobot, TableSimulation
from classes.UserInterface import Requester


def run_simulation():
    """
    Creates instances of the toy robot, table simulator, and requester application, and runs application.
    """
    # Create robot and simulator
    toy_robot = PointRobot(robot_name='Toy Robot')
    table_simulator = TableSimulation(robot=toy_robot, world_name='Table Simulator')

    # Create application and run
    application = Requester(simulator=table_simulator)
    application.run()


if __name__ == "__main__":
    run_simulation()
    print("Application has terminated.")
