.. DroneVis documentation master file, created by
   sphinx-quickstart on Fri Dec 16 00:31:04 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DroneVis's documentation!
====================================

**DroneVis** is a full compatible drone library to automate computer vision algorithms on parrot drones. The library and computer vision alogirthms were built with real-time constraints on-mind. 

All of the implemented real-time data, inference, and detection achieve a minimum ``fps >= 4.5`` on an *Intel core 8* CPU.

Github repository: https://github.com/ahmedheakl/drone-vis

Check out the :doc:`guides/install` section for further information, including how to
install the project.

Main Features
-------------

- Unified state-of-the art computer vision algoritms
- Full control over the drone
- PEP8 compliant (unified code style)
- Documented functions and classes
- Tests, high code coverage and type hints
- Clean code
- Multiple implementations for the same models

+-------------------+----------------------+----------------+
| Drone Control     | Detection Models     | Human Counting |
+===================+======================+================+
| Right, Left       | Faster R-CNN         | CSRNet         |
+-------------------+----------------------+----------------+
| Up, Down          | CenterNet            | ...            |
+-------------------+----------------------+----------------+
| Forward, Back     | YOLO                 | ...            |
+-------------------+----------------------+----------------+
| Takeoff, Land     | Single Shot Detector | ...            |
+-------------------+----------------------+----------------+
| Reset, Emergency  | ...                  | ...            |
+-------------------+----------------------+----------------+
| Rotate Left/Right | ...                  | ...            |
+-------------------+----------------------+----------------+
| Hover, Caliberate | ...                  | ...            |
+-------------------+----------------------+----------------+


.. note::

   This project is under active development.


.. toctree::
   :maxdepth: 2
   :caption: User Guide

   guides/install
   guides/quickstart


.. toctree::
   :maxdepth: 2
   :caption: Connections

   connection/drone_connection
   connection/drone
   connection/command
   connection/video

.. toctree::
   :maxdepth: 2
   :caption: Detection

   detection/detect_algo
   detection/ssd
   detection/yolo
   detection/fasterrcnn

.. toctree::
   :maxdepth: 2
   :caption: Pose Estimation and Segmentation

   pose/pose

.. toctree::
   :maxdepth: 1
   :caption: Face Detection

   face_detect/face_detect

.. toctree::
   :maxdepth: 1
   :caption: User Interfaces

   interfaces/gui
   interfaces/commandline

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
