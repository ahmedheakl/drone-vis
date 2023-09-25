"""Test model factory"""
import pytest
from transformers import (
    VideoMAEForVideoClassification,
    VivitModel,
    TimesformerForVideoClassification,
)

from dronevis.abstract.noop_model import NOOPModel
from dronevis.models.model_factory import ModelFactory


def test_create_none_model():
    """Test create model"""
    model = ModelFactory.create_model("None")
    assert model
    assert isinstance(model, NOOPModel)


def test_create_segmentation_model():
    """Test create segmentation model"""
    model = ModelFactory.create_model("Segment")
    assert model is not None
    assert model.is_seg is True


def test_create_pose_segmentation_model():
    """Test create segmentation model"""
    model = ModelFactory.create_model("Pose+Segment")
    assert model is not None
    assert model.is_seg_pose is True


def test_create_yolov8_track_model():
    """Test create segmentation model"""
    model = ModelFactory.create_model("YOLOv8Track")
    assert model is not None
    assert model.track is True


def test_create_mcg_action_model():
    """Test create segmentation model"""
    model = ModelFactory.create_model("ActionMCG")
    assert model is not None
    assert isinstance(model.net, VideoMAEForVideoClassification)


def test_create_google_action_model():
    """Test create segmentation model"""
    model = ModelFactory.create_model("ActionGoogle")
    assert model is not None
    assert isinstance(model.net, VivitModel)


def test_create_facebook_action_model():
    """Test create segmentation model"""
    model = ModelFactory.create_model("ActionFacebook")
    assert model is not None
    assert isinstance(model.net, TimesformerForVideoClassification)


def test_create_wrong_model():
    """Test create segmentation model"""
    with pytest.raises(ValueError):
        ModelFactory.create_model("Wrong")
