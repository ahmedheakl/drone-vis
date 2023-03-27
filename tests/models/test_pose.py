"""Testing pose estimation module"""
import pytest

from dronevis.models import PoseSegEstimation


def test_multiple_return_type() -> None:
    """Testing whether the model does not allow multiple but
    conflicting inferences"""
    with pytest.raises(AssertionError) as _:
        PoseSegEstimation(is_seg=True, is_seg_pose=True)
