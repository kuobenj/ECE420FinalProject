import cv2
import numpy as np
from dataProcess import *
import random

characterDict = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9',
				 10:'x', 11:'y', 12:'(', 13:')', 14:'+', 15:'-'}

fileNames = ['train0Bin.png', 'train1Bin.png', 'train2Bin.png', 'train3Bin.png', 
			'train4Bin.png', 'train5Bin.png', 'train6Bin.png', 'train7Bin.png', 
			'train8Bin.png', 'train9Bin.png', 'trainxBin.png', 'trainyBin.png', 
			'trainleftparenBin.png', 'trainrightparenBin.png', 'trainplusBin.png', 'trainminusBin.png']
trainPrefix = ['trainingData/processed/train0/train0_', 'trainingData/processed/train1/train1_', 'trainingData/processed/train2/train2_', 'trainingData/processed/train3/train3_', 
			'trainingData/processed/train4/train4_', 'trainingData/processed/train5/train5_', 'trainingData/processed/train6/train6_', 'trainingData/processed/train7/train7_', 
			'trainingData/processed/train8/train8_', 'trainingData/processed/train9/train9_', 'trainingData/processed/trainx/trainx_', 'trainingData/processed/trainy/trainy_', 
			'trainingData/processed/trainleftparen/trainleftparen_', 'trainingData/processed/trainrightparen/trainrightparen_', 'trainingData/processed/trainplus/trainplus_', 
			'trainingData/processed/trainminus/trainminus_']

def generateFeatureData(filename, filenamePre = '', filenameOutputPre = None):
	hogDesc = cv2.HOGDescriptor((28,28), (28,28), (28,28), (4,4), 12)
	characterData = trainingSetFromFile(filenamePre+filename)
	if filenameOutputPre is not None:
		trainingDataFileAwayFileAwaaaaay(characterData, filenameOutputPre)
	features = []
	for character in characterData:
		features.append(np.transpose(hogDesc.compute(character))[0,:])
	return features

trainFeatures = []
trainLabels = []
for i in range(0, len(fileNames)):
	features = generateFeatureData(fileNames[i], 'trainingData/binary/', trainPrefix[i])
	trainFeatures = trainFeatures + features
	trainLabels = trainLabels + ([i] * len(features))

testFeatures = generateFeatureData('testVectorBin.png', '', 'testData/test_')
testData = np.asarray(testFeatures)

trainData = np.asarray(trainFeatures)

labels = np.asarray(trainLabels)

# labels = np.full(len(train1Features), 1, dtype = np.float32)
# labels = np.concatenate([labels, np.full(len(train2Features), 2, dtype = np.float32)])
# labels = np.concatenate([labels, np.full(len(train3Features), 3, dtype = np.float32)])


svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=2.67, gamma=5.383 )

svm = cv2.SVM()
svm.train(trainData,labels, params=svm_params)

output = ''
for testItem in testData:
	result = svm.predict(testItem)
	output = output + characterDict[int(result)]

print output

# print repr(features) 
# print (str(len(features)))
# print sum(abs(features - features2))
# print sum(abs(features - features3))
# print sum(features[12:23])