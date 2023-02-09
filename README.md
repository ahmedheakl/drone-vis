<p><img src="https://badge.fury.io/py/dronevis.svg">
<img src="https://readthedocs.org/projects/drone-vis/badge/?version=latest">
<img src="https://github.com/ahmedheakl/drone-vis/workflows/build/badge.svg">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg">
<img src="https://codecov.io/github/ahmedheakl/drone-vis/branch/master/graph/badge.svg">
<img src="https://github.com/ahmedheakl/drone-vis/workflows/test/badge.svg">
</p>

// dummy
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

You start controling your drone now with just two commands 

```bash
pip install dronevis # install the library 
dronevis-gui # run library GUI
```


> :warning: **If you are using mobile browser**: Be very careful here!
