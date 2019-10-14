import sys
import cv2 as cv

print("Starting ...")
if len (sys.argv) == 2:
	print ("Please enter the framerate and destination filename!\nExiting ...")
	sys.exit (1)

elif len (sys.argv) == 3:
	print ("Please enter the destination filename!\nExiting ...")
	sys.exit (1)

elif len (sys.argv) == 4:
	cap = cv.VideoCapture(sys.argv[1])
	print("Video is opened: %s" % (cap.isOpened()))
	i = 0
	img_counter = 0
	while cap.isOpened():
	    ret, frame = cap.read()
	    # if frame is read correctly ret is True
	    if not ret:
	        print("Can't receive frame (stream end?). Exiting ...")
	        break
	    if i == int(sys.argv[2]):
	    	#print("FUK UUU!!")
	    	cv.imwrite('%s%d.png' %(sys.argv[3], img_counter),frame)
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
	print ("Please enter the path to video file, framerate and destination filename!\nExiting ...")
