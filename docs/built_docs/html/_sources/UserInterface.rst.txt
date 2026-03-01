.. Toy Robot Simulator Application documentation master file, created by
   sphinx-quickstart on Sat Feb 28 2026.

User Interface module
=============================================

This module provides the concrete class for creating a "requester" application that implements the user interaction
behaviour and main business logic for sending commands to the simulator.

It uses Standard Input to obtain string requests from the user. This is parsed by a checker to validate the request
before sending onwards to the simulator. These checks ensure that the input string complies with the format expected
by the application and checks for the following:

1. Are there too few arguments for a PLACE command?
2. Are there too many arguments for a PLACE command?
3. Is the requested F value (the orientation) for a PLACE command unrecognised?
4. Are there unrecognised arguments for the requested command (excluding PLACE)?
5. Is the requested command unrecognised?

The Requester will recognise the following commands:

1. PLACE X Y F
2. MOVE
3. LEFT
4. RIGHT
5. REPORT
6. QUIT

The first five commands above follow the descriptions given in the Toy Robot Simulator Exercise brief, while the QUIT
command provides a way for the user to terminate the session cleanly. Note that whilst the simulator class that the
Requester points to additionally include an implementation to remove the robot from the world, this is not exposed by the
Requester as it is not a specified requirement within the Exercise brief. The remove() method has therefore been built-in
for future-proofing purposes only.

.. automodule:: UserInterface
   :members:
   :undoc-members:
   :show-inheritance:

