# toy_robot_simulator

This package provides a Python solution to the Toy Robot Simulator exercise. It has been tested on Ubuntu-latest with Python versions 3.10, 3.11, 3.12, and 3.13.

## Dependencies

The full list of dependencies can be found in requirements.txt. To install, run the following (the instructions below assumes pip has been installed):

    python3 -m venv /path/to/target/venv/directory [optional]
    . /path/to/target/venv/directory/bin/activate [optional]
    pip install -r /path/to/requirements.txt

Note that the above includes setting up and activating a Python virtual environment. This is optional but recommended to avoid conflicting dependencies already installed within the local system.

## Documentation

The package has been documented using Docstrings, and as such, documentation for the package can be auto-generated from the code using Sphinx. To generate the documentation, run the following in a terminal (make sure that the Python virtual environment is activated if using and the above dependencies have been installed):

    cd /path/to/package/docs
    make html
    
To open the the documentation, go the the build/html folder located inside the docs project sub-directory and open index.html.

## Running the application

To run the application, simply run the Python script on a terminal using:

    Python3 /path/to/package/toy_robot_simulator/toy_robot_simulator.py

To run the linter and test scripts, enter the following commands on a terminal:

    cd /path/to/package_root_directory
    flake8 --statistics
    pytest -v

## Continuous Integration

A lint and test workflow has been created for this package that is triggered on any push and pull request on the Main branch.
    
## Matainer

The maintainer of this package is Cuebong Wong.

