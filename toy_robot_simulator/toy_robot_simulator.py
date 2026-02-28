from classes.Simulator import PointRobot, TableSimulation
from classes.UserInterface import Requester


if __name__ == "__main__":
    # Create robot and simulator
    toy_robot = PointRobot(robot_name='Toy Robot')
    table_simulator = TableSimulation(robot=toy_robot, world_name='Table Simulator')

    application = Requester(simulator=table_simulator)
    application.run()

    print("Application has terminated.")
