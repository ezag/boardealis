Boardealis
==========
.. image:: https://travis-ci.org/ezag/boardealis.svg?branch=master
    :target: https://travis-ci.org/ezag/boardealis

.. image:: https://codecov.io/gh/ezag/boardealis/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ezag/boardealis

Getting Started
---------------

- Change directory into your newly created project.

    cd boardealis

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
