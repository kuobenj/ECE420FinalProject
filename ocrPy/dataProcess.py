import cv2
import numpy as np

def generateCharacterLines(img):
	imgMap = (img/255) * -1 + 1
	lineFinder = np.sum(imgMap, axis = 1)
	characterLines = []
	start = None

	for i in range(0, len(lineFinder)):

		if lineFinder[i] > 0 and (lineFinder[i-1] == 0 or start is None):
			start = i
		elif lineFinder[i] == 0 and lineFinder[i-1] > 0 and start is not None:
			characterLines.append(img[start:(i-1)])
			start = None

	return characterLines

def generateCharacterFromLines(characterLines):
	characterRaw = []

	for l in range(0, len(characterLines)):
		charFinder = np.sum((characterLines[l]/255)*-1 + 1, axis = 0)
		start = None
		for i in range(0, len(charFinder)):
			if charFinder[i] > 0 and (charFinder[i-1] == 0 or start is None):
				start = i
			elif charFinder[i] == 0 and charFinder[i-1] > 0 and start is not None:
				characterRaw.append(characterLines[l][:, start:(i-1)])
				start = None

	return characterRaw

def generateCharacterFormatted(characterRaw):
	characterData = []
	for i in range(0, len(characterRaw)):
		charInv = np.invert(characterRaw[i])
		top = 0
		bottom = charInv.shape[0] - 1
		while np.sum(charInv[top, :]) == 0 and top < bottom:
			top = top + 1
		while np.sum(charInv[bottom, :]) == 0 and bottom > top:
			bottom = bottom - 1
		characterBound = characterRaw[i][top:bottom, :]
		character = np.full((28, 28), 255.0, dtype = np.uint8)
		character[4:24, 4:24] = cv2.resize(characterBound, (20, 20), interpolation = cv2.INTER_LINEAR )
		character[character >= 200] = 255
		character[character < 200] = 0
		characterData.append(character)
	return characterData

def trainingDataFileAwayFileAwaaaaay(characterData, filenamePre):
	for i in range(0, len(characterData)):
		cv2.imwrite(filenamePre+str(i)+'.png', characterData[i])

def trainingSetFromFile(filename):
	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY);
	characterData = generateCharacterFormatted(generateCharacterFromLines(generateCharacterLines(img)))
	return characterData

