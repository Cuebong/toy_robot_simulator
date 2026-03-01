.. Toy Robot Simulator Application documentation master file, created by
   sphinx-quickstart on Sat Feb 28 2026.

Simulator module
=============================================

This module provides the concrete classes for creating a point robot (i.e. the 'Toy Robot') and a table simulator
environment for the toy robot simulator application.

The table simulator implements the application-specific 'rules' for robot navigation, preventing any actions other than
PLACE to be issued when the robot has not been placed onto the table. It further prevents any PLACE or MOVE actions that
would cause the robot to fall outside the boundaries of the table.

For this implementation, it is assumed that the robot is safe as long as it resides on or within the boundaries of the
table. The dimensions of the table are 5 x 5 units and the origin is (0, 0). The robot is therefore deemed safe as long
as its x and y coordinates are between [0, 5] (inclusive).

.. automodule:: Simulator
   :members:
   :undoc-members:
   :show-inheritance:

