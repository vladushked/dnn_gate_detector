# This script made by Vladislav Plotnikov (vladik1209@gmail.com)
# This script transforms your video into number of pictures. Pictures from your video produces every second
# To run this script run the following command in bash terminal
#
# $ python [path_to_your_work_directory]/video_to_frames.py [path_to_your_video] [framerate] [picture_filename] [format]
#
# To take more pictures for each second, just divide [framerate] parameter.
# [format] parameter can be: jpg, png and etc. Write it without any dots!

import sys
import cv2 as cv
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter


def main(input_video, framerate, output_name, image_extension):
    cap = cv.VideoCapture(input_video)
    print("Video is opened: %s" % (cap.isOpened()))
    i = 0
    img_counter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if (not ret and img_counter == 0):
            print("Can't receive frame. Exiting ...")
            break
        elif (not ret and img_counter > 0):
            print("Finish!")
            break
        if i == int(framerate):
            print('%s%d.%s' % (output_name, img_counter, image_extension))
            cv.imwrite('%s%d.%s' %
                       (output_name, img_counter, image_extension), frame)
            img_counter += 1
            i = 0
        else:
            i += 1
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = ArgumentParser(
        description='This script transforms your video into number of pictures. Pictures from your video produces every second\n'
        'To run this script run the following command in bash terminal \n'
        '$ python [path_to_your_work_directory]/video_to_frames.py [path_to_your_video] [framerate] [picture_filename] [format]\n'
        'To take more pictures for each second, just divide [framerate] parameter. \n'
        '[format] parameter can be: jpg, png and etc. Write it without any dots! ', formatter_class=RawTextHelpFormatter)
    ap.add_argument("-i", "--input_video", required=True,
                    help="path to video")
    ap.add_argument("-f", "--framerate", type=int, default=12,
                    help="saving framerate")
    ap.add_argument("-o", "--output_name", required=True,
                    help="output image names start with this string")
    ap.add_argument("-e", "--image_extension", default='jpg',
                    help="percentage of evaluation data")
    args = vars(ap.parse_args())
    main(args["input_video"], args["framerate"], args["output_name"], args["image_extension"])
