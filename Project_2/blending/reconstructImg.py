'''
  File name: reconstructImg.py
  Author:
  Date created:
'''

import numpy as np


def reconstructImg(indexes, red, green, blue, targetImg):

    resultImg = np.copy(targetImg)

    pixY, pixX = np.nonzero(indexes)

    pixs = zip(pixY, pixX)

    red = red.reshape((len(pixs),))
    green = green.reshape((len(pixs),))
    blue = blue.reshape((len(pixs),))

    for i in range(0, len(pixs)):
        y, x = pixs[i]
        resultImg[y][x][0] = min(max(red[i], 0), 255)
        resultImg[y][x][1] = min(max(green[i], 0), 255)
        resultImg[y][x][2] = min(max(blue[i], 0), 255)
    return resultImg