.. Toy Robot Simulator Application documentation master file, created by
   sphinx-quickstart on Sat Feb 28 2026.

Toy Robot Simulator Application documentation
=============================================
-------------------------------------------
Preface
-------------------------------------------
This package provides a solution to the Toy Robot Simulator Exercise. It implements the solution using Object-Oriented
Programming paradigms and Interfaces to provide a modular solution for future extensibility.

The Toy Robot described in the brief is assumed to be a "point robot" that has no geometry and behaves like a holonomic
robot. This point robot is implemented as a concrete robot class that inherits from an abstract robot interface, with
attributes defined to allow modular changes to its drive behaviours and enable the creation of other types of mobile
robots that would be compatible with the simulation world defined.

The Table simulation environment described in the brief is implemented in a similar way, utilising an AbstractWorld
Interface and a concrete class implementation for the specific table environment used in this application. This
approach allows various parameters of the world, such as the dimensions of the table and coordinates of the origin,
to be changed without requiring any modifications to the rest of the codebase for the application to work. Likewise,
the various constraints that are applied to permitted commands for placing and moving the robot, as well as all other
accepted commands, can be changed within the Table Simulator class without affecting the core behaviours of how the
selected robot moves and steers.

Finally there is the User Interface layer that is implemented as a Requester class, which again inherits from an
AbstractRequester Interface. It provides all user input validations to ensure that only inputs that are compliant
with the expected commands are sent onwards to the Table simulation for actioning. This implementation obtains user
inputs via Standard Input, and reports back to the user via Standard Output. However, through the modular approach
taken to implement this layer, a different Requester subclass could be built to enable a different means of obtaining
input sequences for the application (e.g. through reading from a file) simply by overriding the get_request() method
declared in the AbstractRequester Interface. For example, the test_03_appplication.py testing script overrides this
method (using the concept of 'monkey patching') to enable testing of the application by providing a full test sequence
in place of individual commands provided by user input.

-------------------------------------------
Dependencies
-------------------------------------------
The full list of dependencies can be found in requirements.txt. To install, run the following (the instructions below
assumes pip has been installed)::

   python3 -m venv /path/to/target/venv/directory [optional]
   . /path/to/target/venv/directory/bin/activate [optional]
   pip install -r /path/to/requirements.txt

Note that the above includes setting up and activating a Python virtual environment. This is optional but recommended
to avoid conflicting dependencies already installed within the local system.

The package has been tested in Python versions 3.10+ under Ubuntu-latest OS. A Continuous Integration workflow has been
set up on the Git repository.

-------------------------------------------
Running the application
-------------------------------------------
To run the application, simply run the Python script on a terminal using::

   Python3 /path/to/package/toy_robot_simulator/toy_robot_simulator.py

To run the linter and test scripts, enter the following commands on a terminal::

   cd /path/to/package_root_directory
   flake8 --statistics
   pytest -v


.. toctree::
   :maxdepth: 3
   :caption: Contents:
   
   AbstractClasses
   Simulator
   UserInterface
   toy_robot_simulator

