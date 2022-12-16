Installation
============

Prerequisites
-------------

DroneVis requires python 3.7+, PyTorch >= 1.13.0, TorchVision >= 0.14.0, and mxnet >= 1.9.0

Windows 10
----------

Currently, the library is **neighter tested or built on Windows 10 platform**, however,
you can use `WSL <https://learn.microsoft.com/en-us/windows/wsl/install>`_ to install Linux on Windows.

Another option is to create a `Docker <https://www.docker.com/>`_ container with *ubuntu >= 20.04*, and install our
library.

You can also visit the section :ref:`docker <dockerinstall>`.

Linux
-----

The library is **only** heavily tested on ``Ubuntu 20.04 (focal)``. 

Creating a virtual env
~~~~~~~~~~~~~~~~~~~~~~

On ubuntu `20.04` and python `3.8`:


.. note::

   It is recommended to use virtual environments to avoid packages conflict, but it is ok to omit the virtual env part.


.. code-block:: console
    
    $ sudo apt-get update # update current packages
    $ sudo apt-get install -y virtualenv python3-virtualenv # install python virtualenv
    $ virtualenv ~/dronevisvenv --python=python3.8 # create dronevie virtual env
    $ source ~/dronevis/venv/bin/activate # activate virtualenv
     


Install using pip
~~~~~~~~~~~~~~~~~

To use DroneVis, first install it using pip:

.. code-block:: console

   (.dronevisvenv) $ pip install dronevis # install dronevis library


Development version
-------------------

To contribute to DroneVis, with support for running tests and building the documentation.

.. code-block:: bash

    git clone https://github.com/ahmedheakl/drone-vis
    cd drone-vis
    pip install -e .[docs]

.. _dockerinstall:

Docker
------