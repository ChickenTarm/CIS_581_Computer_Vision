'''
  File name: getSolutionVect.py
  Author:
  Date created:
'''

from scipy import signal
import numpy as np
from PIL import Image
from getIndexes import getIndexes

def getSolutionVect(indexes, source, target, offsetX, offsetY):

	lapacian = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])

	src_Lap = signal.convolve2d(source, lapacian, mode='same', boundary='fill', fillvalue=0)

	srcY, srcX = source.shape

	mask = indexes[offsetY:offsetY+srcY, offsetX:offsetX+srcX]

	mys, mxs = np.nonzero(mask)

	maskPixTup = zip(mys, mxs)

	maskPositionMap = {}

	for i in range(0, len(maskPixTup)):
		maskPositionMap[maskPixTup[i]] = i

	iys, ixs = np.nonzero(indexes)

	indexPixTup = zip(iys, ixs)

	indexMap = {}

	for i in range(0, len(indexPixTup)):
		indexMap[i] = indexPixTup[i]

	numPix = np.count_nonzero(indexes)

	SolVectorb = np.zeros(shape=(1,numPix))

	for y in range(0, srcY):
		for x in range(0, srcX):
			if mask[y][x] == 1:
				SolVectorb[0][maskPositionMap[(y, x)]] = src_Lap[y][x]
			if (y, x) in maskPositionMap:
				ty, tx = indexMap[maskPositionMap[(y,x)]]
				above = indexes[ty-1][tx]
				below = indexes[ty+1][tx]
				left = indexes[ty][tx-1]
				right = indexes[ty][tx+1]
				if above == 0:
					SolVectorb[0][maskPositionMap[(y, x)]] = SolVectorb[0][maskPositionMap[(y, x)]] + target[ty - 1][tx]
				if below == 0:
					SolVectorb[0][maskPositionMap[(y, x)]] = SolVectorb[0][maskPositionMap[(y, x)]] + target[ty + 1][tx]
				if left == 0:
					SolVectorb[0][maskPositionMap[(y, x)]] = SolVectorb[0][maskPositionMap[(y, x)]] + target[ty][tx - 1]
				if right == 0:
					SolVectorb[0][maskPositionMap[(y, x)]] = SolVectorb[0][maskPositionMap[(y, x)]] + target[ty][tx + 1]

	return SolVectorb

# getSolutionVect(getIndexes(np.asarray(Image.open("mask.jpg")), 792, 1056, 544, 116), np.asarray(Image.open("face.jpg"))[:,:,0], np.asarray(Image.open("couple.jpg"))[:,:,0], 544, 116)