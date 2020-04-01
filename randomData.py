# 
# Wanna pick out random images from your dataset and make an evaluation data?
# Just use this script, man!
# 
# Written by VLADUSHKED, vladik1209@gmail.com, 11.2019

DESCRIPTION = "Wanna pick out random images from your dataset and make an evaluation data? Just use this script, man!"

import os
import argparse
import shutil
import random

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description = DESCRIPTION)
ap.add_argument("-i", "--images_directory", required = True,
	help="path to directory with images")
ap.add_argument("-l", "--labels_directory",
	help="path to directory with labels")
ap.add_argument("-p", "--percentage", type = float, default = 0.2,
	help="percentage of evaluation data")
args = vars(ap.parse_args())

# read our args to some constants
IMAGES_DIR = args["images_directory"]
if args["labels_directory"]: 
	LABELS_DIR = args["labels_directory"]
else: LABELS_DIR = args["images_directory"]

print('------------------\n')

# step into directory and take files
images = [f for f in os.listdir(IMAGES_DIR) if (os.path.isfile(os.path.join(IMAGES_DIR, f)) and (f.endswith(".jpg") or f.endswith(".png")))]
labels = [f for f in os.listdir(LABELS_DIR) if (os.path.isfile(os.path.join(IMAGES_DIR, f)) and (f.endswith(".txt") or f.endswith(".xml")) and (f != 'classes.txt'))]

# make train and eval directories
DATA_DIR = 'data'
TRAIN_DIR = 'train'
EVAL_DIR = 'eval'
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
    print("Directory " , DATA_DIR ,  " Created ")
    if not os.path.exists(os.path.join(DATA_DIR, TRAIN_DIR)):
        os.mkdir(os.path.join(DATA_DIR, TRAIN_DIR))
    if not os.path.exists(os.path.join(DATA_DIR, EVAL_DIR)):
        os.mkdir(os.path.join(DATA_DIR, EVAL_DIR))
else:    
    print("Directory " , DATA_DIR ,  " already exists")
    print("DIRECTORY ", DATA_DIR, " WILL BE DELETED! \nDO YOU WANT TO CONTINUE? \n")
    input("Press Enter to continue...")
    shutil.rmtree(DATA_DIR)
    os.mkdir(DATA_DIR)
    os.mkdir(os.path.join(DATA_DIR, TRAIN_DIR))
    os.mkdir(os.path.join(DATA_DIR, EVAL_DIR))

# pick eval images
eval_images_quantity = int(len(images)*args['percentage'])
random_images = random.sample(images, eval_images_quantity)
for img in images:
	lbl = img[:len(img) - 3] + "xml"
	if img in random_images:
		shutil.copyfile(os.path.join(IMAGES_DIR, img), os.path.join(DATA_DIR, EVAL_DIR, img))
		shutil.copyfile(os.path.join(LABELS_DIR, lbl), os.path.join(DATA_DIR, EVAL_DIR, lbl))
	else:
		shutil.copyfile(os.path.join(IMAGES_DIR, img), os.path.join(DATA_DIR, TRAIN_DIR, img))
		shutil.copyfile(os.path.join(LABELS_DIR, lbl), os.path.join(DATA_DIR, TRAIN_DIR, lbl))

print('\n------------------')
# Oh, man, you labeled a lot of images