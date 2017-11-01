'''
  File name: getCoefficientMatrix.py
  Author:
  Date created:
'''

import numpy as np

def getCoefficientMatrix(indexes):

	numPixs = np.count_nonzero(indexes)

	coeffA = np.zeros(shape=(numPixs, numPixs))

	postionMap = {}

	yMax, xMax = indexes.shape

	y1s, x1s = np.nonzero(indexes)

	pixTup = zip(y1s, x1s)

	for i in range(0, len(pixTup)):
		postionMap[pixTup[i]] = i

	for y in range(1, yMax-1):
		for x in range(1, xMax-1):
			if (y, x) in postionMap:
				currPix = postionMap[(y, x)]
				coeffA[currPix][currPix] = 4
				above = indexes[y-1][x]
				below = indexes[y+1][x]
				left = indexes[y][x-1]
				right = indexes[y][x+1]
				if above > 0:
					coeffA[currPix][postionMap[(y-1, x)]] = -1
				if below > 0:
					coeffA[currPix][postionMap[(y+1, x)]] = -1
				if left > 0:
					coeffA[currPix][postionMap[(y, x-1)]] = -1
				if right > 0:
					coeffA[currPix][postionMap[(y, x+1)]] = -1

	return coeffA