'''
  File name: rmVerSeam.py
  Author:
  Date created:
'''

import numpy as np


def rmVerSeam(I, Mx, Tbx):

  yMax, xMax = Mx.shape

  Ix = np.zeros(shape=(yMax, xMax - 1, 3))

  bottom = Mx[yMax - 1, :]

  bestIndex = np.argmin(bottom)

  rowDict = {}

  print "bestIndexVert: " + str(bestIndex)

  y = yMax - 1
  x = bestIndex

  E = Mx[y][x]

  rowDict[y] = x

  while y > 0:
    change = Tbx[y][x]
    y = y - 1
    x = x + change
    rowDict[y] = x

  for i in range(0, yMax):
    xIgn = rowDict[i]
    # print "xIgn: " + str(xIgn)
    Ix[i, 0 : xIgn, :] = I[i, 0 : xIgn, :]
    Ix[i, xIgn : xMax-1, :] = I[i, min(xIgn + 1, xMax - 1): xMax, :]

  return Ix, E