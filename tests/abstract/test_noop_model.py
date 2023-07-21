"""Testing no operation model"""
import numpy as np

from dronevis.abstract.noop_model import NOOPModel


def test_idle_transform():
    """Input image should not be affected by noop model transformations"""
    model = NOOPModel()
    model.load_model()
    image = np.zeros((3, 10))
    output_image = model.transform_img(image)

    assert np.equal(image, output_image).all()


def test_idle_predict():
    """Input image should be affected by noop model inference"""
    model = NOOPModel()
    model.load_model()
    image = np.zeros((3, 10))
    output_image = model.predict(image)

    assert np.equal(image, output_image).all()
