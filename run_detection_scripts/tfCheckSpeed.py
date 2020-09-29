import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"]=""
import tensorflow as tf
import pathlib
import time
from PIL import Image


def load_model(model_dir):
    model = tf.saved_model.load(model_dir)
    return model



def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]

    # Run inference
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)
    


    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    
    
    output_dict = {key:value[0, :num_detections].numpy() 
                 for key,value in output_dict.items()}

    # detection_classes should be ints.
    detection_boxes = output_dict['detection_boxes']
    detection_classes = output_dict['detection_classes'].astype(int)
    detection_scores = output_dict['detection_scores']
    
    return num_detections, detection_boxes, detection_classes, detection_scores

def show_inference(model, image_path):
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = np.array(Image.open(image_path))
    # Actual detection.
    num_detections, detection_boxes, detection_classes, detection_scores = run_inference_for_single_image(model, image_np)
    # Visualization of the results of a detection.

# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = pathlib.Path('/home/hydronautics/test/')
TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))

model_dir = '/home/hydronautics/graph_rcnn_200_280920/saved_model/'
detection_model = load_model(model_dir)

average = 0
start_time = time.time()
output_dict_1 = show_inference(detection_model, TEST_IMAGE_PATHS[0])
average += time.time() - start_time
print(average)

average = 0
for image_path in TEST_IMAGE_PATHS:
    start_time = time.time()
    output_dict = show_inference(detection_model, image_path)
    average += time.time() - start_time
    #print(average)
average = average / int(len(TEST_IMAGE_PATHS))
print(average)
