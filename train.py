import numpy as np
from PIL import Image
import cv2, os

# This file helps us train our data of pictures.

# This is the folder where the pictures are stored
path = 'dataset'

# LBPH algorithm that helps train the data
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Function that gets the ID of each image to pair them with the person
def getImages(path):
	# An array of faces and an array of Ids
	faces=[]
	IDs=[]

	ThePaths=[os.path.join(path,f) for f in os.listdir(path)]

	# for loop that gets the ID of each image
	for imagepath in ThePaths:
		faceImg=Image.open(imagepath).convert('L')
		fnp= np.array(faceImg, 'uint8')
		ID=int(os.path.split(imagepath)[-1].split('.')[1])
		faces.append(fnp)
		# print ID
		IDs.append(ID)
		cv2.imshow("training", fnp)
		cv2.waitKey(10)
	return IDs, faces

Ids,faces=getImages(path)

# Training the program to recognize the faces based on their ID
recognizer.train(faces,np.array(Ids))

# Writes this data in the .yml file
recognizer.write('recognizer/trainingData.yml')
cv2.destroyAllWindows()
