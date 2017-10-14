'''
  File name: reconstructImg.py
  Author:
  Date created:
'''

import numpy as np


def reconstructImg(indexes, red, green, blue, targetImg):

    resultImg = np.copy(targetImg)

    pixY, pixX = np.count_nonzero(indexes)

    pixs = zip(pixY, pixX)

    for i in range(0, len(pixs)):
        y, x = pixs[i]
        resultImg[y][x][0] = red[i]
        resultImg[y][x][1] = green[i]
        resultImg[y][x][2] = blue[i]
    return resultImg