import cv2
import numpy as np
from dataProcess import *
import random

characterDict = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9',
				 10:'x', 11:'y', 12:'(', 13:')', 14:'+', 15:'-', 16:'=', 100:'.'}

fileNames = ['train0Bin.png', 'train1Bin.png', 'train2Bin.png', 'train3Bin.png', 
			'train4Bin.png', 'train5Bin.png', 'train6Bin.png', 'train7Bin.png', 
			'train8Bin.png', 'train9Bin.png', 'trainxBin.png', 'trainyBin.png', 
			'trainleftparenBin.png', 'trainrightparenBin.png', 'trainplusBin.png', 
			'trainminusBin.png', 'trainEqualsBin.png']

trainPrefix = ['trainingData/processed/train0/train0_', 'trainingData/processed/train1/train1_', 'trainingData/processed/train2/train2_', 'trainingData/processed/train3/train3_', 
			'trainingData/processed/train4/train4_', 'trainingData/processed/train5/train5_', 'trainingData/processed/train6/train6_', 'trainingData/processed/train7/train7_', 
			'trainingData/processed/train8/train8_', 'trainingData/processed/train9/train9_', 'trainingData/processed/trainx/trainx_', 'trainingData/processed/trainy/trainy_', 
			'trainingData/processed/trainleftparen/trainleftparen_', 'trainingData/processed/trainrightparen/trainrightparen_', 'trainingData/processed/trainplus/trainplus_', 
			'trainingData/processed/trainminus/trainminus_', 'trainingData/processed/trainequals/trainequals_']

trainLineSpaceWidth = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100]

def generateFeatureData(filename, filenamePre = '', filenameOutputPre = None, lineSpaceWidth = 1):
	hogDesc = cv2.HOGDescriptor((28,28), (28,28), (28,28), (4,4), 12)
	characterTup = trainingSetFromFile(filenamePre+filename, lineSpaceWidth)
	characterData = characterTup[0]
	if filenameOutputPre is not None:
		trainingDataFileAwayFileAwaaaaay(characterData, filenameOutputPre)
	features = []
	for character in characterData:
		features.append(np.transpose(hogDesc.compute(character))[0,:])
	return (features, characterTup[1])

trainFeatures = []
trainLabels = []
for i in range(0, len(fileNames)):
	features = (generateFeatureData(fileNames[i], 'trainingData/binary/', trainPrefix[i], trainLineSpaceWidth[i]))[0]
	trainFeatures = trainFeatures + features
	trainLabels = trainLabels + ([i] * len(features))

testFeaturesTup = generateFeatureData('exponent3out.png', '', 'testData/test5_')
testFeatures = testFeaturesTup[0]
testPos = testFeaturesTup[1]
testData = np.asarray(testFeatures)

trainData = np.asarray(trainFeatures)
testPos = np.asarray(testFeaturesTup[1])
labels = np.asarray(trainLabels)

print testPos
print testFeaturesTup[1]


svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=2.67, gamma=5.383 )

svm = cv2.SVM()
svm.train(trainData,labels, params=svm_params)
svm.save("handwriting_svm.xml")

heights = testPos[:,1] - testPos[:,0]
middles = (testPos[:,0] + testPos[:,1]) / 2
widths = testPos[:, 2]
maxHeight = np.max(heights)

output = ''
exponent = False
for i in range(0,testData.shape[0]):
	insertStr = ''
	if heights[i] < 0.2*maxHeight and widths[i] < 0.2*maxHeight:
		insertStr = '.'
		result = 100
	else:
		testItem = testData[i]
		result = svm.predict(testItem)
		if i > 0 and result <= 9 and resultprev <= 11 and ((resultprev == 11 and testPos[i,1] < middles[i-1] - heights[i-1]*0.25) or (resultprev != 11 and testPos[i,1] < middles[i-1])):
			insertStr = '^(' + characterDict[int(result)]
			exponent = True
		elif i > 0 and result < 100 and resultprev <= 9 and ((result == 11 and testPos[i-1,1] < middles[i] + heights[i]*0.25) or (resultprev != 11 and testPos[i-1,1] < middles[i])):
			insertStr = ')' + characterDict[int(result)]
			exponent = False
		else:
			insertStr = characterDict[int(result)]
	resultprev = result
	output = output + insertStr

if exponent:
	output = output + ')'

print output

# print repr(features) 
# print (str(len(features)))
# print sum(abs(features - features2))
# print sum(abs(features - features3))
# print sum(features[12:23])
