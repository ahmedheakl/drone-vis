import cv2
import numpy as np
from typing import Union


def write_fps(image: np.ndarray, fps: Union[str, int, float]) -> np.ndarray:
    """Write fps on input image

    Args:
        image (np.array): input image
        fps (Union[str, int, float]): frame per second

    Returns:
        np.array: processed image with fps written
    """
    assert isinstance(fps, (str, int, float)), "Please enter a valid fps value"
    if not isinstance(fps, str):
        fps = str(int(fps))

    cv2.putText(
        img=image,
        text=f"{fps} FPS",
        org=(15, 30),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=(100, 200, 0),
        thickness=2,
    )
    return image
