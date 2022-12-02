from dronevis.object_detection_models import SSD 

import cv2


model = SSD()
model.load_model()

print("Starting Video Stream .... ")
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

"""
Frequency of inference:
    You can decrease the freq for faster FPS, 
    however, you will lower quality inferece. 
"""
predict_iters = 10
iteration = 0

while True:
    ret, frame = cap.read()
    if iteration % predict_iters == 0:
        
        x, img = model.transform_img(frame)
        cv2.imshow('Input', model.predict(img, x))
    else: 
        _, img = model.transform_img(frame)
    iteration += 1
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
    
    


