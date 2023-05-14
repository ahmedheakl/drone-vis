<img src="https://user-images.githubusercontent.com/52796111/235324370-646b53c8-7540-4555-8097-63b4ead2d4fc.png" align="right" width="30%"/>

![CI](https://github.com/ahmedheakl/drone-vis/workflows/test/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/drone-vis/badge/?version=latest)](https://drone-vis.readthedocs.io/) ![coverage report](https://codecov.io/github/ahmedheakl/drone-vis/branch/master/graph/badge.svg)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Version](https://badge.fury.io/py/dronevis.svg)
# DroneVision

Drone Vision (DroneVis) is a full compatible drone library to automate computer vision algorithms on parrot drones. You can read a detailed documentation of Drone Vision [docs](https://drone-vis.readthedocs.io/en/latest).

**DroneVis** is a cutting-edge drone software library that has been specifically designed for use with the AR. Drone 2.0. It has been extensively tested both indoors and outdoors, and offers a wide range of features including adaptability in connecting to the drone, advanced computer vision algorithms, and a user-friendly interface. This makes it easy for users to take full advantage of the drone's capabilities and control it with simple commands.All of the implemented real-time data, inference, and detection achieve a minimum ``fps >= 4.5`` on an Intel core 8 CPU.

## Features
- Unified state-of-the art computer vision algoritms
- Full control over the drone
- PEP8 compliant (unified code style)
- Documented functions and classes
- Tests, high code coverage and type hints
- Clean code
- Multiple implementations for the same models
- Logger with timestamps
- Two UI for easier usage (GUI, CLI)



| Drone Control         | Computer Vision Models| Usage                 |   Implementation      |
|-----------------------|-----------------------|-----------------------|-----------------------|
| Right, Left           | Faster R-CNN          | Detection/Recognition | PyTorch               |
| Up, Down              | CenterNet             | Detection/Recognition | MxNet                 |
| Forward, Backward     | YOLO                  | Detection/Recognition | MxNet                 |
| Takeoff, Land         | YOLOv5                | Detection/Recognition | PyTorch               |
| Reset, Emergency      | SSD                   | Detection/Recognition | PyTorch               |
| Rotate Left/Right     | CSRNet                | Crowd Counting        | PyTorch               |
| Hover, Caliberate     | BlazeFace             | Face Detection        | MediaPipe             |
| Camera Stream         | BlazePose             | Pose Estimation       | MediaPipe             |
| Hand Gesture Control  | BlazePose             | Segmenation           | Mediapipe             |

## How to Install 

You start controling your drone now with just two commands:

```bash
pip install dronevis # install the library 
dronevis-gui # run library GUI
```

<p align="center">
<img src="imgs/dronevis-gui.png" width=700>
</p>

Press the ``start`` button to start a demo drone simulation, and run your favourite algorithms with the ``stream`` button.


<p align="center">
<img src="imgs/dronevis-gui-demo.png" width=700>
</p>

You can control your drone with our ``CLI``:
```bash
dronevis
```

<p align="center">
<img src="imgs/dronevis-cli.png" width=400>
</p>

> :warning: **If you are a Windows**: models implemented with Mxnet library are buggy.

## Getting Started 

Dronevis is built with multiple modes for customizibility. You can view all the options for either runnning our ``GUI`` or ``CLI`` as follows: 

```bash
dronevis --help
```

<p align="center">
<img src="imgs/dronevis-cli-help.png" width=500>
</p>

The default mode for running either the CLI or the GUI is the ``demo`` mode. You can alter the mode by providing "real" to ``--drone`` argument.

```bash
dronevis --drone=real # cli real drone mode
```

or for GUI,

```bash
dronevis-gui --drone=real # gui real drone mode
```

## Documentation 

Dronevis is developed with an extensive documentation for easier user contributions. You can check our full documentation in [here](drone-vis.readthedocs.io/en/latest) to go more in-depth of **how the library is structure** and **how to contribute your favourite model**. 



## Citing the Project

To cite this repository:

```bibtex
@software{drone-vis,
  author  = {Ahmed Heakl, Abdallah-Elbarkokry, Fatma Youssef, Youssief Anas},
  title   = {Dronevis: Full compatible drone library to automate computer vision algorithms on parrot drones},
  year    = {2023},
  url     = {github.com/ahmedheakl/drone-vis},
  version = {1.0.0}
}
```
