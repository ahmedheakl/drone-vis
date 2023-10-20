Installation
============

Prerequisites
-------------

DroneVis requires python 3.7+, PyTorch >= 1.13.0, TorchVision >= 0.14.0


Linux, Windows, MacOs
--------------------- 

You need to install the PyTorch version that match your GPU capabilities. You can find the right version for your GPU `here <https://pytorch.org/get-started/locally/>`_. Also, the Pytorch version should match your cuda version, check it `here <https://pytorch.org/get-started/previous-versions/>`_.


Creating a virtual env (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Additionally, to have a comprehensive development environment, you can install the development dependencies:

.. code-block:: console
    
    $ pip install -r requirements-dev.txt

.. _dockerinstall:

Docker
------

You can now `install docker <https://docs.docker.com/get-docker/>`_ on your platform, and pull our image from ``docker hub`` and start working right-away. 

To pull our docker image ``ahmedheakl/dronevis``:

.. code-block:: console

    $ docker pull ahmedheakl/dronevis


To run the image with interactive terminal: 

.. code-block:: console

    $ docker run -it ahmedheakl/dronevis

You can now start running your favourites computer vision alogrithms. 