# import pytest
# from dronevis.detection_gluoncv import SSD
# import numpy as np

# @pytest.fixture
# def model():
#     return SSD()

# @pytest.fixture
# def dummy_data():
#     return np.zeros((10, 10), dtype=np.float32)


# def test_loading_model(model):
#     model.load_model()
    
#     assert model.net is not None, "Model is loaded, however, ``net`` attribute is not initialized."

# # def test_predict_net_init(model, dummy_data):
# #     with pytest.raises(AssertionError):
# #         model.predict(dummy_data)
