from classes.Simulator import PointRobot, TableSimulation


def run_sequence1(sim: TableSimulation):
    # Test sequence
    sim.move_robot()
    sim.turn_robot_left()
    sim.turn_robot_right()
    sim.report_robot_location()
    sim.place_robot(2, 3, 'EAST')
    sim.report_robot_location()
    sim.move_robot()
    sim.report_robot_location()
    sim.turn_robot_left()
    sim.report_robot_location()
    sim.move_robot()
    sim.report_robot_location()
    sim.place_robot(7, 1, 'SOUTH')
    sim.place_robot(4, 6, 'SOUTH')
    sim.place_robot(0, 0, 'EAST')
    sim.report_robot_location()
    sim.turn_robot_right()
    sim.report_robot_location()
    sim.turn_robot_right()
    sim.report_robot_location()
    sim.move_robot()
    sim.report_robot_location()
    sim.remove_robot()
    sim.report_robot_location()


def run_sequence2(sim: TableSimulation):
    sim.place_robot(0, 0, 'NORTH')
    sim.move_robot()
    sim.report_robot_location()


def run_sequence3(sim: TableSimulation):
    sim.place_robot(0, 0, 'NORTH')
    sim.turn_robot_left()
    sim.report_robot_location()


def run_sequence4(sim: TableSimulation):
    sim.place_robot(1, 2, 'EAST')
    sim.move_robot()
    sim.move_robot()
    sim.turn_robot_left()
    sim.move_robot()
    sim.report_robot_location()


if __name__ == "__main__":
    # Create robot and simulator
    toy_robot = PointRobot(robot_name='Toy Robot')
    simulator = TableSimulation(robot=toy_robot, world_name='Table Simulator')

    print("\n---------------- Running Test Sequence 1 ------------------")
    run_sequence1(simulator)
    simulator.remove_robot()

    print("\n---------------- Running Test Sequence 2 ------------------")
    run_sequence2(simulator)
    simulator.remove_robot()

    print("\n---------------- Running Test Sequence 3 ------------------")
    run_sequence3(simulator)
    simulator.remove_robot()

    print("\n---------------- Running Test Sequence 4 ------------------")
    run_sequence4(simulator)
    simulator.remove_robot()
