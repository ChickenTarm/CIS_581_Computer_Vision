'''
  File name: seamlessCloningPoisson.py
  Author:
  Date created:
'''

from getIndexes import getIndexes
from getCoefficientMatrix import getCoefficientMatrix
from getSolutionVect import getSolutionVect
from reconstructImg import reconstructImg
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

def seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY):
	targetH, targetW, _ = targetImg.shape

	indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)

	coeffA = getCoefficientMatrix(indexes)

	src_red = sourceImg[:, :, 0]
	src_blue = sourceImg[:, :, 1]
	src_green = sourceImg[:, :, 2]

	tgt_red = targetImg[:, :, 0]
	tgt_blue = targetImg[:, :, 1]
	tgt_green = targetImg[:, :, 2]

	red_sol = getSolutionVect(indexes, src_red, tgt_red, offsetX, offsetY)
	blue_sol = getSolutionVect(indexes, src_blue, tgt_blue, offsetX, offsetY)
	green_sol = getSolutionVect(indexes, src_green, tgt_green, offsetX, offsetY)

	print "Start inversion"

	solution = np.linalg.inv(coeffA)

	print "inversion done"

	print solution

	red = np.dot(solution, red_sol)
	blue = np.dot(solution, blue_sol)
	green = np.dot(solution, green_sol)

	resultImg = reconstructImg(indexes, red, green, blue, targetImg)

	plt.imshow(resultImg)
	plt.show()

	return resultImg

seamlessCloningPoisson(np.asarray(Image.open("face.jpg")), np.asarray(Image.open("couple.jpg")), np.asarray(Image.open("mask.jpg")), 544, 116)