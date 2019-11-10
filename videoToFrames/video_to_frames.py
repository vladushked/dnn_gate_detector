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

print("Starting ...")
if len (sys.argv) == 2:
	print ("Please enter the framerate, destination filename and format!\nExiting ...")
	sys.exit (1)
elif len (sys.argv) == 3:
	print ("Please enter the destination filename and format!\nExiting ...")
	sys.exit (1)
elif len (sys.argv) == 4:
	print ("Please enter the destination format!\nExiting ...")
	sys.exit (1)

elif len (sys.argv) == 5:
	cap = cv.VideoCapture(sys.argv[1])
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
	    if i == int(sys.argv[2]):
	    	print('%s%d.%s' %(sys.argv[3], img_counter, sys.argv[4]))
	    	cv.imwrite('%s%d.%s' %(sys.argv[3], img_counter, sys.argv[4]),frame)
	    	img_counter += 1
	    	i = 0
	    else:
	    	i += 1
	    	#print("FUK UUU!!") 
 	    #if cv.waitKey(0) == ord('q'):
 	    #    break
 	    #cv.imshow('frame', frame)
	cap.release()
	cv.destroyAllWindows()
else:
	print ("Please enter the path to video file, framerate, destination filename and format!\nExiting ...")
