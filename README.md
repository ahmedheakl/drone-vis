<p><img src="https://badge.fury.io/py/dronevis.svg">
<img src="https://readthedocs.org/projects/drone-vis/badge/?version=latest">
<img src="https://github.com/ahmedheakl/drone-vis/workflows/build/badge.svg">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg">
<img src="https://codecov.io/github/ahmedheakl/drone-vis/branch/master/graph/badge.svg">
<img src="https://github.com/ahmedheakl/drone-vis/workflows/test/badge.svg">
</p>

<p>
<img src="https://img.shields.io/badge/gitlab%20ci-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white" height=20>

<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" height=20>

<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" height=20>

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" height=20>
<img src="https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge" height=20>
</p>

**`Documentation`** |
------------------- |
[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](https://drone-vis.readthedocs.io/en/latest) |


# DroneVis: Full compatible drone library to automate computer vision algorithms on parrot drones.

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

Here are the drone control functionalities:
|                   |                    |                   |                   |
|-------------------|--------------------|-------------------|-------------------|
| Right, Left       | Reset, Emergency   | Hover, Caliberate | Forward, Backward |
| Up, Down          | Rotate Left/Right  | Camera Stream     | Takeoff, Land     |

Here are the models implemented to provide vision for the drone:

| Computer Vision Model | Usage                 |   Implementation      |
|-----------------------|-----------------------|-----------------------|
| Faster R-CNN          | Detection/Recognition | PyTorch               |
| CenterNet             | Detection/Recognition | MxNet                 |
| YOLO                  | Detection/Recognition | MxNet                 |
| YOLOv5                | Detection/Recognition | PyTorch               |
| SSD                   | Detection/Recognition | PyTorch               |
| CSRNet                | Crowd Counting        | PyTorch               |
| BlazeFace             | Face Detection        | MediaPipe             |
| BlazePose             | Pose Estimation       | MediaPipe             |
| BlazePose             | Segmenation           | Mediapipe             |

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
  author  = {Ahmed Heakl, Abdallah-Elbarkokry, Fatma Youssef},
  title   = {Dronevis: Full compatible drone library to automate computer vision algorithms on parrot drones},
  year    = {2022},
  url     = {github.com/ahmedheakl/drone-vis},
  version = {0.2.2}
}
```
