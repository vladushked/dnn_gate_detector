# tree
#
#	network_directory
#		frozen_inference_graph.pb
#		network_name.pbtxt
#		object_detection_classes_coco.txt
#	images
#		example_01.jpg
#		example_02.jpg
#		example_03.jpg
#	videos
#		
#	output
#		
#	mask_rcnn.py
#	mask_rcnn_video.py

# import the necessary packages
import numpy as np
import argparse
import random
import time
import cv2
import os

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

# load the COCO class labels our Mask R-CNN was trained on
#labelsPath = os.path.sep.join([args["network_directory"],
#	"classes.txt"])
#LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the Mask R-CNN weights and model configuration
weightsPath = os.path.sep.join([args["network"],
	"frozen_inference_graph.pb"])
configPath = os.path.sep.join([args["network"],
	"faster_rcnn_inception_v2_pets.config"])
 
# load our Mask R-CNN trained on the COCO dataset (90 classes)
# from disk
print("[INFO] loading Network from disk...")
net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)

# load our input image and grab its spatial dimensions
image = cv2.imread(args["image"])
(H, W) = image.shape[:2]

blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
(boxes, masks) = net.forward(["detection_out_final", "detection_masks"])
end = time.time()

# show timing information and volume information on Mask R-CNN
print("[INFO] Mask R-CNN took {:.6f} seconds".format(end - start))
print("[INFO] boxes shape: {}".format(boxes.shape))
print("[INFO] masks shape: {}".format(masks.shape))