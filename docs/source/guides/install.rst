Installation
============

Prerequisites
-------------

DroneVis requires python 3.7+, PyTorch >= 1.13.0, TorchVision >= 0.14.0, and mxnet >= 1.9.0

Windows 10
----------

Currently, the library is **neighter tested nor built on Windows 10 platform**. There are two options available though:

1. Use `WSL <https://learn.microsoft.com/en-us/windows/wsl/install>`_ to install Linux on Windows.
2. Fetch our docker image from `DockerHub <https://hub.docker.com/>`_, and run it. 
3. Create a `Docker <https://www.docker.com/>`_ container with *ubuntu >= 20.04*, and install our library.

You can visit the section :ref:`docker <dockerinstall>` for more details.

Linux
-----

The library is **only** heavily tested on ``Ubuntu 20.04 (focal)``. 

Creating a virtual env
~~~~~~~~~~~~~~~~~~~~~~

On ubuntu `20.04` and python `3.8`:


.. note::

   It is recommended to use a virtual environment to avoid packages conflict, but it is ok to omit the virtual env part.


.. code-block:: console
    
    $ sudo apt-get update # update current packages
    $ sudo apt-get install -y virtualenv python3-virtualenv # install python virtualenv
    $ virtualenv ~/dronevisvenv --python=python3.8 # create dronevis virtual env
    $ source ~/dronevis/venv/bin/activate # activate virtualenv
     


Install using pip
~~~~~~~~~~~~~~~~~

To use DroneVis, you need to install it using pip:

.. code-block:: console

   (.dronevisvenv) $ pip install dronevis # install dronevis library


Development version
-------------------

To contribute to DroneVis, with support for running tests and building the documentation.

.. code-block:: console

    $ git clone https://github.com/ahmedheakl/drone-vis
    $ cd drone-vis
    $ pip install -e .[docs]

.. _dockerinstall:

Docker
------

You can now `install docker <https://docs.docker.com/get-docker/>`_ on your platform, and pull our image from ``docker hub`` and start working right-away. 

To pull our docker image ``ahmedheakl/dronevis``:abbr:

.. code-block:: console

    docker pull ahmedheakl/dronevis


To run the image with interactive terminal: 

.. code-block:: console

    docker run -it ahmedheakl/dronevis:latest

You can now start running your favourites computer vision alogrithms. 