import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimage

img = cv2.cvtColor(cv2.imread('trainCalibri1Bin.png'),cv2.COLOR_BGR2GRAY);

imgMap = (img/255) * -1 + 1

lineFinder = np.sum(imgMap, axis = 1)

characterLines = []
characterRaw = []

start = 0
for i in range(0, len(lineFinder)):
	if lineFinder[i] > 0 and lineFinder[i-1] == 0:
		start = i
	elif lineFinder[i] == 0 and lineFinder[i-1] > 0:
		characterLines.append(img[start:(i-1)])

for l in range(0, len(characterLines)):
	charFinder = np.sum((characterLines[l]/255)*-1 + 1, axis = 0)
	start = 0
	for i in range(0, len(charFinder)):
		if charFinder[i] > 0 and charFinder[i-1] == 0:
			start = i
		elif charFinder[i] == 0 and charFinder[i-1] > 0:
			characterRaw.append(characterLines[l][:, start:(i-1)])

for i in range(0, len(characterRaw)):
	print i
	cv2.imwrite('train1/train1'+str(i)+'.png', characterRaw[i])

cv2.imwrite('train1_0.png', characterRaw[0])

cv2.imwrite('output.png',characterLines[0])
#plt.imshow(characterLines[0], cmap='Greys')

print len(lineFinder)
plt.show()

print repr(img)