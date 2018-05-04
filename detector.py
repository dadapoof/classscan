import cv2
import numpy as np
from collections import Counter

# This is the camera that is used in the classroom

# We do something similar to the app.py by setting up the face recognition. However, this time we have names attributed to each face recognized.
# This also runs until we stop it with a key

present = []


face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# The cam is my webcam for now
cam = cv2.VideoCapture(0)

rec=cv2.face.LBPHFaceRecognizer_create()

# Taking the info frmo the trainer
rec.read("recognizer/trainingData.yml")
id=0

# Attributes for the putText. This is how we write the name under each person's face!
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 2
fontcolor = (255, 255, 255)
x = 0
y = 0
w = 0
h = 0

mode_list = [""]


# infinite loop
while(True):
	ret, img = cam.read()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_csc.detectMultiScale(gray, 1.3, 5)

	# For each rectangle found. aka each face detected,
	# We check to see which ID the face corresponds to
	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
		id,conf=rec.predict(gray[y:y+h, x:x+w])
		if (id == 0):
			id="Hritik"
			present.append(id)
			mode_list.append(str("Hritik"))
		if (id == 1):
			id="David"
			present.append(id)
			mode_list.append(str("David"))
	mode = Counter(mode_list)
	cv2.putText(img, str(mode.most_common(1)), (x,y+h), fontface, fontscale, fontcolor)
	del mode_list[:]

	cv2.imshow('img', img)
	
	# Runs until I press the Escape key (27)
	key = cv2.waitKey(1)
	if key == 27:
		break

def Present():
	return present

cam.release()
cv2.destroyAllWindows()
