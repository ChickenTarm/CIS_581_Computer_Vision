'''
  File name: getIndexes.py
  Author:
  Date created:
'''

import numpy as np


def getIndexes(mask, targetH, targetW, offsetX, offsetY):

	indexes = np.zeros(shape=(targetH,targetW))
	maskY, maskX = mask.shape

	for y in range(0, maskY):
		for x in range(0, maskX):
			indexes[y + offsetY][x + offsetX] = mask[y][x]

	return indexes