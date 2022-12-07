from dronevis.object_detection_models.centernet import CenterNet
from gluoncv import utils


# initialize object
model = CenterNet()

# load model with default pretrained version
model.load_model()

# download img. You can add yourown img
img_name = utils.download(
    "https://raw.githubusercontent.com/zhreshold/"
    + "mxnet-ssd/master/data/demo/dog.jpg",
    path="dog.jpg",
)


# load the img from disk and transform it

# Carefull with transform functions as each model
# returns a unique set of parameters. Check the docs
# for more info 
x, img = model.transform_and_load_img(img_name)

# make inference
model.predict(img, x)

# show result img with bouding box
model.plot_bounding_box(img)
