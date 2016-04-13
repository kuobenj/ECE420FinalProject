import cv2
import numpy as np

fileNames = ['train0.png', 'train1.png', 'train2.png', 'train3.png', 
			'train4.png', 'train5.png', 'train6.png', 'train7.png', 
			'train8.png', 'train9.png', 'trainx.png', 'trainy.png', 
			'trainleftparen.png', 'trainrightparen.png', 'trainplus.png', 'trainminus.png']



# for fname in fileNames:
# 	img = cv2.cvtColor(cv2.imread('trainingData/orig/' + fname),cv2.COLOR_BGR2GRAY);
# 	img = np.invert(img)
# 	img[img >= 200] = 255
# 	img[img < 200] = 0
# 	img = cv2.filter2D(img, -1, np.ones((5,5)))
# 	img = np.invert(img)
# 	print 'trainingData/binary/'+fname.rsplit( ".", 1 )[ 0 ] + 'Bin.png'
# 	cv2.imwrite('trainingData/binary/'+fname.rsplit( ".", 1 )[ 0 ] + 'Bin.png', img)

img = cv2.cvtColor(cv2.imread('testVector.png'),cv2.COLOR_BGR2GRAY);
img = np.invert(img)
img[img >= 200] = 255
img[img < 200] = 0
img = cv2.filter2D(img, -1, np.ones((5,5)))
img = np.invert(img)
cv2.imwrite('testVectorBin.png', img)
