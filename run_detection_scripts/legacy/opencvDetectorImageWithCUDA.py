# https://www.pyimagesearch.com/2018/11/19/mask-r-cnn-with-opencv/


# import the necessary packages
import numpy as np
import cv2 as cv
import os
import time
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-n", "--network", required=True,
	help="base path to network directory")
ap.add_argument("-v", "--visualize", type=int, default=0,
	help="whether or not we are going to visualize each instance")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# loading the labels
labelsPath = os.path.sep.join(["labels.txt"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the Mask R-CNN weights and model configuration
weightsPath = os.path.sep.join([args["network"],
	"frozen_inference_graph.pb"])
configPath = os.path.sep.join([args["network"],
	"opencv_graph.pbtxt"])

# load our NET from disk
print("[INFO] loading %s from disk..." % (args['network']))
cvNet = cv.dnn.readNetFromTensorflow(weightsPath, configPath)

print("[INFO] setting preferable backend and target to CUDA...")
cvNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
cvNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

img = cv.imread(args["image"])
rows = img.shape[0]
cols = img.shape[1]
cvNet.setInput(cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
start = time.time()
cvOut = cvNet.forward()
end = time.time()

# show timing information and volume information on NET
print("[INFO] %s took {:.6f} seconds".format(end - start) % (args['network']))
print("[INFO] boxes shape: {}".format(cvOut.shape))

# loop over the number of detected objects
for i in range(0, cvOut.shape[2]):
    # extract the class ID of the detection along with the confidence
    # (i.e., probability) associated with the prediction
    classID = int(cvOut[0, 0, i, 1])
    confidence = cvOut[0, 0, i, 2]
 
    # filter out weak predictions by ensuring the detected probability
    # is greater than the minimum probability
    if confidence > args["confidence"]:
        # clone our original image so we can draw on it
        clone = img.copy()
 
        # scale the bounding box coordinates back relative to the
        # size of the image and then compute the width and the height
        # of the bounding box
        box = cvOut[0, 0, i, 3:7] * np.array([cols, rows, cols, rows])
        (startX, startY, endX, endY) = box.astype("int")
        boxW = endX - startX
        boxH = endY - startY 
        cv.rectangle(clone, (startX, startY), (endX, endY), 
            (23, 230, 210), thickness=2)  

        # draw the predicted label and associated probability of the
        # instance segmentation on the image
        text = "{}: {:.4f}".format(LABELS[classID], confidence)
        cv.putText(clone, text, (startX, startY - 5),
            cv.FONT_HERSHEY_SIMPLEX, 0.5, (23, 230, 210), 2)

        cv.imshow('img', clone)
        cv.waitKey()
"""
for detection in cvOut[0,0,:,:]:
    print(detection)
    score = float(detection[2])
    if score > 0.5:
        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows
        cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)

cv.imshow('img', img)
cv.waitKey()
"""