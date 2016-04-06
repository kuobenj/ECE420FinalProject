import cv2
import numpy as np

filename = 'statusTestVector.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

imgHit = cv2.imread('hitlerTestVec.png')
grayHit = cv2.cvtColor(imgHit,cv2.COLOR_BGR2GRAY)

img3 = cv2.imread('shitty3testVector.png')
gray3 = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)

cv2.imwrite('output2.png', img)

hogDesc = cv2.HOGDescriptor((28,28), (28,28), (28,28), (4,4), 12)

features = hogDesc.compute(gray)
features2 = hogDesc.compute(grayHit)
features3 = hogDesc.compute(gray3)

print repr(features) 
print (str(len(features)))
print sum(abs(features - features2))
print sum(abs(features - features3))
print sum(features[12:23])