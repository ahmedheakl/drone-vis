"""Testing SSD Model implementation"""
from typing import Generator, Tuple
import pytest
import os
from PIL import Image
import numpy as np

from dronevis.models import SSD

TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "")
HUMAN_PHOTO = TEST_DATA_PATH + "/human_photo.jpg"
BLACK_PHOTO = TEST_DATA_PATH + "/black_photo.jpg"
THRESHOLD_SCORE = 0.7


@pytest.fixture(scope="session")
def load_files() -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
    human_photo_pil = Image.open(HUMAN_PHOTO)
    human_photo = np.asarray(human_photo_pil)

    black_photo_pil = Image.open(BLACK_PHOTO)
    black_photo = np.asarray(black_photo_pil)

    yield human_photo, black_photo


def test_model_predictions_with_human(load_files):
    """When the model is prompted with a photo of a human, it should
    generate a score for a huamn in the photo larger than a threshold
    score.
    """
    model = SSD()
    model.load_model()
    human_photo, black_photo = load_files
    pred_image = model.predict(human_photo, THRESHOLD_SCORE)
    assert model.pred_scores is not None

    assert len(model.pred_scores[model.pred_scores > THRESHOLD_SCORE]) > 0

    pred_image = model.predict(black_photo)
    assert model.pred_scores is not None

    assert len(model.pred_scores[model.pred_scores > THRESHOLD_SCORE]) == 0
