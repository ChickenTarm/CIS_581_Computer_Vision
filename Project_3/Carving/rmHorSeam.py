'''
  File name: rmHorSeam.py
  Author:
  Date created:
'''

import numpy as np


def rmHorSeam(I, My, Tby):
  yMax, xMax = My.shape

  Iy = np.zeros(shape=(yMax - 1, xMax, 3))

  end = My[:, xMax - 1]

  bestIndex = np.argmin(end)

  colDict = {}

  y = bestIndex
  x = xMax - 1

  E = My[y][x]

  colDict[x] = y

  while x > 0:
    change = Tby[y][x]
    y = y + change
    x = x - 1
    colDict[x] = y

  for i in range(0, xMax):
    yIgn = colDict[i]
    Iy[0 : yIgn, i, :] = I[0 : yIgn, i, :]
    Iy[yIgn : yMax - 1, i, :] = I[min(yIgn + 1, yMax - 1) : yMax, i, :]

  return Iy, E
