import cv2
import numpy as np

def generateCharacterLines(img, lineSpaceWidth = 1):
	imgMap = (img/255) * -1 + 1
	lineFinder = np.sum(imgMap, axis = 1)
	characterLines = []
	start = None

	for i in range(0, len(lineFinder)):
		if lineFinder[i] > 0 and (np.sum(lineFinder[max(0,i-1-lineSpaceWidth):i-1]) == 0 or start is None):
			start = i
		elif np.sum(lineFinder[i:min(i+lineSpaceWidth, len(lineFinder) - 1)]) == 0 and lineFinder[i-1] > 0 and start is not None:
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
	characterPos = []
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

		height = characterBound.shape[0]
		width = characterBound.shape[1]

		if height > width:
			newHeight = 20
			newWidth = int(width * newHeight/height/2) * 2
			if newWidth <= 0:
				newWidth = 2
		else:
			newWidth = 20
			newHeight = int(height * newWidth/width/2) * 2
			if newHeight <= 0:
				newHeight = 2

		characterScaled = cv2.resize(characterBound, (newWidth, newHeight), interpolation = cv2.INTER_LINEAR )

		characterScaled[characterScaled >= 200] = 255
		characterScaled[characterScaled < 200] = 0

		character[(14 - newHeight/2):(14 + newHeight/2), (14 - newWidth/2):(14 + newWidth/2)] = characterScaled

		character = np.invert(character)
		character = cv2.filter2D(character, -1, np.ones((2,2)))
		character = np.invert(character)
		
		characterData.append(character)
		characterPos.append((top,bottom, width))

	return (characterData, characterPos)

def trainingDataFileAwayFileAwaaaaay(characterData, filenamePre):
	for i in range(0, len(characterData)):
		cv2.imwrite(filenamePre+str(i)+'.png', characterData[i])

def trainingSetFromFile(filename, lineSpaceWidth = 1):
	img = cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2GRAY);
	lines = generateCharacterLines(img, lineSpaceWidth)
	characterData = generateCharacterFormatted(generateCharacterFromLines(lines))
	return characterData

