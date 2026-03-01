# toy_robot_simulator

This package provides a Python solution to the Toy Robot Simulator exercise. It has been tested on Ubuntu-latest with Python versions 3.10, 3.11, 3.12, and 3.13.

## Dependencies [Optional]

No dependencies outside of the base Python 3 installation is required to run the application (See [Section: Running the application](#running-the-application)). Dependencies are only required for running lint, test scripts, and generating documentation. However, these have also been implemented as Github workflows that are run automatically on a push or pull request trigger for the **`main`** branch.

The full list of dependencies can be found in **`/toy_robot_simulator/requirements.txt`**. To install, run the following (the instructions below assumes pip has been installed):

    python3 -m venv /path/to/target/venv/directory [optional]
    . /path/to/target/venv/directory/bin/activate [optional]
    pip install -r /path/to/requirements.txt

The above includes setting up and activating a Python virtual environment. This is optional but recommended to avoid conflicting dependencies already installed within the local system.

## Documentation

Documentation for this application and its underlying codebase has been made available through Github Pages: [https://cuebong.github.io/toy_robot_simulator/](https://cuebong.github.io/toy_robot_simulator/).

The documentation is auto-generated from Docstrings using Sphinx, and is built automatically using a Github workflow to update the documentation on a push or pull-request trigger from the **`main`** branch. To generate the documentation on a local repository, run the following in a terminal (make sure that the Python virtual environment is activated if using and the above dependencies have been installed):

    cd /path/to/package/docs
    make html
    
To open the documentation locally, go to the **`_build/html`** folder located inside the docs project sub-directory and open **`index.html`**.

## Running the application

To run the application, simply run the following Python script on a terminal using:

    Python3 /path/to/package/toy_robot_simulator/toy_robot_simulator.py

To run the linter and test scripts, enter the following commands on a terminal:

    cd /path/to/package_root_directory
    flake8 --statistics
    pytest -v

## 4. Continuous Integration

An automated lint and test Github workflow (based on flake8 and pytest, respectively) has been created for this package that is triggered on any push and pull request on the **`main`** branch. As of writing, the test scripts achieve 100% coverage for the Python modules used in the Toy Robot Simulator application.
    
## Maintainer

The maintainer of this package is Cuebong Wong.

