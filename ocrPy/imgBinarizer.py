import cv2
import numpy as np

fileNames = ['trainCalibri1.png', 'trainCalibri2.png']

for fname in fileNames:
	img = cv2.cvtColor(cv2.imread(fname),cv2.COLOR_BGR2GRAY);
	img[img > 20] = 255
	img[img <= 20] = 0
	cv2.imwrite(fname.rsplit( ".", 1 )[ 0 ] + 'Bin.png', img)

