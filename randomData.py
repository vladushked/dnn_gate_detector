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
IMAGES = args["images_directory"]
if args["labels_directory"]: 
	LABELS = args["labels_directory"]
else: LABELS = args["images_directory"]

print('------------------\n')

# step into directory and take files
images = [f for f in os.listdir(IMAGES) if (os.path.isfile(os.path.join(IMAGES, f)) and (f.endswith(".jpg") or f.endswith(".png")))]
labels = [f for f in os.listdir(LABELS) if (os.path.isfile(os.path.join(IMAGES, f)) and (f.endswith(".txt") or f.endswith(".xml")) and (f != 'classes.txt'))]
images_quantity = len(images)

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
# random_counter = [random.randrange(0,images_quantity,1) for i in range(int(images_quantity*args['percentage']))]
random_counter = []
for i in range(int(images_quantity*args['percentage'])):
	r = random.randrange(0,images_quantity,1)
	for j in range(len(random_counter)):
		if r == random_counter[j]:
			
			break
	random_counter.append(r)
print(random_counter)
print(len(random_counter))
print('\n------------------')
# Oh, man, you labeled a lot of images