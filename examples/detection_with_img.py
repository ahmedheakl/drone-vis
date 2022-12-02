from dronevis.object_detection_models import SSD
from gluoncv import utils


# initialize object
ssd = SSD()

# load model with default pretrained version
ssd.load_model()

# download img. You can add yourown img
img_name = utils.download(
    "https://raw.githubusercontent.com/zhreshold/"
    + "mxnet-ssd/master/data/demo/dog.jpg",
    path="dog.jpg",
)


# load the img from disk and transform it
x, img = ssd.load_and_transform_img(img_name)

# make inference
ssd.predict(img, x)

# show result img with bouding box
ssd.plot_bounding_box(img)
