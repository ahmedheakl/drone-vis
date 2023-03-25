"""Implementing fixture and hooks to be shared amongst modules"""
from typing import Generator
import pytest
import requests
import os
import shutil

URL_NAME_DICT = {
    "https://drive.google.com/file/d/1YIxL0l8S66cdKnryUCAzZpF20s_VMwoa/view?usp=sharing": "test_video.avi",
    "https://drive.google.com/file/d/1o1LQoiOQ_l6iSJ91hVXPJvqEhp1gB-vJ/view?usp=sharing": "human_photo.jpg",
    "https://drive.google.com/file/d/15cvqF5FuWliuRey4b64Fdh-ewCZ0K7yu/view?usp=sharing": "black_image.jpg",
}

TEST_DATA_PATH = "./test_data"


def pytest_configure() -> None:
    """Configurations for pytest tests"""
    if not os.path.exists(TEST_DATA_PATH):
        os.mkdir(TEST_DATA_PATH)
    os.environ["TEST_DATA_PATH"] = TEST_DATA_PATH
    if os.path.exists(TEST_DATA_PATH) or len(os.listdir(TEST_DATA_PATH)) > 0:
        return

    for url, filename in URL_NAME_DICT.items():
        response = requests.get(url)
        filepath = os.path.join(TEST_DATA_PATH, filename)
        with open(filepath, "wb") as video_writer:
            video_writer.write(response.content)


@pytest.fixture(scope="session", autouse=True)
def remove_donwload_video() -> Generator[None, None, None]:
    yield
    if os.path.exists(TEST_DATA_PATH):
        shutil.rmtree(TEST_DATA_PATH)
