"""Implementing fixture and hooks to be shared amongst modules"""
from typing import Generator
import os
from pathlib import Path
import pytest
import requests
from google_drive_downloader import GoogleDriveDownloader as gdd

from dronevis.drone_connect.demo_drone import DemoVideoThread
from dronevis.abstract.base_video_thread import BaseVideoThread

URL_NAME_DICT = {
    "https://drive.google.com/file/d/1YIxL0l8S66cdKnryUCAzZpF20s_VMwoa/view?usp=sharing": "test_video.avi",
    "https://drive.google.com/file/d/1o1LQoiOQ_l6iSJ91hVXPJvqEhp1gB-vJ/view?usp=sharing": "human_photo.jpg",
    "https://drive.google.com/file/d/15cvqF5FuWliuRey4b64Fdh-ewCZ0K7yu/view?usp=sharing": "black_photo.jpg",
    "https://drive.google.com/file/d/1jo3vjs_Lbw6KFVNf6V35IwiTKsp1gvmU/view?usp=sharing": "30fps_image.png",
}

TEST_DATA_FOLDER = "test_data"
TEST_DATA_PATH = os.path.join(os.getcwd(), TEST_DATA_FOLDER)
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


def pytest_configure() -> None:
    """Configurations for pytest tests"""
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    if not os.path.exists(TEST_DATA_PATH):
        os.mkdir(TEST_DATA_PATH)

    os.environ["TEST_DATA_PATH"] = TEST_DATA_PATH
    if os.path.exists(TEST_DATA_PATH) and len(os.listdir(TEST_DATA_PATH)) > 0:
        return

    for url, filename in URL_NAME_DICT.items():
        output_path = os.path.join(TEST_DATA_PATH, filename)
        if Path(filename).suffix in ALLOWED_IMAGE_EXTENSIONS:
            download_image(url, output_path)
        else:
            download_video(url, output_path)


def download_image(url: str, image_path: str) -> None:
    """Downlaod images from provided url"""
    url_id = url.split("/")[-2]
    gdd.download_file_from_google_drive(file_id=url_id, dest_path=image_path)


def download_video(url: str, video_path: str) -> None:
    """Download video from provided url"""
    response = requests.get(url)
    with open(video_path, "wb") as video_writer:
        video_writer.write(response.content)


@pytest.fixture(scope="session", autouse=True)
def remove_donwload_video() -> Generator[None, None, None]:
    yield
    for _, thread in DemoVideoThread._instances.items():
        thread.close_thread()
        thread.join()

    for _, thread in BaseVideoThread._instances.items():
        thread.close_thread()
        thread.join()
