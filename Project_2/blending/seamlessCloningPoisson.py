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
from scipy import misc
from scipy import sparse

def seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY):
    targetH, targetW, _ = targetImg.shape

    indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)

    coeffA = getCoefficientMatrix(indexes)

    src_red = sourceImg[:, :, 0]
    src_green = sourceImg[:, :, 1]
    src_blue = sourceImg[:, :, 2]

    tgt_red = targetImg[:, :, 0]
    tgt_green = targetImg[:, :, 1]
    tgt_blue = targetImg[:, :, 2]

    red_sol = getSolutionVect(indexes, src_red, tgt_red, offsetX, offsetY)
    green_sol = getSolutionVect(indexes, src_green, tgt_green, offsetX, offsetY)
    blue_sol = getSolutionVect(indexes, src_blue, tgt_blue, offsetX, offsetY)

    print red_sol.shape

    red = sparse.linalg.spsolve(coeffA, red_sol.T)
    green = sparse.linalg.spsolve(coeffA, green_sol.T)
    blue = sparse.linalg.spsolve(coeffA, blue_sol.T)

    red = np.ndarray.astype(red , dtype=int)
    green = np.ndarray.astype(green, dtype=int)
    blue = np.ndarray.astype(blue, dtype=int)

    np.set_printoptions(threshold='nan')

    resultImg = reconstructImg(indexes, red, green, blue, targetImg)

    plt.imshow(resultImg)
    plt.show()

    misc.imsave("result.png", resultImg)

    return resultImg
