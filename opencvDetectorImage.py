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

img = cv.imread(args["image"])
rows = img.shape[0]
cols = img.shape[1]
cvNet.setInput(cv.dnn.blobFromImage(img, swapRB=True, crop=False))
start = time.time()
cvOut = cvNet.forward()
end = time.time()

# show timing information and volume information on NET
print("[INFO] %s took {:.6f} seconds".format(end - start) % (args['network']))
print("[INFO] boxes shape: {}".format(cvOut.shape))


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