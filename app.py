# We will be using Python's OpenCv2 Library to build our Face Scan API

import cv2
import numpy as np
from PIL import ImageGrab

# Getting the OpenCV2 Classifier to detect the frontal face of people
face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Getting access to my computer's webcam
camera = cv2.VideoCapture(0)

# Getting user input for user id!
id = raw_input('enter user id')

# A counter that will be used later!
counter = 0;

# Infinite Loop 
while(True):
	# Gets images from my webcam
	ret, img = camera.read()

	# Changes the images captured from colored to gray
	# This helps in terms of facial recognition
	change_to_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Detects objects in the picture and returns a list of rectangles
	faces = face_csc.detectMultiScale(change_to_gray, 1.3, 5)

	# Basically looking at the rectangles returned by the detectMultiScale function
	for (x, y, w, h) in faces:
		# Increasing our counter
		counter = counter+1;

		# Saving the pictures in a folder as a unique name
		# This is why we have a counter! Each picture has a different id
		cv2.imwrite("dataSet/User." + str(id) + "." + str(counter) + ".jpg", change_to_gray[y:y+h, x:x+w])

		# Forming a rectangle for every face recognized
		# We made the rectangle green
		cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

		cv2.waitKey(150)

	# 
	cv2.imshow('img', img)
	
	cv2.waitKey(1)

	# Breaks out of the while loop after taking a bunch of pictures
	if (counter > 30):
		break

# Closing the camera and shutting down/closing the windows
camera.release()
cv2.destroyAllWindows()
