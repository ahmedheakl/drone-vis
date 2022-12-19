import cv2
def write_fps(image, fps):
    """Write fps on input image

    Args:
        image (np.array): input image
        fps (str | int | float): frame per second

    Returns:
        np.array: processed image with fps written
    """
    if not isinstance(fps, str):
        fps = str(int(fps))
    cv2.putText(
        image,
        f"{fps} FPS",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (100, 200, 0),
        2,
    )
    return image 