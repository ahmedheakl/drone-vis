# DroneVis: Full compatible drone library to automate computer vision algorithms on parrot drones.

The library is mainly concerned with providing multiple interfaces for controling AR.Drones and running **real-time computer vision alogorithms**. 
#### User Interfaces
- Command Line Interface
- Graphical User Interface
- Hand Gesture Control (control the drone with your hand gestures/movements)

#### Computer Vision Algorithms Features

- Models are work in **real-time constraints** with a **minimum of 5 frames per second on CPU**.

- Models from **multiple domains**:
    * <p style="color: dark-violet; font-weight: bold;">Object Detection/Recognition</p>

        + Faster R-CNN
        + Single Shot Detector (SSD)
        + YOLO
        + YOLOv5
        + CenterNet
    * <p style="color: dark-violet; font-weight: bold;">Crowd Counting</p>
    
        + CSRNet
    * <p style="color: dark-violet; font-weight: bold;">Face Detection</p>
    
        + MobileNetv3
    * <p style="color: dark-violet; font-weight: bold;">Pose Estimation</p>
    
        + Mobilenetv3 + SSD
    * <p style="color: dark-violet; font-weight: bold;">Image Segmentation</p>
    
        <span style="text-decoration: underline; font-style: italic;">(Human segmentation is the only currently developed model)</span>

        + Mobilenetv3 + SSD
    * <p style="color: dark-violet; font-weight: bold;">Human Tracking <span style="text-decoration: underline;">(To be implemented)</span></p>

    * <p style="color: dark-violet; font-weight: bold;">Instance Segmentation<span style="text-decoration: underline;">(To be implemented)</span></p>

-  Built with **integrity constraints** in mind for easier user access; For example, each model is implemented with 4 main methods ``load_model``, ``transform_img``, ``predict``, ``detect_webcam``. Hence, each model can be treated with a high level of abstraction.

- Models are **implemented with multiple frameworks**. For example, Single-shot detector (SSD) model is implemented with PyTorch and Mxnet. 

- *(For the paper)* Detailed comparisons for models in each domain will be provided.

#### Software Engineering Features
- **Fully documented**, see [our docs](https://drone-vis.readthedocs.io/en/latest/)
- **Docker Image** available on [dockerhub](https://hub.docker.com/r/ahmedheakl/dronevis) for easy ship-and-use. 
- Tested on **multiple python environments** with tox envs
- Tested on **multiple platforms** with github CI *(currently on Linux distro's and windows subsystem for Linux)*
- **PEP8 compliant** (unified code style)
- **Offline mode for running models** without the need to download the weights everytime using the model
- **Well tested** with pytest <span style="text-decoration: underline;">(To be implemented)</span>

