import os
import argparse
import shutil

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
	help="path to directory")
ap.add_argument("-p", "--percentage", type=float, default=0.2,
	help="percentage of test data")
args = vars(ap.parse_args())

# step into our directory and take files
imagesAndLabels = [f for f in os.listdir(args["directory"]) if os.path.isfile(os.path.join(args["directory"], f))]
print('> Directory has %d images' %(int(len(imagesAndLabels)/2)))

imagesAndLabelsQuantity = int(len(imagesAndLabels))
